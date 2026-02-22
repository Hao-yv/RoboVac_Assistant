"""
@Time    : 2026/2/22 19:40
@Author  : Zhang Hao yv
@File    : middleware.py
@IDE     : PyCharm
"""
from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime

from langgraph.types import Command

from Utils.logger_handler import logger
from Utils.prompt_loader import load_system_prompts, load_report_prompts

# 工具执行监控
@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    tool_name = request.tool_call['name']
    logger.info(f" [monitor_tool] 执行工具: {tool_name} ")
    logger.info(f" [monitor_tool] 传入工具: {request.tool_call['args']} ")

    try:
        result = handler(request)
        logger.info(f" 【monitor_tool】工具调用成功")

        # 使用 request 中的工具名称，而不是 result（ToolMessage 没有 tool_call 属性）
        if tool_name == "fill_context_for_report":
            request.runtime.context['report'] = True

        return result
    except Exception as e:
        logger.error(f"工具 {tool_name} 调用失败，原因：{str(e)}", exc_info=True)
        raise e

# 在模型执行前输出日志
@before_model
def log_before_model(
        state: AgentState,  # 整个智能体中的状态注入
        runtime: Runtime    # 记录整个智能体中的状态信息
):
    messages = state.get("messages", [])
    logger.info(f"【log_before_model】即将调用模型，带有{len(messages)}条消息")
    if messages:
        last = messages[-1]
        content = getattr(last, "content", None) or ""
        logger.debug(f"【log_before_model】{type(last).__name__} | {(content if isinstance(content, str) else str(content))[:200]}")
    return None

# 动态切换提示词
@dynamic_prompt # 每一次生成提示词之前调用此函数
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get('report', False)
    if is_report: # 是报告生成场景,返回报告生成提示词内容
        return load_report_prompts()
    else: return load_system_prompts()