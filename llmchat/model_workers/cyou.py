import sys
import time
import hashlib

from llmchat.model_workers.base import *
from llmchat.utils import get_httpx_client
from fastchat import conversation as conv
import json
from typing import List, Dict
import random
from fastchat.conversation import Conversation
from llmchat.settings import logger, log_verbose

DEFAULT_ANSWER = "徒儿所说的问题竟然难住了为师，徒儿不妨提些其它问题。"

def calculate_md5(input_string):
    md5 = hashlib.md5()
    md5.update(input_string.encode('utf-8'))
    encrypted = md5.hexdigest()
    return encrypted

def replace_str(input_string):
    if input_string == '' or input_string == 'null':
        logger.warning("gpt response: text = null!")
        return DEFAULT_ANSWER
    print(f"\ninput_string = {input_string}")
    output_string = input_string.replace('<回答>','')
    output_string = output_string.replace('</回答>','')
    output_string = output_string.replace('<答案>','')
    output_string = output_string.replace('</答案>','')
    output_string = output_string.replace('<回复>','')
    output_string = output_string.replace('</回复>','')
    output_string = output_string.replace('<附加内容>','')
    output_string = output_string.replace('</附加内容>','')
    print(f"\noutput_string = {output_string}")
    output_string.replace('\'','')
    output_string.replace('\"','')
    output_string.replace('“','')
    output_string.replace('”','')
    return output_string

class CyouWorker(ApiModelWorker):
    def __init__(
            self,
            *,
            model_names: List[str] = ["cyou-api"],
            controller_addr: str,
            worker_addr: str,
            **kwargs,
    ):
        kwargs.update(model_names=model_names, controller_addr=controller_addr, worker_addr=worker_addr)
        kwargs.setdefault("context_len", 8192)
        super().__init__(**kwargs)

    def do_chat(self, params: ApiChatParams) -> Dict:
        try:
            params.load_config_not_declare(self.model_names[0])

            data = {
                "bodyArray": params.messages,
                "temperature": params.temperature
            }
            json_data = json.dumps(data)

            timestamp = int(time.time() * 1000)
            signature = calculate_md5(params.clientId + params.privateKey + params.api_url + str(timestamp) + json_data)

            req_params = {
                'clientId': params.clientId,
                'timestamp': timestamp,
                'random': random.random(),
                'algorithm': "MD5",
                'sign': signature,
            }

            url = params.server_address + params.api_url

            if log_verbose:
                logger.info(f'{self.__class__.__name__}:url: {url}')
                logger.info(f'{self.__class__.__name__}:params: {params}')
                logger.info(f'{self.__class__.__name__}:json: {data}')

            with get_httpx_client() as client:
                response = client.post(url=url, params=req_params, json=data)
                if response.status_code == 200:
                    rjson_data = response.json()
                    if log_verbose:
                        logger.info(f'{self.__class__.__name__}:response: {rjson_data}')

                    if rjson_data["msg"] is None:
                        answer = rjson_data["data"]["content"]
                        answer = replace_str(answer)
                        yield {
                            "error_code": 0,
                            "text": answer
                        }
                    else:
                        error_msg = rjson_data['msg'].split(', ', 1)[1]
                        error_msg = error_msg.strip('"')
                        msg_content = json.loads(error_msg)

                        message = msg_content['error']['message']
                        status = msg_content['error']['status']

                        yield {
                            "error_code": status,
                            "text": message
                        }
                else:
                    yield {
                        "error_code": response.status_code,
                        "text": response.text
                    }

        except Exception as e:
            logger.error(f"CyouWorker.do_chat发生Error : {e}")

    def get_embeddings(self, params):
        # TODO: 支持embeddings
        print("embedding")
        print(params)

    def make_conv_template(self, conv_template: str = None, model_path: str = None) -> Conversation:
        # TODO: 确认模板是否需要修改
        return conv.Conversation(
            name=self.model_names[0],
            system_message="",
            messages=[],
            roles=["user", "assistant", "system"],
            sep="\n### ",
            stop_str="###",
        )


if __name__ == "__main__":
    import uvicorn
    from llmchat.utils import MakeFastAPIOffline
    from fastchat.serve.model_worker import app

    worker = CyouWorker(
        controller_addr="http://127.0.0.1:20001",
        worker_addr="http://127.0.0.1:21001",
    )
    sys.modules["fastchat.serve.model_worker"].worker = worker
    MakeFastAPIOffline(app)
    uvicorn.run(app, port=21001)
    # # do_request()
