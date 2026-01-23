from dataclasses import dataclass
from typing import List, Any


@dataclass
class ToolCandidate:
    """
    单个工具的决策评分明细（可解释性核心）
    """
    tool_name: str
    rule_score: float
    history_score: float
    llm_score: float
    final_score: float


@dataclass
class DecisionResult:
    """
    Decision 模块的最终输出
    """
    selected_tool: str
    final_score: float
    candidates: List[ToolCandidate]


@dataclass
class AgentResult:
    """
    Agent 总体运行结果
    """
    status: str
    result: Any
    reason: str | None
    state: dict
