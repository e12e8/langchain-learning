def reflect(step, decision, result, state):
    if result.get("ok"):
        return {
            "is_success": True,
            "should_retry": False,
            "confidence": 0.9,
            "reason": "步骤执行成功",
            "failure_severity": 0.0,
            "counterfactual": None,
        }

    last_decision = state.get_last_decision(step.id)
    alternative = None

    if last_decision:
        ranked = sorted(
            last_decision["candidates"],
            key=lambda x: x["final_score"],
            reverse=True
        )
        if len(ranked) > 1:
            alternative = ranked[1]["tool"]

    # 确定失败类型
    if "error" in result:
        failure_type = "tool_error"  # 工具执行错误
    elif alternative is not None:
        failure_type = "decision_error"  # 决策错误，有替代方案
    else:
        failure_type = "no_progress"  # 无进展

    return {
        "is_success": False,
        "should_retry": True,
        "confidence": 0.6,
        "reason": "执行失败",
        "failure_severity": 0.4,
        "failure_type": failure_type,
        "counterfactual": {
            "alternative_tool": alternative,
            "reason": "当时评分次高"
        } if alternative else None
    }
