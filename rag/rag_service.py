"""
@Time    : 2026/2/22 15:57
@Author  : Zhang Hao yv
@File    : rag_service.py
@IDE     : PyCharm
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from Utils.prompt_loader import load_rag_prompts
from rag.vector_store import VectorStoreService
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model

"""
    总结服务类：用户提问，搜索参考资料，将提问和参考资料交给模型，让模型总结回复
"""
class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(prompt_text)
        self.model = chat_model
        self.chain = self.__init_chain()

    def __init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】：参考资料：{doc.page_content} | 参考源数据：{doc.metadata}\n"

        return self.chain.invoke(
            {
                "input": query,
                "context": context
             }
        )



if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize("小户型适合那些扫地机器人"))

