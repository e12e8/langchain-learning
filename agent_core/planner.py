# planner.py - 任务规划模块
from dataclasses import dataclass
from typing import List


@dataclass
class Step:
    id: str
    desc: str                       # 步骤描述
    max_retries: int = 2            # 最大重试次数


def plan(task: str) -> List[Step]:
    """简单任务拆解（未来可换 LLM 规划）"""
    # 临时优化：step_2 只放纯任务，避免中文干扰
    return [
        Step(id="step_1", desc=f"理解任务: {task}", max_retries=1),  # 去冒号
        Step(id="step_2", desc=task, max_retries=3),  # 纯 task "计算 17 * 23，然后把结果乘以 5"
        Step(id="step_3", desc="整理结果并输出最终答案", max_retries=1),
    ]