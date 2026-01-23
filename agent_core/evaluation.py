def evaluate_outcome(state) -> dict:
    """
    判断整体目标是否已经达成（与单步成功/失败解耦）
    """
    step_results = state.step_results

    if not step_results:
        return {
            "is_complete": False,
            "reason": "尚无任何步骤结果"
        }

    # 示例规则：最后一步有可读输出即视为完成
    last_step = sorted(step_results.keys())[-1]
    last_result = step_results[last_step]

    if last_result.get("ok") or "content" in last_result:
        return {
            "is_complete": True,
            "reason": "已生成最终可交付结果"
        }

    return {
        "is_complete": False,
        "reason": "未生成最终结果"
    }
