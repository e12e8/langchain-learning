# main.py
import asyncio                    # 异步执行库
from agent import run_agent       # 导入智能体运行函数

if __name__ == "__main__":
    result = asyncio.run(         # 异步运行智能体
        run_agent("测试一下最小 Agent")  # 执行测试任务
    )
    print(result)                 # 输出结果