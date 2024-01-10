import os

config = {
    "model_name": "tiangong-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("TIANGONG_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("TIANGONG_API_PORT", 21010))
    },

    # 昆仑万维天工 API https://model-platform.tiangong.cn/
    "online_model": {
        "version": "SkyChat-MegaVerse",
        "api_key": "",
        "secret_key": "",
        "provider": "TianGongWorker",
    }

}
