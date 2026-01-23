# finalizer.py - 最终结果生成模块
from typing import Dict, Any
from state import State


def finalize(state: State) -> Dict[str, Any]:
    """
    将 Agent 的多步执行结果，整理为一个对用户 / 业务友好的最终答案
    """

    step_results = state.step_results

    # 1️⃣ 找到“核心数值结果”（通常来自 calculator）
    numeric_result = None
    for step_id, result in step_results.items():
        if "result" in result and isinstance(result["result"], (int, float)):
            numeric_result = result["result"]

    # 2️⃣ 找到“最终表达结果”（通常来自 echo / summary）
    final_text = None
    for step_id, result in reversed(list(step_results.items())):
        if "content" in result:
            final_text = result["content"]

    # 3️⃣ 计算整体置信度（简化版：基于成功率）
    tool_stats = state.tool_stats
    total = sum(v["success"] + v["failure"] for v in tool_stats.values())
    success = sum(v["success"] for v in tool_stats.values())
    confidence = round(success / total, 2) if total > 0 else 0.5

    # 4️⃣ 构造企业级返回结构
    return {
        "answer": final_text or numeric_result,
        "evidence": step_results,
        "confidence": confidence,
    }
