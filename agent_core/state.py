# state.py - 状态管理模块
from typing import Dict, Any, List
from collections import defaultdict
from common_types import DecisionResult  # 导入决策结果类型


class State:
    """Agent 全局状态中心，所有记忆和统计集中在此"""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []                     # 执行轨迹（决策+执行）
        self.step_retry_counts = defaultdict(int)                   # 每步重试次数
        self.tool_stats = defaultdict(lambda: {"success": 0, "failure": 0})  # 工具成功/失败统计
        self.tool_experience_bias = defaultdict(float)              # 经验偏置（-0.4 ~ +0.4）
        self.step_results = {}                                      # 新增：跨步结果缓存（step_id → result）

    def record_decision(self, step_id: str, decision: DecisionResult):
        """记录完整决策轨迹（可解释性核心）"""
        self.history.append(
            {
                "type": "decision",
                "step_id": step_id,
                "decision": {
                    "selected_tool": decision.selected_tool,         # 记录选中的工具
                    "final_score": decision.final_score,           # 记录最终得分
                    "candidates": [                               # 记录所有候选工具评分
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

    def record_step(self, step_id: str, tool: str, result: Dict[str, Any], reflection: Dict[str, Any]):
        """记录单步执行 + 反思结果，并更新统计与经验偏置"""
        self.history.append(
            {
                "type": "execution",
                "step_id": step_id,
                "tool": tool,                                        # 记录使用的工具
                "result": result,                                  # 记录执行结果
                "reflection": reflection,                          # 记录反思结果
            }
        )

        # 新增：缓存结果
        if result.get("ok"):
            self.step_results[step_id] = result

        if result.get("ok"):
            self.tool_stats[tool]["success"] += 1                 # 更新成功统计
        else:
            self.tool_stats[tool]["failure"] += 1               # 更新失败统计

        if reflection.get("should_retry"):
            self.step_retry_counts[step_id] += 1                  # 更新重试次数

        # 经验学习：失败惩罚 + 成功微弱加成
        severity = reflection.get("failure_severity", 0.0)
        if severity > 0:
            penalty = -0.25 * severity
            self.tool_experience_bias[tool] += penalty
            self.tool_experience_bias[tool] = max(-0.4, min(0.4, self.tool_experience_bias[tool]))
        elif reflection.get("is_success"):
            self.tool_experience_bias[tool] += 0.08               # 成功微弱加成
            self.tool_experience_bias[tool] = min(0.4, self.tool_experience_bias[tool])

    def build_context(self, step) -> Dict[str, Any]:
        """为工具准备当前上下文（只读快照）"""
        return {
            "step_id": step.id,                                   # 步骤ID
            "step_desc": step.desc,                                # 步骤描述
            "retry_count": self.step_retry_counts.get(step.id, 0),  # 重试次数
            "previous_results": list(self.step_results.values())[-2:],  # 最近 2 步结果
            "state": self.snapshot(),                             # 当前状态快照
        }

    def snapshot(self) -> Dict[str, Any]:
        """返回当前状态的只读快照，防止外部修改"""
        return {
            "history": self.history,                              # 历史记录
            "step_retry_counts": dict(self.step_retry_counts),    # 步骤重试计数
            "tool_stats": dict(self.tool_stats),                  # 工具统计
            "tool_experience_bias": dict(self.tool_experience_bias),  # 经验偏置
            "step_results": self.step_results,                    # 步骤结果缓存
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.snapshot()