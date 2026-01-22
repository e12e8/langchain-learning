# decision.py
from dataclasses import dataclass
from typing import Dict, Any, List
from tool_registry import list_tools
from llm_adapter import LLMAdapter
from state import State
from common_types import DecisionResult, ToolDecisionScore


# ────────────────────────────────────────────────
# 规则评分（强约束，优先级最高）
# ────────────────────────────────────────────────
def rule_score(tool: str, task: str) -> float:
    """
    显式规则判断工具是否适合任务
    """
    if tool == "calculator":
        # calculator 只适合数学任务
        return 1.0 if any(ch.isdigit() for ch in task) else 0.0

    if tool == "echo":
        # echo 作为兜底工具
        return 0.6

    return 0.3


# ────────────────────────────────────────────────
# 历史评分（来自 State 的成功率）
# ────────────────────────────────────────────────
def history_score(state: State, tool: str) -> float:
    stats = state.tool_stats.get(tool)
    if not stats:
        return 0.5  # 冷启动

    total = stats["success"] + stats["failure"]
    if total == 0:
        return 0.5

    return stats["success"] / total


# ────────────────────────────────────────────────
# LLM 评分（语义理解）
# ────────────────────────────────────────────────
def llm_score(task: str, tool: str) -> float:
    """
    让 LLM 给出 0~1 的适配度评分
    """
    llm = LLMAdapter()

    prompt = f"""
你是一个 Agent 的工具决策模块。

任务描述：
{task}

工具：
{tool}

请判断该工具是否适合完成任务。
只返回 0~1 之间的小数，不要解释。
"""

    try:
        text = llm.llm.invoke(prompt).content.strip()
        score = float(text)
        return max(0.0, min(score, 1.0))
    except Exception:
        return 0.5


# ────────────────────────────────────────────────
# ⭐ 核心：Decision 主函数（可解释）
# ────────────────────────────────────────────────
def decide(step, state: State) -> DecisionResult:
    """
    对所有工具进行评分，并返回完整决策轨迹
    """
    scores: List[ToolDecisionScore] = []

    for tool in list_tools():
        r = rule_score(tool, step.desc)
        h = history_score(state, tool)
        l = llm_score(step.desc, tool)

        final = 0.4 * r + 0.3 * h + 0.3 * l

        scores.append(
            ToolDecisionScore(
                tool_name=tool,
                rule_score=round(r, 2),
                history_score=round(h, 2),
                llm_score=round(l, 2),
                final_score=round(final, 2),
            )
        )

    # 选择最终得分最高的工具
    selected = max(scores, key=lambda x: x.final_score)

    return DecisionResult(
        selected_tool=selected.tool_name,
        final_score=selected.final_score,
        candidates=scores,
    )
