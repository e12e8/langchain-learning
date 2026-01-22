# termination.py - 终止条件判断模块
from typing import Dict, Any
from state import State              # 导入状态管理


def should_terminate(
    reflection: Dict[str, Any],     # 反思结果
    state: State,                    # 当前状态
    current_step_idx: int,          # 当前步骤索引
    total_steps: int                # 总步骤数
) -> bool:
    """判断是否应该结束整个 Agent 运行"""
    # 最后一步成功 → 正常结束
    if reflection.get("is_success", False) and current_step_idx == total_steps - 1:
        return True

    # 硬终止：某步连续失败过多
    if any(count > 5 for count in state.step_retry_counts.values()):
        return True

    # 可扩展：token 预算、时间预算、无进展检测等
    return False