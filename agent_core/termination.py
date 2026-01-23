# termination.py
from typing import Dict, Any
from failure_guard import detect_no_progress
from state import State


def should_terminate(
    reflection: Dict[str, Any],
    state: State,
    current_step_idx: int,
    total_steps: int
) -> bool:
    # 1. 正常完成：最后一步成功
    if current_step_idx == total_steps - 1 and reflection.get("is_success"):
        return True

    # 2. 硬终止：单步重试过多
    if any(count >= 5 for count in state.step_retry_counts.values()):
        return True

    # 3. 软终止：无进展检测
    if detect_no_progress(state.to_dict()):
        return True

    return False
