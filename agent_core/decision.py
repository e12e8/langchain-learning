# decision.py - 决策模块
from dataclasses import dataclass
from typing import List
from tool_registry import list_tools   # 导入工具注册表
from llm_adapter import LLMAdapter    # 导入LLM适配器
from state import State               # 导入状态管理
from common_types import DecisionResult, ToolDecisionScore  # 导入共享数据类型


def rule_score(tool: str, task: str) -> float:
    """规则优先级打分（最高权重）"""
    if tool == "calculator":
        # 数学任务优先使用计算器
        return 1.0 if any(ch.isdigit() for ch in task) else 0.0
    if tool == "echo":
        return 0.6  # 兜底工具
    return 0.3


def history_score(state: State, tool: str) -> float:
    """基于历史成功率打分，冷启动 0.5"""
    # 获取工具统计信息
    stats = state.tool_stats.get(tool)
    if not stats:
        return 0.5  # 冷启动默认值
    total = stats["success"] + stats["failure"]
    # 计算成功比例，避免除零错误
    return stats["success"] / total if total > 0 else 0.5


def llm_score(task: str, tool: str) -> float:
    """让 LLM 给出语义适配度（0~1）"""
    # 创建LLM适配器实例
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
        # 获取LLM评分并规范化到0-1范围
        text = llm.llm.invoke(prompt).content.strip()
        score = float(text)
        return max(0.0, min(score, 1.0))
    except:
        # 异常情况下返回默认评分
        return 0.5


def decide(step, state: State) -> DecisionResult:
    """综合打分选工具：rule + history + llm + experience_bias"""
    # 存储所有工具的评分
    scores: List[ToolDecisionScore] = []

    # 遍历所有可用工具
    for tool in list_tools():
        r = rule_score(tool, step.desc)  # 规则评分
        h = history_score(state, tool)   # 历史评分
        l = llm_score(step.desc, tool)   # LLM评分
        bias = state.tool_experience_bias.get(tool, 0.0)  # 经验偏向

        # 加权融合（权重可调）
        final = 0.35 * r + 0.25 * h + 0.25 * l + 0.15 * bias

        # 添加评分结果
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
        selected_tool=selected.tool_name,  # 返回选中的工具
        final_score=selected.final_score,  # 返回最终得分
        candidates=scores,                 # 返回所有候选工具评分
    )