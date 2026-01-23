import asyncio
from langchain_openai import ChatOpenAI

class LLMAdapter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model: str = "qwen-turbo", temperature: float = 0.0, api_key: str = "你的API_KEY"):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key="sk-4362e181dc44456fae7072e7eac4e970",
        )
        self._initialized = True

    async def ainvoke(self, prompt: str) -> str:
        # 直接使用 LangChain 提供的异步接口
        response = await self.llm.ainvoke(prompt)
        return response.content