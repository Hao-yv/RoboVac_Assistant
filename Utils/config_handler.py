"""
@Time    : 2026/2/21 19:08
@Author  : Zhang Hao yv
@File    : config_handler.py
@IDE     : PyCharm
"""
import os
import yaml
from dotenv import load_dotenv
from Utils.path_tool import get_abs_path

def load_rag_config(env_path: str = None):
    """
    从 .env 文件加载 RAG 相关配置
    返回字典格式，保持与原有接口兼容
    
    Args:
        env_path: .env 文件路径，默认为项目根目录下的 .env
        
    Returns:
        dict: RAG 配置字典
    """
    if env_path is None:
        env_path = get_abs_path(".env")
    
    # 加载 .env 文件到环境变量（如果文件不存在也不会报错）
    load_dotenv(env_path, override=False)
    
    # 从环境变量构建配置字典
    rag_config = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", ""),
        "OPENAI_API_BASE": os.getenv("OPENAI_API_BASE", os.getenv("OPENAI_BASE_URL", "")),  # 兼容旧配置名
        "OPENAI_MODEL_NAME": os.getenv("OPENAI_MODEL_NAME", ""),
        "EMBEDDING_MODEL_NAME": os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-ada-002"),
    }
    
    return rag_config

def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载配置
# rag_config 从 .env 文件读取（包含敏感信息如 API key）
rag_config = load_rag_config()
# 其他配置从 yml 文件读取（非敏感配置）
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
agent_config = load_agent_config()

# 自动将 rag_config 中的标准环境变量名配置项设置到环境变量
# LangChain 会自动读取这些环境变量，无需在代码中显式传递
# 标准环境变量名列表（LangChain 默认支持）
STANDARD_ENV_VARS = [
    "OPENAI_API_KEY",
    "OPENAI_BASE_URL",
    "OPENAI_API_BASE",  # 兼容旧配置名
    "DASHSCOPE_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    # 可以继续添加其他标准环境变量名
]

for env_var in STANDARD_ENV_VARS:
    # 如果环境变量不存在，且 rag_config 中存在对应键，则设置到环境变量
    if env_var not in os.environ:
        config_value = rag_config.get(env_var)
        if config_value:
            os.environ[env_var] = str(config_value)

# 兼容旧配置名 OPENAI_API_BASE -> OPENAI_BASE_URL
if "OPENAI_BASE_URL" not in os.environ and rag_config.get("OPENAI_API_BASE"):
    os.environ["OPENAI_BASE_URL"] = rag_config["OPENAI_API_BASE"]

if __name__ == '__main__':
    print(rag_config["OPENAI_MODEL_NAME"])

