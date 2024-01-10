import os

config = {
    "model_name": "fangzhou-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("FANGZHOU_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("FANGZHOU_API_PORT", 21006))
    },

    # 火山方舟 API，文档参考 https://www.volcengine.com/docs/82379
    "online_model": {
        "version": "chatglm-6b-model",  # 当前支持 "chatglm-6b-model"， 更多的见文档模型支持列表中方舟部分。
        "version_url": "",  # 可以不填写version，直接填写在方舟申请模型发布的API地址
        "api_key": "",
        "secret_key": "",
        "provider": "FangZhouWorker",
    }

}
