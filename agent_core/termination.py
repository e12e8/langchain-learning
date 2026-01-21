from typing import Dict, Any

def should_terminate(reflection: Dict[str, Any]) -> bool:
    """
    判断是否应该终止执行
    """
    return reflection.get("is_success", False)  # 根据反思结果判断是否终止