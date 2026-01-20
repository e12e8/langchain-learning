from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import datetime

# 加载环境变量配置
load_dotenv()

# 初始化大语言模型，配置相关参数
llm = ChatOpenAI(model="qwen-turbo",
                 temperature=0.2,
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                 api_key="sk-4362e181dc44456fae7072e7eac4e970"
                 )

# --------------定义第一个工具-----------------------------
@tool
def get_current_weekday() -> str:
    """获取今天是星期几（中文，例如：星期一）
    
    Returns:
        str: 当前日期对应的中文星期（如：星期一、星期二等）
    """
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    today = datetime.datetime.now().weekday()
    return weekdays[today]

@tool
def get_current_time()-> str:
    """获取当前时间
    
    Returns:
        str: 格式化的当前时间字符串，格式为 YYYY-MM-DD HH:MM:SS
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
# 打印工具信息
print("工具描述：", get_current_time.description)
print("工具参数：", get_current_time.args)

# 手动调用工具不经过模型
result = get_current_time.invoke({})
print("工具调用结果：", result)

# 将工具列表绑定到语言模型
tools = [get_current_time, get_current_weekday]
system_prompt = """
你是一个严格使用工具的助手。
规则：
1. 任何涉及当前时间、日期、星期几的问题，**必须**调用工具，**禁止**自己编造答案。
2. 得到工具结果后，**必须**完全使用工具结果，不要添加或修改任何数字/日期。
3. 如果问题不需要工具，直接回答。
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{query}")
])

llm_with_tools = prompt | llm.bind_tools(tools)

# 定义测试查询列表
queries=[
    "请使用工具告诉我现在北京的准确时间",
    "请使用工具告诉我今天是星期几",
    "请使用工具告诉我现在北京时间和今天星期几",
    "你是谁？",
    "请使用工具查询现在几点？今天星期几？",
]

# 遍历所有查询并处理工具调用
for query in queries:
    print("问题：", query)
    response = llm_with_tools.invoke(query)

    # 打印完整响应 看看有没有tool_calls
    print("模型原始回复：", response)

    # 检查是否有工具调用
    if response.tool_calls:
        print("模型决定调用工具！")
        tool_results = []

        for tool_call in response.tool_calls:
            name = tool_call["name"]
            args = tool_call["args"]
            print(f"  → 调用 {name}，参数：{args}")

            # 执行工具
            if name == "get_current_time":
                result = get_current_time.invoke(args)
            elif name == "get_current_weekday":
                result = get_current_weekday.invoke(args)
            else:
                result = "未知工具"

            print("  工具结果：", result)
            tool_results.append(f"{name} 返回：{result}")

        # 构建最终提示，将工具结果反馈给模型以生成自然回答
        final_prompt = f"""
        用户问题：{query}

        工具调用结果：
        {chr(10).join(tool_results)}

        【严格规则】
        - 你**必须**完全基于上面的工具结果回答，**禁止**使用任何其他知识或猜测。
        - 如果工具结果包含时间/日期/星期，请**一字不改**地使用它。
        - 不要说“我无法获取实时信息”，因为工具已经提供了。
        - 回答要简洁、自然、准确。

        现在请给出完整回答：
        """
        # 获取模型的最终响应
        final_response = llm.invoke(final_prompt)
        print("最终回答：", final_response.content)

    else:
        print("模型直接回答：", response.content)