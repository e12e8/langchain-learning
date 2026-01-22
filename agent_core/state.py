# state.py
from typing import Dict, Any, List
from collections import defaultdict
from common_types import DecisionResult


class State:
    """
    Agent 状态中心：
    - 决策轨迹（Decision Trace）
    - 执行历史
    - 工具成功率
    - 重试次数
    """

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.step_retry_counts = defaultdict(int)
        self.tool_stats = defaultdict(lambda: {"success": 0, "failure": 0})

    # ─────────────────────────────────────────
    # ⭐ 记录 Decision（Day 8 核心）
    # ─────────────────────────────────────────
    def record_decision(self, step_id: str, decision: DecisionResult):
        """
        记录一次完整的决策过程（可解释、可回放）
        """
        self.history.append(
            {
                "type": "decision",
                "step_id": step_id,
                "decision": {
                    "selected_tool": decision.selected_tool,
                    "final_score": decision.final_score,
                    "candidates": [
                        {
                            "tool": c.tool_name,
                            "rule_score": c.rule_score,
                            "history_score": c.history_score,
                            "llm_score": c.llm_score,
                            "final_score": c.final_score,
                        }
                        for c in decision.candidates
                    ],
                },
            }
        )

    # ─────────────────────────────────────────
    # 记录执行结果
    # ─────────────────────────────────────────
    def record_step(
        self,
        step_id: str,
        tool: str,
        result: Dict[str, Any],
        reflection: Dict[str, Any],
    ):
        self.history.append(
            {
                "type": "execution",
                "step_id": step_id,
                "tool": tool,
                "result": result,
                "reflection": reflection,
            }
        )

        if result.get("ok"):
            self.tool_stats[tool]["success"] += 1
        else:
            self.tool_stats[tool]["failure"] += 1

        if reflection.get("should_retry"):
            self.step_retry_counts[step_id] += 1

    # ─────────────────────────────────────────
    # 工具执行上下文
    # ─────────────────────────────────────────
    def build_context(self, step) -> Dict[str, Any]:
        return {
            "step_id": step.id,
            "step_desc": step.desc,
            "retry_count": self.step_retry_counts.get(step.id, 0),
            "state": self.snapshot(),
        }

    # ─────────────────────────────────────────
    # State 快照（只读）
    # ─────────────────────────────────────────
    def snapshot(self) -> Dict[str, Any]:
        return {
            "history": self.history,
            "step_retry_counts": dict(self.step_retry_counts),
            "tool_stats": dict(self.tool_stats),
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.snapshot()
