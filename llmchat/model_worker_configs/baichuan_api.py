import os

config = {
    "model_name": "baichuan-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("BAICHUAN_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("BAICHUAN_API_PORT", 21008))
    },

    # 百川 API，申请方式请参考 https://www.baichuan-ai.com/home#api-enter
    "online_model": {
        "version": "Baichuan2-53B",  # 当前支持 "Baichuan2-53B"， 见官方文档。
        "api_key": "",
        "secret_key": "",
        "provider": "BaiChuanWorker",
    }

}
