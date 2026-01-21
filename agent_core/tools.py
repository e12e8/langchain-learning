# tools.py
"""
工具定义文件（注册已迁移到 tool_registry.py）
建议：未来可以考虑把所有工具类都迁移到 tool_registry.py
"""

from typing import Dict, Any


class EchoTool:
    """
    回声工具（示例）
    """

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        task = context.get("task", "")
        return {
            "ok": True,
            "content": f"Echo: {task}",
            "meta": {
                "duration_ms": 0,
                "cost": 0.0
            }
        }


class CalculatorTool:
    """
    计算器工具
    """

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        expression = context.get("expression", "")

        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                "ok": True,
                "result": result,
                "meta": {
                    "duration_ms": 10,
                    "cost": 0.001
                }
            }
        except Exception as e:
            return {
                "ok": False,
                "error": str(e),
                "meta": {
                    "duration_ms": 10,
                    "cost": 0.001
                }
            }