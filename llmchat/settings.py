import logging
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", "False") == "True"

# 是否显示详细日志
log_verbose = os.getenv("LOG_VERBOSE", "False") == "True"

# 日志格式
LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(format=LOG_FORMAT)

# 工程路径
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

# 日志存储路径
LOG_PATH = os.path.join(PROJECT_PATH, "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# httpx 请求默认超时时间（秒）。如果加载模型或对话较慢，出现超时错误，可以适当加大该值。
HTTPX_DEFAULT_TIMEOUT = 300.0

LLM_MODELS = [
    "qwen-api",
    "cyou-api",
]

# fastchat controller server
FSCHAT_CONTROLLER = {
    "host": os.getenv("FSCHAT_CONTROLLER_HOST", "0.0.0.0"),
    "port": int(os.getenv("FSCHAT_CONTROLLER_PORT", 20001)),
    "dispatch_method": "shortest_queue",
}

# fastchat openai_api server
FSCHAT_OPENAI_API = {
    "host": os.getenv("FSCHAT_OPENAI_API_HOST", "0.0.0.0"),
    "port": int(os.getenv("FSCHAT_OPENAI_API_PORT", 20000)),
}
