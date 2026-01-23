# failure_guard.py
from typing import Dict, Any


def detect_no_progress(state: Dict[str, Any], window: int = 3) -> bool:
    """
    检测最近 N 步是否没有有效进展
    """
    recent = state["history"][-window * 2:]  # decision + execution

    successful_steps = [
        h for h in recent
        if h["type"] == "execution" and h["result"].get("ok")
    ]

    # 没有任何成功结果
    return len(successful_steps) == 0
