from dataclasses import dataclass
from typing import List

@dataclass
class Step:
    id: str
    desc: str
    max_retries: int = 1

def plan(task: str) -> List[Step]:
    return [Step(id="step_1", desc=task)]
