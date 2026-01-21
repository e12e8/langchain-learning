from dataclasses import dataclass
from typing import List

@dataclass
class Step:
    id: str
    desc: str                    # 步骤描述
    max_retries: int = 1         # 每个 step 最多允许重试次数

def plan(task: str) -> List[Step]:
    # Week 1：最小规划，单步即可
    return [Step(id="step_1", desc=task)]