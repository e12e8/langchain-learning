from typing import Dict, Any, List
from collections import defaultdict
from common_types import DecisionResult


class State:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.step_retry_counts = defaultdict(int)
        self.tool_stats = defaultdict(lambda: {"success": 0, "failure": 0})
        self.tool_experience_bias = defaultdict(float)
        self.step_results = {}

    def record_decision(self, step_id: str, decision: DecisionResult):
        self.history.append({
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
        })

    def record_step(self, step_id: str, tool: str, result: Dict[str, Any], reflection: Dict[str, Any]):
        self.history.append({
            "type": "execution",
            "step_id": step_id,
            "tool": tool,
            "result": result,
            "reflection": reflection,
        })

        if result.get("ok"):
            self.step_results[step_id] = result
            self.tool_stats[tool]["success"] += 1
            self.tool_experience_bias[tool] += 0.08
        else:
            self.tool_stats[tool]["failure"] += 1

        if reflection.get("should_retry"):
            self.step_retry_counts[step_id] += 1

    def get_last_decision(self, step_id: str):
        for item in reversed(self.history):
            if item["type"] == "decision" and item["step_id"] == step_id:
                return item["decision"]
        return None

    def snapshot(self) -> Dict[str, Any]:
        return {
            "history": self.history,
            "step_retry_counts": dict(self.step_retry_counts),
            "tool_stats": dict(self.tool_stats),
            "tool_experience_bias": dict(self.tool_experience_bias),
            "step_results": self.step_results,
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.snapshot()
