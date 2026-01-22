# execution.py - 工具执行模块
from typing import Dict, Any
from tool_registry import get_tool   # 导入工具注册表


def execute(tool_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    # 获取指定工具
    tool = get_tool(tool_name)
    if not tool:
        # 工具不存在时返回错误
        return {"ok": False, "error": f"工具 {tool_name} 不存在"}

    try:
        # 执行工具并返回结果
        return tool.run(context)
    except Exception as e:
        # 捕获异常并返回错误信息
        return {
            "ok": False,
            "error": str(e),
        }