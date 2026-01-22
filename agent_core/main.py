# main.py - 智能体系统主入口
import asyncio                   # 异步执行库
from agent import run_agent      # 导入智能体运行函数


if __name__ == "__main__":
    # 运行智能体执行指定任务
    result = asyncio.run(run_agent("计算 17 * 23，然后把结果乘以 5"))
    print(result)                  # 输出执行结果