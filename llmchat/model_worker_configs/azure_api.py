import os

config = {
    "model_name": "azure-api",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("AZURE_API_HOST", "127.0.0.1"),
        "port": int(os.getenv("AZURE_API_PORT", 21009))
    },

    # Azure API
    "online_model": {
        "deployment_name": "",  # 部署容器的名字
        "resource_name": "",  # https://{resource_name}.openai.azure.com/openai/ 填写resource_name的部分，其他部分不要填写
        "api_version": "",  # API的版本，不是模型版本
        "api_key": "",
        "provider": "AzureWorker",
    }

}
