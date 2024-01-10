import os

config = {
    "model_name": "zhipu-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("ZHIPU_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("ZHIPU_API_PORT", 21002))
    },

    # 具体注册及api key获取请前往 http://open.bigmodel.cn
    "online_model": {
        "api_key": "",
        "version": "chatglm_turbo",  # 可选包括 "chatglm_turbo"
        "provider": "ChatGLMWorker",
    }

}
