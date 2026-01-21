# execution.py
from typing import Dict, Any
from tool_registry import get_tool


def execute(tool_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行指定的工具
    """
    tool = get_tool(tool_name)
    if not tool:
        return {"ok": False, "error": f"工具 {tool_name} 不存在"}

    try:
        return tool.run(context)   # ← 统一调用 run 方法
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "meta": {"duration_ms": 0, "cost": 0.0}
        }