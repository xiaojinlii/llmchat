import os

config = {
    "model_name": "moonshot-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("MOONSHOT_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("MOONSHOT_API_PORT", 21013))
    },

    "online_model": {
        "version": "moonshot-v1-8k",
        "api_base_url": "https://api.moonshot.cn/v1",
        "api_key": "sk-XXX",
        "provider": "OpenaiWorker",
    }

}
