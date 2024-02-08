# python -m llmchat.reranker.reranker_model_worker --model-path D:/workdir/models/reranker/bge-reranker-base --model-names bge-reranker-base --device cpu --no-register

import requests

data = {
    "sentences": [
        ['哈喽', '嗨'],
        ['早上好', '晚上好'],
        ['你在做什么', '你干啥呢'],
        ['你好', '你好'],
    ]
}
response = requests.post("http://localhost:21015/worker_compute_score", json=data)
print(response.json())


data = {
    "query": "哈喽",
    "texts": ["哈喽", "嗨", "你好", "早上好"]
}
response = requests.post("http://localhost:21015/worker_compute_score_by_query", json=data)
print(response.json())
