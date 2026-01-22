# reflection.py - 反思模块
from typing import Dict, Any


def reflect(step, decision, result: Dict[str, Any]) -> Dict[str, Any]:
    """评估本次执行质量，并给出学习信号"""
    if result.get("ok"):
        # 执行成功时返回成功信号
        return {
            "is_success": True,           # 标记执行成功
            "should_retry": False,        # 无需重试
            "confidence": 0.9,            # 高置信度
            "reason": "工具执行成功",      # 成功原因
            "failure_severity": 0.0       # 失败严重度为0
        }

    # 获取错误信息并转为小写
    error_msg = result.get("error", "unknown_error").lower()
    severity = 0.3  # 默认轻度失败

    # 根据错误类型设置严重程度
    if any(word in error_msg for word in ["not found", "permission", "invalid"]):
        severity = 0.9                 # 高严重度错误
    elif any(word in error_msg for word in ["timeout", "rate limit"]):
        severity = 0.4                 # 中等严重度错误
    elif any(word in error_msg for word in ["syntax", "type", "value"]):
        severity = 0.7  # syntax error 严重度 0.7，可重试

    # 判断是否应该重试
    should_retry = severity < 0.8 or "syntax" in error_msg  # 加 syntax 可重试

    return {
        "is_success": False,           # 标记执行失败
        "should_retry": should_retry,   # 是否需要重试
        "confidence": 1.0 - severity,   # 计算置信度
        "reason": f"执行失败，严重度 {severity:.2f}: {error_msg}",  # 失败原因
        "failure_severity": severity    # 失败严重度
    }