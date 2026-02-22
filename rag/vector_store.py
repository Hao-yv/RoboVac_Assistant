"""
@Time    : 2026/2/22 08:41
@Author  : Zhang Hao yv
@File    : vector_store.py
@IDE     : PyCharm
"""
import os

from langchain_chroma import Chroma
from langchain_core.documents import Document

from Utils.config_handler import chroma_config
from Utils.logger_handler import logger
from Utils.path_tool import get_abs_path
from Utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from langchain_text_splitters import RecursiveCharacterTextSplitter

from model.factory import embedding_model

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_config["persist_directory"]
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为内存存入向量库
        要计算文件MD5去重
        :return:
        """
        def check_md5_hex(md5_for_hex: str):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]), "w", encoding='utf-8').close()
                return False # MD5没处理过

            with open(get_abs_path(chroma_config["md5_hex_store"]), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_hex:
                        return True # MD5处理过
                return False # MD5没处理过

        def save_md5_hex(md5_for_hex: str):
            with open(get_abs_path(chroma_config["md5_hex_store"]), 'a', encoding='utf-8') as f:
                f.write(md5_for_hex + '\n')

        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            elif read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            else:
                return []

        allowed_file_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"]),
        )
        for file_path in allowed_file_path:
            # 获取文件MD5
            md5_hex = get_file_md5_hex(file_path)
            if md5_hex is None:
                logger.warning(f"[加载知识库] {file_path} 无法计算MD5，跳过")
                continue
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库] {file_path}内容已经存在于知识库，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(file_path)
                if not documents:
                    logger.warning(f"[加载知识库] {file_path} 文件内没有有效文本内容，跳过")
                    continue
                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库] {file_path} 分片后没有有效文本内容，跳过")
                    continue

                #     将内容存入向量库
                self.vector_store.add_documents(split_document)
                #     记录已经处理好的MD5,避免下次加载重复
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库] {file_path} 内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库] {file_path} 加载失败: {str(e)}", exc_info=True)
                continue

if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for doc in res:
        print(doc.page_content)
        print("_"*20)
