# tool_registry.py
from typing import Dict, Any, Protocol, List

# ────────────────────────────────────────────────
# 工具协议（保持不变）
# ────────────────────────────────────────────────
class Tool(Protocol):
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ...

# ────────────────────────────────────────────────
# 具体工具实现（全部集中在这里）
# ────────────────────────────────────────────────
class EchoTool:
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        task = context.get("task", "")
        return {
            "ok": True,
            "content": f"Echo: {task}",
            "meta": {"duration_ms": 0, "cost": 0.0}
        }


class CalculatorTool:
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        expression = context.get("expression", "")
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                "ok": True,
                "result": result,
                "meta": {"duration_ms": 10, "cost": 0.001}
            }
        except Exception as e:
            return {
                "ok": False,
                "error": str(e),
                "meta": {"duration_ms": 10, "cost": 0.001}
            }

# ────────────────────────────────────────────────
# 全局注册表（唯一一份）
# ────────────────────────────────────────────────
_TOOLS: Dict[str, Tool] = {
    "echo": EchoTool(),
    "calculator": CalculatorTool(),
    # 以后新增工具直接在这里加一行
    # "search": SearchTool(),
}

# ────────────────────────────────────────────────
# 对外接口（其他文件只能用这些）
# ────────────────────────────────────────────────
def register_tool(name: str, tool_instance: Tool):
    """允许动态注册（可选）"""
    _TOOLS[name] = tool_instance

def get_tool(name: str) -> Tool | None:
    return _TOOLS.get(name)

def list_tools() -> List[str]:
    return list(_TOOLS.keys())