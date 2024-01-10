import os

config = {
    "model_name": "qianfan-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("QIANFAN_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("QIANFAN_API_PORT", 21005))
    },

    # 百度千帆 API，申请方式请参考 https://cloud.baidu.com/doc/WENXINWORKSHOP/s/4lilb2lpf
    "online_model": {
        "version": "ERNIE-Bot",  # 注意大小写。当前支持 "ERNIE-Bot" 或 "ERNIE-Bot-turbo"， 更多的见官方文档。
        "version_url": "",  # 也可以不填写version，直接填写在千帆申请模型发布的API地址
        "api_key": "",
        "secret_key": "",
        "provider": "QianFanWorker",
    }

}
