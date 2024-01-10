import os

config = {
    "model_name": "",

    "base": {
        "online_api": True,  # True:线上模型, False:离线模型
        "vllm_enabled": False,
    },

    "server": {
        "host": os.getenv("DEFAULT_MODEL_WORKER_HOST", "127.0.0.1"),
        "port": int(os.getenv("DEFAULT_MODEL_WORKER_PORT", 21001))
    },

    # 线上模型
    "online_model": {
        "model_name": "gpt-3.5-turbo",
        "api_base_url": "https://api.openai.com/v1",
        "api_key": "",
        "openai_proxy": "",
    },

    # 离线模型
    "offline_model": {
        "model_path": "/root/models/llm/Qwen/Qwen-14B-Chat",
        "device": "auto",  # LLM 运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。

        # model_worker多卡加载需要配置的参数
        # "gpus": None, # 使用的GPU，以str的格式指定，如"0,1"，如失效请使用CUDA_VISIBLE_DEVICES="0,1"等形式指定
        # "num_gpus": 1, # 使用GPU的数量
        # "max_gpu_memory": "20GiB", # 每个GPU占用的最大显存

        # 以下为model_worker非常用参数，可根据需要配置
        # "load_8bit": False, # 开启8bit量化
        # "cpu_offloading": None,
        # "gptq_ckpt": None,
        # "gptq_wbits": 16,
        # "gptq_groupsize": -1,
        # "gptq_act_order": False,
        # "awq_ckpt": None,
        # "awq_wbits": 16,
        # "awq_groupsize": -1,
        # "model_names": LLM_MODELS,
        # "conv_template": None,
        # "limit_worker_concurrency": 5,
        # "stream_interval": 2,
        # "no_register": False,
        # "embed_in_truncate": False,
    },

    # 推理加速框架，注意使用vllm必须有gpu，且仅支持Linux，详情见 https://docs.vllm.ai/en/latest/
    # vllm对一些模型支持还不成熟，暂时默认关闭，详情见 https://docs.vllm.ai/en/latest/models/supported_models.html
    # fschat=0.2.33的代码有bug, 如需使用，源码修改fastchat.server.vllm_worker，
    # 将103行中sampling_params = SamplingParams的参数stop=list(stop)修改为stop= [i for i in stop if i!=""]
    "vllm": {
        # tokenizer = model_path # 如果tokenizer与model_path不一致在此处添加
        # 'tokenizer_mode':'auto',
        # 'trust_remote_code':True,
        # 'download_dir':None,
        # 'load_format':'auto',
        # 'dtype':'auto',
        # 'seed':0,
        # 'worker_use_ray':False,
        # 'pipeline_parallel_size':1,
        # 'tensor_parallel_size':1,
        # 'block_size':16,
        # 'swap_space':4 , # GiB
        # 'gpu_memory_utilization':0.90,
        # 'max_num_batched_tokens':2560,
        # 'max_num_seqs':256,
        # 'disable_log_stats':False,
        # 'conv_template':None,
        # 'limit_worker_concurrency':5,
        # 'no_register':False,
        # 'num_gpus': 1
        # 'engine_use_ray': False,
        # 'disable_log_requests': False
    }

}
