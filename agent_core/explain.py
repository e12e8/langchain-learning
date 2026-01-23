# explain.py
from typing import Dict, Any
from replay import replay


def build_explanation(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    构建结构化解释信息（不使用 LLM）
    """
    return {
        "steps": len(state["history"]) // 2,
        "tools_used": list(state["tool_stats"].keys()),
        "tool_learning_bias": state["tool_experience_bias"],
        "replay": replay(state["history"])
    }
