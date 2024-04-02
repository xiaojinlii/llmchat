import sys
import os
from fastchat.conversation import Conversation
from openai import OpenAI

from llmchat.model_workers.base import *
from llmchat.utils import get_httpx_client, get_model_worker_config
from fastchat import conversation as conv
import json
from typing import List, Dict
from llmchat.settings import logger, log_verbose


class OpenaiWorker(ApiModelWorker):
    def __init__(
            self,
            *,
            controller_addr: str = None,
            worker_addr: str = None,
            model_names: List[str],
            **kwargs,
    ):
        kwargs.update(model_names=model_names, controller_addr=controller_addr, worker_addr=worker_addr)
        super().__init__(**kwargs)

        config = get_model_worker_config(model_names[0])
        self.client = OpenAI(
            api_key=config["api_key"],
            base_url=config["api_base_url"],
        )

    def do_chat(self, params: ApiChatParams) -> Dict:
        params.load_config(self.model_names[0])

        try:
            completion = self.client.chat.completions.create(
                model=params.version,
                messages=params.messages,
                temperature=params.temperature,
                max_tokens=params.max_tokens if params.max_tokens else None,
                stream=True,
            )

            text = ""
            for c in completion:
                chunk = c.choices[0].delta.content
                if chunk is not None:
                    text += chunk
                yield {
                    "error_code": 0,
                    "text": text
                }
        except Exception as e:
            self.logger.error(f"请求 Openai API 时发生错误：{e}")
            yield {
                "error_code": 400,
                "text": e
            }

    def get_embeddings(self, params):
        print("embedding")
        print(params)

    def make_conv_template(self, conv_template: str = None, model_path: str = None) -> Conversation:
        return conv.Conversation(
            name=self.model_names[0],
            system_message="You are a helpful, respectful and honest assistant.",
            messages=[],
            roles=["user", "assistant", "system"],
            sep="\n### ",
            stop_str="###",
        )


if __name__ == "__main__":
    import uvicorn
    from llmchat.utils import MakeFastAPIOffline
    from fastchat.serve.base_model_worker import app

    worker = OpenaiWorker(
        controller_addr="http://127.0.0.1:20001",
        worker_addr="http://127.0.0.1:21008",
    )
    sys.modules["fastchat.serve.model_worker"].worker = worker
    MakeFastAPIOffline(app)
    uvicorn.run(app, port=21008)
