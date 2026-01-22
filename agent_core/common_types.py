"""
共享的数据类型定义，避免循环导入
"""
from dataclasses import dataclass
from typing import Dict, Any, List


# ────────────────────────────────────────────────
# 单个工具的评分明细（Decision Trace 原子）
# ────────────────────────────────────────────────
@dataclass
class ToolDecisionScore:
    tool_name: str
    rule_score: float
    history_score: float
    llm_score: float
    final_score: float


# ────────────────────────────────────────────────
# 决策最终结果（包含所有候选工具）
# ────────────────────────────────────────────────
@dataclass
class DecisionResult:
    selected_tool: str
    final_score: float
    candidates: List[ToolDecisionScore]