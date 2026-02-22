"""
@Time    : 2026/2/22 20:17
@Author  : Zhang Hao yv
@File    : react_agent.py
@IDE     : PyCharm
"""
from langchain.agents import create_agent

from Utils.prompt_loader import load_system_prompts
from model.factory import chat_model
from agent.tools.agent_tools import (rag_summarize_service, get_weather, get_user_location, get_user_id,
                                     get_current_month, fetch_external_data, fill_context_for_report)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize_service, get_weather, get_user_location, get_user_id,
                   get_current_month, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        # 第三个参数context就是上下文, 就说=是提示词切换的标记
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report_prompt": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + '\n'

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("给我生成使用报告"):
        print(chunk, end='', flush=True)
