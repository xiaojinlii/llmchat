import importlib
import os
from typing import Literal

from llmchat.settings import PROJECT_PATH, logger, log_verbose


def detect_device() -> Literal["cuda", "mps", "cpu"]:
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
    except:
        pass
    return "cpu"


def llm_device(device: str = None) -> Literal["cuda", "mps", "cpu"]:
    device = device
    if device not in ["cuda", "mps", "cpu"]:
        device = detect_device()
    return device


def load_model_worker_config():
    config_path = os.path.join(PROJECT_PATH, "llmchat/model_worker_configs")

    configs = {}
    items = os.listdir(config_path)
    for item in items:
        if item.endswith('.py') and item not in ["example.py"]:
            case_name = item.replace('.py', '')
            mod = importlib.import_module(f'llmchat.model_worker_configs.{case_name}')
            cfg = mod.config
            configs[cfg["model_name"]] = cfg

    # for model_name, model_config in configs.items():
    #     print(f"{model_name}:{model_config}")

    return configs


def get_model_worker_config(model_name: str = None) -> dict:
    from llmchat import model_workers

    # ApiConfigParams.validate_config会传进来一个None，不知道为啥
    if model_name is None:
        return {}

    configs = load_model_worker_config()

    cfg = configs.get(model_name)
    base = cfg.get("base")

    config = {}
    config.update(cfg.get("base", {}))
    config.update(cfg.get("server", {}))
    if base["online_api"]:
        config.update(cfg.get("online_model", {}))
        if provider := config.get("provider"):
            try:
                config["worker_class"] = getattr(model_workers, provider)
            except Exception as e:
                msg = f"在线模型 ‘{model_name}’ 的provider没有正确配置"
                logger.error(f'{e.__class__.__name__}: {msg}',
                             exc_info=e if log_verbose else None)
    else:
        config.update(cfg.get("offline_model", {}))
        path = config["model_path"]
        if path and os.path.isdir(path):
            config["model_path_exists"] = True
        config["device"] = llm_device(config.get("device"))

        if base["vllm_enabled"]:
            config.update(cfg.get("vllm", {}))

    return config
