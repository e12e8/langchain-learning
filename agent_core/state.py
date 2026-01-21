# state.py
from typing import Dict, Any, List
from collections import defaultdict


class State:
    """
    Agent 状态中心：
    - 记录执行历史
    - 统计工具成功率
    - 记录 step 的 retry 次数
    """

    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.step_retry_counts: Dict[str, int] = defaultdict(int)
        self.tool_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"success": 0, "failure": 0}
        )

    # ─────────────────────────────────────────
    # 记录一次执行结果（唯一写入口）
    # ─────────────────────────────────────────
    def record(
        self,
        step_id: str,
        tool: str,
        result: Dict[str, Any],
        reflection: Dict[str, Any],
    ):
        self.history.append(
            {
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
    # 查询接口（Decision / Agent 使用）
    # ─────────────────────────────────────────
    def get_retry_count(self, step_id: str) -> int:
        return self.step_retry_counts.get(step_id, 0)

    def get_tool_score(self, tool_name: str) -> float:
        stats = self.tool_stats.get(tool_name)
        if not stats:
            return 0.5  # 未使用过的工具，中立分
        total = stats["success"] + stats["failure"]
        if total == 0:
            return 0.5
        return stats["success"] / total

    def has_success(self, step_id: str) -> bool:
        for h in self.history:
            if h["step_id"] == step_id and h["reflection"].get("is_success"):
                return True
        return False
    # ─────────────────────────────────────────
    # 构造工具执行上下文（Agent / Tool 唯一入口）
    # ─────────────────────────────────────────
    def build_context(self, step) -> Dict[str, Any]:
        """
        为工具构造统一上下文
        """
        return {
            "step_id": step.id,
            "step_desc": step.desc,
            "retry_count": self.get_retry_count(step.id),
            "state": self.snapshot(),  # 只读快照
        }
    # ─────────────────────────────────────────
    # 语义化封装：供 Agent 主循环调用
    # ─────────────────────────────────────────
    def record_step(
        self,
        step_id: str,
        tool: str,
        result: Dict[str, Any],
        reflection: Dict[str, Any],
    ):
        """
        Agent 主循环专用接口（语义更清晰）
        """
        self.record(
            step_id=step_id,
            tool=tool,
            result=result,
            reflection=reflection,
        )

    # ─────────────────────────────────────────
    # ⭐ 核心：对外快照接口（agent.py 用的）
    # ─────────────────────────────────────────
    def snapshot(self) -> Dict[str, Any]:
        """
        返回当前 State 的只读快照
        """
        return {
            "history": self.history,
            "step_retry_counts": dict(self.step_retry_counts),
            "tool_stats": dict(self.tool_stats),
        }

    def last_success_result(self) -> Dict[str, Any]:
        """
        获取最后一次成功的执行结果
        """
        for item in reversed(self.history):
            if item.get("result", {}).get("ok"):
                return item["result"]
        return {}

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式（兼容旧版本）
        """
        return self.snapshot()
