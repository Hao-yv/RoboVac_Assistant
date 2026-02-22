"""
@Time    : 2026/2/22 20:48
@Author  : Zhang Hao yv
@File    : app.py
@IDE     : PyCharm
"""
import streamlit as st
from agent.react_agent import ReactAgent
import time

# 页面配置：宽屏、标题、图标
st.set_page_config(
    page_title="扫地机器人智能客服",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自定义样式：简洁现代 + 流式输出优化
st.markdown("""
<style>
    /* 主容器 */
    .stApp { background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%); }
    
    /* 标题区 */
    .main-header {
        text-align: center;
        padding: 1.5rem 0 2rem;
        border-bottom: 1px solid rgba(0,0,0,0.06);
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        font-size: 1.85rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: #64748b;
        font-size: 0.95rem;
        margin: 0.5rem 0 0;
    }
    
    /* 聊天消息气泡 */
    [data-testid="stChatMessage"] {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    
    /* 流式输出文字样式优化 */
    .stMarkdown p {
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* 打字机光标效果 */
    .streaming-cursor::after {
        content: '|';
        animation: blink 1s step-end infinite;
        color: #3b82f6;
        margin-left: 2px;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    /* 流式输出容器 */
    .streaming-container {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 输入框容器 */
    .stChatInputContainer {
        padding: 1rem 0 1.5rem;
    }
    
    /* 侧边栏（若启用）- 重点调整部分 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        color: #e2e8f0;
    }
    
    /* 侧边栏内的 Markdown 文本颜色优化 */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span {
        color: #cbd5e1 !important;
    }
    
    /* 侧边栏标题加亮 */
    [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        font-weight: 600;
    }

    /* 侧边栏按钮样式优化：适配深色背景 */
    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent;
        color: #e2e8f0 !important;
        border: 1px solid #475569;
        border-radius: 8px;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.1);
        color: #fff !important;
        border-color: #94a3b8;
    }
    
    /* 侧边栏分割线颜色调整 */
    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }
    
    /* Markdown 内容样式 */
    .stMarkdown code {
        background-color: #f1f5f9;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9em;
    }
    
    .stMarkdown pre {
        background-color: #1e293b;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# 标题区
st.markdown(
    '<div class="main-header">'
    '<h1>🤖 扫地机器人智能客服</h1>'
    '<p>支持产品咨询、使用建议、故障排除、保养指南与个人使用报告生成</p>'
    '</div>',
    unsafe_allow_html=True,
)

# 初始化 agent（放 cache 里避免每次重载）
@st.cache_resource
def get_agent():
    return ReactAgent()

# 会话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏：清空对话与说明
with st.sidebar:
    st.markdown("### ⚙️ 对话")
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("**💡 可尝试：**")
    st.markdown("- 小户型适合哪些扫地机器人？")
    st.markdown("- 扫地机器人如何保养？")
    st.markdown("- 给我生成使用报告")

# 展示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# 流式输出包装函数 - 优化文字显示效果
def stream_with_formatting(generator):
    """包装生成器，使流式输出更加平滑"""
    for chunk in generator:
        if chunk:
            # 逐字输出，增加平滑度
            yield chunk
            time.sleep(0.01)

# 用户输入
if prompt := st.chat_input("输入您的问题，例如：小户型适合哪些扫地机器人？"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        agent = get_agent()
        # 使用流式输出，文字会以打字机效果显示 [[3]]
        full_response = st.write_stream(stream_with_formatting(agent.execute_stream(prompt)))
        st.session_state.messages.append({"role": "assistant", "content": full_response})