# python -m llmchat.embeddings.embeddings_model_worker --model-path D:/workdir/models/embedding/bge-large-zh-v1.5 --model-names bge-large-zh-v1.5 --device cpu --no-register

import requests

data = {
    "input": "哈喽"
}
response = requests.post("http://localhost:21015/worker_get_embeddings", json=data)
print(response.json())


data = {
    "input": "哈喽"
    # "input": ["哈喽", "嗨"]
}
response = requests.post("http://localhost:21015/worker_get_query_embeddings", json=data)
print(response.json())
