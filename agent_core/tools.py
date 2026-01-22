# tools.py - 工具定义文件
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
        # 获取任务内容
        task = context.get("task", "")
        return {
            "ok": True,                    # 标记执行成功
            "content": f"Echo: {task}",     # 返回回声内容
            "meta": {                       # 元数据
                "duration_ms": 0,           # 执行耗时
                "cost": 0.0                 # 执行成本
            }
        }


class CalculatorTool:
    """
    计算器工具
    """

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 获取表达式
        expression = context.get("expression", "")

        try:
            # 执行表达式计算
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                "ok": True,                    # 标记执行成功
                "result": result,              # 返回计算结果
                "meta": {                       # 元数据
                    "duration_ms": 10,           # 执行耗时
                    "cost": 0.001               # 执行成本
                }
            }
        except Exception as e:
            # 返回错误信息
            return {
                "ok": False,                   # 标记执行失败
                "error": str(e),               # 错误信息
                "meta": {                       # 元数据
                    "duration_ms": 10,           # 执行耗时
                    "cost": 0.001               # 执行成本
                }
            }