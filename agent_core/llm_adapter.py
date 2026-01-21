# llm_adapter.py
import asyncio
from langchain_openai import ChatOpenAI
from typing import Any

class LLMAdapter:
    _instance = None  # 单例模式（可选，但推荐）

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        model: str = "qwen-turbo",
        temperature: float = 0.0,
        api_key: str = "sk-4362e181dc44456fae7072e7eac4e970"
    ):
        # 防止重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=api_key,
        )
        self._initialized = True

    async def ainvoke(self, prompt: str, **kwargs) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.llm.invoke(prompt, **kwargs)
        )
        return response.content.strip()