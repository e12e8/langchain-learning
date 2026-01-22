# tool_registry.py - 工具注册表
from typing import Dict, Any, Protocol, List
import re  # 加 re 用于提取表达式


class Tool(Protocol):
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 工具协议定义
        ...


class EchoTool:
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 获取任务描述
        task = context.get("step_desc", "")
        # 获取前置结果
        previous = context.get("previous_results", [])
        summary = f"{task}"
        if previous:
            # 注入前步结果
            summary += f" (基于前步结果: {previous[-1].get('result', 'N/A')})"  # 注入前步结果
        return {"ok": True, "content": f"Echo: {summary}"}


class CalculatorTool:
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 获取任务描述
        desc = context.get("step_desc", "")
        # 提取纯表达式：找数字/运算符，忽略中文
        expression = re.sub(r'[^\d\s\+\-\*/\(\)]', '', desc).strip()  # 移除非数学字符
        expression = re.sub(r'\s+', '', expression)  # 去空格
        # 示例: "计算 17 * 23，然后把结果乘以 5" → "17*23*5"
        if not expression:
            return {"ok": False, "error": "No valid expression found"}

        try:
            # 执行表达式计算
            result = eval(expression, {"__builtins__": {}}, {})
            return {"ok": True, "result": result}
        except Exception as e:
            # 返回错误信息
            return {"ok": False, "error": str(e)}


# 注册工具字典
_TOOLS: Dict[str, Tool] = {
    "echo": EchoTool(),
    "calculator": CalculatorTool(),
}


def get_tool(name: str) -> Tool | None:
    # 根据名称获取工具
    return _TOOLS.get(name)


def list_tools() -> List[str]:
    # 返回所有可用工具名称
    return list(_TOOLS.keys())