import os

config = {
    "model_name": "minimax-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("MINIMAX_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("MINIMAX_API_PORT", 21003))
    },

    # 具体注册及api key获取请前往 https://api.minimax.chat/
    "online_model": {
        "group_id": "",
        "api_key": "",
        "is_pro": False,
        "provider": "MiniMaxWorker",
    }

}
