import argparse
import os
import sys
import uuid

import uvicorn
from fastapi import Request
from fastchat.serve.base_model_worker import BaseModelWorker, app, acquire_worker_semaphore, release_worker_semaphore
from fastchat.utils import build_logger
from typing import List

from starlette.responses import JSONResponse

worker_id = str(uuid.uuid4())[:8]
logger = build_logger("embeddings_model_worker", f"embeddings_model_worker_{worker_id}.log")
sys.modules["fastchat.serve.base_model_worker"].logger = logger


class EmbeddingWorker(BaseModelWorker):
    def __init__(
            self,
            controller_addr: str,
            worker_addr: str,
            worker_id: str,
            model_path: str,
            model_names: List[str],
            limit_worker_concurrency: int,
            no_register: bool,
            device: str,
    ):
        super().__init__(
            controller_addr,
            worker_addr,
            worker_id,
            model_path,
            model_names,
            limit_worker_concurrency,
        )

        logger.info(f"Loading the embeddings model {self.model_names} on worker {worker_id} ...")

        self.model_path = model_path

        model_name: str = model_names[0]
        if model_name == "text-embedding-ada-002":  # openai text-embedding-ada-002
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(model=model_name,
                                               openai_api_key=model_path)
        elif 'bge-' in model_name:
            from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
            self.embeddings = HuggingFaceBgeEmbeddings(
                model_name=model_path,
                model_kwargs={'device': device}
            )
            if model_name == "bge-large-zh-noinstruct":  # bge large -noinstruct embedding
                self.embeddings.query_instruction = ""
        else:
            from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=model_path,
                model_kwargs={'device': device}
            )

        if not no_register:
            self.init_heart_beat()

    def get_embeddings(self, params):
        self.call_ct += 1

        ret = {"embedding": [], "token_num": 0}
        texts = params["input"]
        out_embeddings = self.embeddings.embed_documents(texts)
        ret["embedding"] = out_embeddings
        return ret

    def get_query_embeddings(self, params):
        self.call_ct += 1

        ret = {"embedding": [], "token_num": 0}
        text = params["input"]
        out_embedding = self.embeddings.embed_query(text)
        ret["embedding"] = out_embedding
        return ret


@app.post("/worker_get_query_embeddings")
async def get_query_embeddings(request: Request):
    params = await request.json()
    await acquire_worker_semaphore()
    embedding = worker.get_query_embeddings(params)
    release_worker_semaphore()
    return JSONResponse(content=embedding)


def create_embeddings_model_worker():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=21015)
    parser.add_argument("--worker-address", type=str, default="http://localhost:21015")
    parser.add_argument(
        "--controller-address", type=str, default="http://localhost:20001"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default="BAAI/bge-large-zh-v1.5",
        help="The path to the weights. This can be a local folder or a Hugging Face repo ID.",
    )
    parser.add_argument(
        "--model-names",
        type=lambda s: s.split(","),
        help="Optional display comma separated names",
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["cpu", "cuda", "mps", "xpu", "npu"],
        default="cuda",
        help="The device type",
    )
    parser.add_argument(
        "--limit-worker-concurrency",
        type=int,
        default=5,
        help="Limit the model concurrency to prevent OOM.",
    )
    parser.add_argument("--no-register", action="store_true")
    parser.add_argument(
        "--ssl",
        action="store_true",
        required=False,
        default=False,
        help="Enable SSL. Requires OS Environment variables 'SSL_KEYFILE' and 'SSL_CERTFILE'.",
    )
    args = parser.parse_args()
    logger.info(f"args: {args}")

    worker = EmbeddingWorker(
        args.controller_address,
        args.worker_address,
        worker_id,
        args.model_path,
        args.model_names,
        args.limit_worker_concurrency,
        no_register=args.no_register,
        device=args.device,
    )
    return args, worker


if __name__ == "__main__":
    args, worker = create_embeddings_model_worker()
    if args.ssl:
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level="info",
            ssl_keyfile=os.environ["SSL_KEYFILE"],
            ssl_certfile=os.environ["SSL_CERTFILE"],
        )
    else:
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
