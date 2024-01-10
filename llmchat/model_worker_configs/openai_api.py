import os

config = {
    "model_name": "openai-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("OPENAI_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("OPENAI_API_PORT", 21001))
    },

    "online_model": {
        "model_name": "gpt-3.5-turbo",
        "api_base_url": "https://api.openai.com/v1",
        "api_key": "",
        "openai_proxy": "",
    }

}
