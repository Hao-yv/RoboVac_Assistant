"""
@Time    : 2026/2/21 19:39
@Author  : Zhang Hao yv
@File    : file_handler.py
@IDE     : PyCharm
"""
import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from Utils.logger_handler import logger


def get_file_md5_hex(file_path: str):
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件{file_path}不存在")
        return None

    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]路径{file_path}不是文件")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 4096  # 4KB分片，防止爆内存
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):  # 修复：新变量 chunk 接收读取结果
                md5_obj.update(chunk)
        return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"计算文件{file_path}md5失败，{str(e)}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]) -> list[str]:
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path} 不是文件夹")
        return files  # 修复：返回空列表而非 allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return files


def pdf_loader(file_path: str, passwd=None) -> list[Document]:
    return PyPDFLoader(file_path, passwd).load()


def txt_loader(file_path: str) -> list[Document]:
    return TextLoader(file_path, autodetect_encoding=True).load()  # 自动检测编码更健壮