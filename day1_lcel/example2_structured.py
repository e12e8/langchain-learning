from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import BaseModel, Field

# 定义想要的输出结构（Pydantic 模型）
class JokeResponse(BaseModel):
    setup: str = Field(description="笑话的前半段铺垫")
    punchline: str = Field(description="笑话的包袱/笑点")

# Prompt
prompt = ChatPromptTemplate.from_template(
    "讲一个关于 {topic} 的程序员笑话，用中文。"
)

# LLM
llm = ChatOpenAI(model="qwen-turbo", temperature=0.9, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", api_key="sk-4362e181dc44456fae7072e7eac4e970")

# Parser（直接解析成 Pydantic 对象）
parser = StrOutputParser()

# 链
chain = prompt | llm | parser

# 调用
result = chain.invoke({"topic": "debug"})
print(result)
# 输出类似：{'setup': '...', 'punchline': '...'}