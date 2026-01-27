from typing import List
from common_types import DecisionResult, ToolCandidate
from state import State


def decide(step, state: State) -> DecisionResult:
    """
    根据规则 + 历史 + 经验偏置，选择最合适的工具
    """

    candidates: List[ToolCandidate] = []

    desc = step.desc

    # === 规则层：加入知识库检索的判断 ===
    if "计算" in desc:
        tool_rules = {"calculator": 1.0, "echo": 0.2, "knowledge": 0.1}
    elif any(kw in desc for kw in ["检索", "知识库", "查询", "谁是"]):
        tool_rules = {"knowledge": 1.0, "echo": 0.4, "calculator": 0.1}
    else:
        tool_rules = {"echo": 0.8, "knowledge": 0.2, "calculator": 0.1}

    # === 打分融合 ===
    for tool, rule_score in tool_rules.items():
        history = state.tool_stats[tool]
        history_score = (
            history["success"] / (history["success"] + history["failure"])
            if history["success"] + history["failure"] > 0
            else 0.5
        )

        llm_score = rule_score
        bias = state.tool_experience_bias.get(tool, 0.0)

        final = round(0.5 * rule_score + 0.3 * history_score + 0.2 * llm_score + bias, 2)

        candidates.append(ToolCandidate(tool, rule_score, history_score, llm_score, final))

    # === 选择得分最高的工具 ===
    candidates.sort(key=lambda x: x.final_score, reverse=True)
    selected = candidates[0]

    return DecisionResult(
        selected_tool=selected.tool_name,
        final_score=selected.final_score,
        candidates=candidates,
    )
