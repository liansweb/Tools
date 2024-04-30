import logging
from config import LOG_LEVEL

def log_config(level):
    if level == "DEBUG":
        # 配置日志记录的基本设置
        logging.basicConfig(
            level=getattr(logging,level),
            format=f'%(asctime)s - %(levelname)s - [%(pathname)s:%(lineno)d] - %(module)s - %(funcName)s - %(lineno)s - %(message)s'
        )
    elif level == "INFO":
        # 配置日志记录的基本设置
        logging.basicConfig(
            level=getattr(logging,level),
            format=f'%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s'
        )
    else:
        level = "INFO"
        logging.basicConfig(
            level=getattr(logging,level),
            format=f'%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s'
        )
    # 创建 Logger 实例  
    logger = logging.getLogger(__name__)
    return logger

logger = log_config(level=LOG_LEVEL)