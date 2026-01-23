import asyncio
from agent import run_agent
from replay import replay
async def main():
    task = "计算 1999 + 1996 并整理输出"
    result = await run_agent(task)
    print(f"状态: {result.status}")
    print(f"回答: {result.result['answer']}")
    print(f"工具学习累积: {result.state['tool_experience_bias']}")
    print("====== AGENT REPLAY ======")
    print(replay(result.state["history"]))
if __name__ == "__main__":
    # 启动异步主程序
    asyncio.run(main())