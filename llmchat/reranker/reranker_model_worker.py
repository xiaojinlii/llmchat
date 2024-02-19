import argparse
import os
import sys
import uuid

import uvicorn
from fastapi import Request
from fastchat.serve.base_model_worker import BaseModelWorker, app, acquire_worker_semaphore, release_worker_semaphore
from fastchat.utils import build_logger
from typing import List

from sentence_transformers import CrossEncoder
from starlette.responses import JSONResponse

worker_id = str(uuid.uuid4())[:8]
logger = build_logger("reranker_model_worker", f"reranker_model_worker_{worker_id}.log")
sys.modules["fastchat.serve.base_model_worker"].logger = logger

class RerankerWorker(BaseModelWorker):
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
            batch_size: int = 32,
            num_workers: int = 0,
    ):
        super().__init__(
            controller_addr,
            worker_addr,
            worker_id,
            model_path,
            model_names,
            limit_worker_concurrency,
        )

        logger.info(f"Loading the reranker model {self.model_names} on worker {worker_id} ...")

        self.model_path = model_path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.model = CrossEncoder(model_name=model_path, max_length=1024, device=device)

        if not no_register:
            self.init_heart_beat()

    def compute_score(self, sentence_pairs: List[List[str]]) -> List[float]:
        self.call_ct += 1

        scores = self.model.predict(
            sentences=sentence_pairs,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            convert_to_tensor=True
        )

        results = scores.numpy().tolist()
        return results

    def compute_score_by_query(self, query: str, texts: List[str]) -> List[float]:
        sentence_pairs = [[query, text] for text in texts]
        return self.compute_score(sentence_pairs)


@app.post("/worker_compute_score")
async def compute_score(request: Request):
    params = await request.json()
    await acquire_worker_semaphore()
    embedding = worker.compute_score(params["sentences"])
    release_worker_semaphore()
    return JSONResponse(content=embedding)


@app.post("/worker_compute_score_by_query")
async def compute_score_by_query(request: Request):
    params = await request.json()
    await acquire_worker_semaphore()
    embedding = worker.compute_score_by_query(params["query"], params["texts"])
    release_worker_semaphore()
    return JSONResponse(content=embedding)


def create_reranker_model_worker():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=21031)
    parser.add_argument("--worker-address", type=str, default="http://localhost:21031")
    parser.add_argument(
        "--controller-address", type=str, default="http://localhost:20001"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default="BAAI/bge-reranker-base",
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

    worker = RerankerWorker(
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
    args, worker = create_reranker_model_worker()
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
