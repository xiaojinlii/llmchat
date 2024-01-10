import os


config = {
    "model_name": "qwen-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("QWEN_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("QWEN_API_PORT", 21007))
    },

    # 阿里云通义千问 API，文档参考 https://help.aliyun.com/zh/dashscope/developer-reference/api-details
    "online_model": {
        "version": "qwen-turbo",  # 可选包括 "qwen-turbo", "qwen-plus"
        "api_key": "",  # 请在阿里云控制台模型服务灵积API-KEY管理页面创建
        "provider": "QwenWorker",
        "embed_model": "text-embedding-v1"  # embedding 模型名称
    }

}
