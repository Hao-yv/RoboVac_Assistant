"""
@Time    : 2026/2/22 09:08
@Author  : Zhang Hao yv
@File    : factory.py
@IDE     : PyCharm
"""
from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings

from Utils.config_handler import rag_config
from Utils.logger_handler import logger


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> BaseChatModel | Embeddings:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> BaseChatModel:
        # LangChain 会自动从环境变量 OPENAI_API_KEY 和 OPENAI_BASE_URL 读取
        return ChatOpenAI(
            model=rag_config["OPENAI_MODEL_NAME"],
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Embeddings:
        # LangChain 会自动从环境变量 OPENAI_API_KEY 和 OPENAI_BASE_URL 读取
        model_name = rag_config.get("EMBEDDING_MODEL_NAME", "text-embedding-ada-002")
        logger.info(f"初始化 OpenAIEmbeddings，模型: {model_name}")
        
        return OpenAIEmbeddings(
            model=model_name,
        )


def get_chat_model() -> BaseChatModel:
    return ChatModelFactory().generator()


def get_embedding_model() -> Embeddings:
    return EmbeddingsFactory().generator()

# 文件底部直接实例化，模块被导入时就会立即执行，若配置未就绪会报错
chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingsFactory().generator()