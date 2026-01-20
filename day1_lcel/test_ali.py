# test_ali.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # 如果你用 .env 文件放 key

# 推荐写法：直接传参（最清晰，不依赖环境变量顺序）
llm = ChatOpenAI(
    model="qwen-turbo",                  # 或 qwen-plus / qwen-max 如果额度够
    temperature=0.3,                     # 稍微低一点，输出更稳定
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-4362e181dc44456fae7072e7eac4e970",   # 你的 key
    max_tokens=512,
)

# 最简单的测试
response = llm.invoke("用一句话告诉我 LangChain 现在最核心的概念是什么？")
print(response.content)