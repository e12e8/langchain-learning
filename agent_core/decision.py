# decision.py
from dataclasses import dataclass
from typing import Dict, Any
from tool_registry import list_tools
from llm_adapter import LLMAdapter
from state import State

# ────────────────────────────────────────────────
# Decision 结果结构
# ────────────────────────────────────────────────
@dataclass
class DecisionResult:
    tool_name: str
    score: float
    reason: Dict[str, Any]


# ────────────────────────────────────────────────
# 规则评分（强约束，最重要）
# ────────────────────────────────────────────────
def rule_score(tool: str, task: str) -> float:
    """
    基于显式规则判断 tool 是否适合当前任务
    """
    if tool == "calculator":
        # calculator 只适合数学表达式
        has_digit = any(ch.isdigit() for ch in task)
        return 1.0 if has_digit else 0.0

    if tool == "echo":
        # echo 是兜底工具
        return 0.6

    return 0.3


# ────────────────────────────────────────────────
# 历史评分（来自 State）
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
    让 LLM 给一个 0~1 的适配度分数
    """
    llm = LLMAdapter()

    prompt = f"""
你是一个 Agent 的决策评分模块。
任务是：{task}

工具：{tool}

请判断这个工具是否适合完成该任务。
只返回 0 到 1 之间的小数，不要解释。
"""

    try:
        score_text = llm.llm.invoke(prompt).content.strip()
        score = float(score_text)
        return max(0.0, min(score, 1.0))
    except Exception:
        return 0.5


# ────────────────────────────────────────────────
# 核心：Decision 主函数
# ────────────────────────────────────────────────
def decide(step, state: State) -> DecisionResult:
    candidates = list_tools()
    best: DecisionResult | None = None

    for tool in candidates:
        r_score = rule_score(tool, step.desc)
        h_score = history_score(state, tool)
        l_score = llm_score(step.desc, tool)

        final = (
            0.4 * r_score +
            0.3 * h_score +
            0.3 * l_score
        )

        detail = {
            "rule_score": round(r_score, 2),
            "history_score": round(h_score, 2),
            "llm_score": round(l_score, 2),
            "final_score": round(final, 2)
        }

        if best is None or final > best.score:
            best = DecisionResult(
                tool_name=tool,
                score=final,
                reason=detail
            )

    return best
