# day3_langgraph_agent.py - 使用 LangGraph 实现 ReAct 风格 Agent
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph import END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv
import os
import datetime
import operator

load_dotenv()

# LLM 配置
llm = ChatOpenAI(
    model="qwen-turbo",
    temperature=0.2,
    base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    api_key=os.getenv("DASHSCOPE_API_KEY", "sk-4362e181dc44456fae7072e7eac4e970"),
)


# 工具定义
@tool
def get_current_time() -> str:
    """获取当前北京时间，格式：YYYY-MM-DD HH:MM:SS"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_current_weekday() -> str:
    """获取今天是星期几，返回中文（如：星期二）"""
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[datetime.datetime.now().weekday()]


tools = [get_current_time, get_current_weekday]

# LLM 绑定工具  你现在有这两个技能可以用哦，什么时候需要就说一声。
llm_with_tools = llm.bind_tools(tools)


# State 定义（LangGraph 的核心：状态机）
class AgentState(TypedDict):
    messages: Annotated[List[AIMessage | HumanMessage], operator.add]
    # 可以加更多状态，如 intermediate_steps 等


# 节点 1: Agent 思考节点（决定 Action 或 Final Answer）
def agent_node(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# 节点 2: 工具执行节点
tool_node = ToolNode(tools)


# 条件边：模型是否要调用工具，还是结束
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


# 构建图
workflow = StateGraph(AgentState)

# 添加节点："agent"节点用于思考和决策，"tools"节点用于执行工具
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# 设置工作流入口点为"agent"节点
workflow.set_entry_point("agent")
# 添加条件边：根据should_continue函数的返回值决定流程走向
# 如果返回"tools"则转向工具节点，如果返回END则结束流程
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
# 添加从"tools"节点到"agent"节点的边，形成循环
workflow.add_edge("tools", "agent")

# 编译成可执行 Agent
app = workflow.compile()


# 测试函数
# 测试函数（修复版）
def run_agent(question: str):
    print("\n" + "=" * 60)
    print(f"问题：{question}")
    print("=" * 60 + "\n")

    inputs = {"messages": [HumanMessage(content=question)]}

    for event in app.stream(inputs):
        for value in event.values():
            if "messages" in value:
                last_msg = value["messages"][-1]
                print(
                    last_msg.content or f"[工具返回] {last_msg.content if hasattr(last_msg, 'content') else last_msg}")

                # 只在 AIMessage 时检查 tool_calls
                if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
                    print("调用工具：", last_msg.tool_calls)
                print("-" * 40)


# 测试问题
test_queries = [
    "请告诉我现在北京的准确时间",
    "今天是星期几？",
    "现在北京时间是几点？今天星期几？一起告诉我",
    "你是谁？",
    "现在几点？明天是星期几？",
]

for q in test_queries:
    run_agent(q)