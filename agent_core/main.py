import asyncio
from agent import run_agent
from replay import replay
async def main():
    # 故意问得模糊一点，测试向量检索的语义理解能力
    task = "第一周学习计划是什么？"
    result = await run_agent(task)
    print(f"状态: {result.status}")
    print(f"回答: {result.result['answer']}")
    print(f"工具学习累积: {result.state['tool_experience_bias']}")
    print("====== AGENT REPLAY ======")
    print(replay(result.state["history"]))
if __name__ == "__main__":
    # 启动异步主程序
    asyncio.run(main())