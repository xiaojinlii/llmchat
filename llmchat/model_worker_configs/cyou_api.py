import os

config = {
    "model_name": "cyou-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("CYOU_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("CYOU_API_PORT", 21011))
    },

    "online_model": {
        "clientId": "",
        "privateKey": "",
        "server_address": "http://127.0.0.0:8100",
        "api_url": "/cyouNeiOpenAi/api/chatGpt",
        "provider": "CyouWorker",
    }

}
