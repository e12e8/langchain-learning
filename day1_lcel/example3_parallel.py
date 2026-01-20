from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="qwen-turbo",
                 temperature=0.9,
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                 api_key="sk-4362e181dc44456fae7072e7eac4e970"
                 )

# 两个并行的 prompt
joke_prompt = ChatPromptTemplate.from_template("讲一个关于 {topic} 的冷笑话，越冷越好。")
poem_prompt = ChatPromptTemplate.from_template("写一首关于 {topic} 的四行小诗。")

# 并行执行
parallel = RunnableParallel(
    joke = joke_prompt | llm | StrOutputParser(),
    poem = poem_prompt | llm | StrOutputParser()
)

# 最后再总结
summary_prompt = ChatPromptTemplate.from_template(
    "根据下面两种创作，总结一句话关于 {topic} 的感觉：\n笑话：{joke}\n诗：{poem}"
)
summary_chain = summary_prompt | llm | StrOutputParser()

# 完整链：输入 → 并行 → 合并 → 总结
# 保留 topic 不被覆盖
full_chain = RunnableParallel(
    topic = RunnablePassthrough(),          # 显式保留原始 topic
    joke  = joke_prompt | llm | StrOutputParser(),
    poem  = poem_prompt | llm | StrOutputParser()
) | summary_chain

# 运行
print(full_chain.invoke("程序员学langchain 学到崩溃"))