from typing import List
from common_types import DecisionResult, ToolCandidate
from state import State


def decide(step, state: State) -> DecisionResult:
    """
    根据规则 + 历史 + 经验偏置，选择最合适的工具
    """

    candidates: List[ToolCandidate] = []

    # === 规则层（rule-based） ===
    if "计算" in step.desc:
        tool_rules = {
            "calculator": 1.0,
            "echo": 0.6,
        }
    else:
        tool_rules = {
            "echo": 0.8,
            "calculator": 0.3,
        }

    # === 打分融合 ===
    for tool, rule_score in tool_rules.items():
        history = state.tool_stats[tool]
        history_score = (
            history["success"] / (history["success"] + history["failure"])
            if history["success"] + history["failure"] > 0
            else 0.5
        )

        llm_score = rule_score  # 当前阶段先简化
        bias = state.tool_experience_bias[tool]

        final = round(
            0.5 * rule_score +
            0.3 * history_score +
            0.2 * llm_score +
            bias,
            2
        )

        candidates.append(
            ToolCandidate(
                tool_name=tool,
                rule_score=rule_score,
                history_score=history_score,
                llm_score=llm_score,
                final_score=final,
            )
        )

    # === 选择得分最高的工具 ===
    candidates.sort(key=lambda x: x.final_score, reverse=True)
    selected = candidates[0]

    return DecisionResult(
        selected_tool=selected.tool_name,
        final_score=selected.final_score,
        candidates=candidates,
    )
