import os

config = {
    "model_name": "gemini-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("GEMINI_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("GEMINI_API_PORT", 21012))
    },

    # Gemini API https://makersuite.google.com/app/apikey
    "online_model": {
        "api_key": "",
        "provider": "GeminiWorker",
    }

}
