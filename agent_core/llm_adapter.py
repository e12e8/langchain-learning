# llm_adapter.py - LLM适配器
import asyncio
from langchain_openai import ChatOpenAI
from typing import Any

class LLMAdapter:
    _instance = None  # 单例模式（可选，但推荐）

    def __new__(cls, *args, **kwargs):
        # 实现单例模式
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        model: str = "qwen-turbo",        # 模型名称
        temperature: float = 0.0,        # 温度参数
        api_key: str = "sk-4362e181dc44456fae7072e7eac4e970"  # API密钥
    ):
        # 防止重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
        # 初始化ChatOpenAI客户端
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 阿里云API地址
            api_key=api_key,
        )
        self._initialized = True

    async def ainvoke(self, prompt: str, **kwargs) -> str:
        # 获取事件循环
        loop = asyncio.get_event_loop()
        # 在线程池中执行同步调用
        response = await loop.run_in_executor(
            None,
            lambda: self.llm.invoke(prompt, **kwargs)  # 调用LLM
        )
        # 返回清理后的内容
        return response.content.strip()