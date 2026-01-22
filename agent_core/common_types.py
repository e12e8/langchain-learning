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
    tool_name: str                   # 工具名称
    rule_score: float                # 规则评分
    history_score: float             # 历史评分
    llm_score: float                 # LLM评分
    final_score: float               # 最终评分


# ────────────────────────────────────────────────
# 决策最终结果（包含所有候选工具）
# ────────────────────────────────────────────────
@dataclass
class DecisionResult:
    selected_tool: str               # 选中的工具
    final_score: float               # 最终得分
    candidates: List[ToolDecisionScore]  # 候选工具列表