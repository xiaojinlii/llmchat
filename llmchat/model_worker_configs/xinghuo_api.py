import os

config = {
    "model_name": "xinghuo-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("XINGHUO_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("XINGHUO_API_PORT", 21004))
    },

    # 具体注册及api key获取请前往 https://xinghuo.xfyun.cn/
    "online_model": {
        "APPID": "",
        "APISecret": "",
        "api_key": "",
        "version": "v1.5",  # 你使用的讯飞星火大模型版本，可选包括 "v3.0", "v1.5", "v2.0"
        "provider": "XingHuoWorker",
    }

}
