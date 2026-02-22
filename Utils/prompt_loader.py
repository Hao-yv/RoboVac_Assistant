"""
@Time    : 2026/2/21 20:53
@Author  : Zhang Hao yv
@File    : prompt_loader.py
@IDE     : PyCharm
"""

from Utils.path_tool import get_abs_path
from Utils.logger_handler import logger
from Utils.config_handler import prompts_config

def load_system_prompts():
    try:
        prompt_path = prompts_config.get("main_prompt_path")
        if not prompt_path:
            raise KeyError("main_prompt_path")
        system_prompt_path = get_abs_path(prompt_path)
    except KeyError as e:
        logger.error("[load_system_prompts]在yaml配置项中没有main_prompt_path配置项")
        raise e

    try:
        return open(system_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_system_prompts]读取系统提示词出错: {str(e)}", exc_info=True)
        raise e

def load_rag_prompts():
    try:
        prompt_path = prompts_config.get("rag_prompt_path")
        if not prompt_path:
            raise KeyError("rag_prompt_path")
        rag_prompt_path = get_abs_path(prompt_path)
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置项中没有rag_prompt_path配置项")
        raise e

    try:
        return open(rag_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]读取系统提示词出错: {str(e)}", exc_info=True)
        raise e

def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_config["report_prompt_path"])
    except KeyError as e:
        logger.error("[load_report_prompts] 在yaml配置项中没有report_prompt_path配置项")
        raise e

    try:
        return open(report_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_report_prompts] 解析报告生成提示词出错: {str(e)}", exc_info=True)
        raise e
