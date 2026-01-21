# reflection.py
from typing import Dict, Any


def reflect(step, decision, result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reflection 模块：
    - 判断本次执行是否成功
    - 是否需要重试
    - 是否属于不可恢复错误
    """

    # 工具层返回失败
    if not result.get("ok"):
        error_msg = result.get("error", "unknown_error")

        # 明确不可恢复错误（示例，可扩展）
        fatal_errors = [
            "invalid syntax",
            "permission",
            "not found",
        ]

        for fatal in fatal_errors:
            if fatal in error_msg.lower():
                return {
                    "is_success": False,
                    "should_retry": False,
                    "confidence": 0.1,
                    "reason": f"不可恢复错误：{error_msg}",
                }

        # 可重试错误
        return {
            "is_success": False,
            "should_retry": True,
            "confidence": 0.4,
            "reason": f"执行失败，可重试：{error_msg}",
        }

    # 工具返回成功
    return {
        "is_success": True,
        "should_retry": False,
        "confidence": 0.9,
        "reason": "工具执行成功",
    }
