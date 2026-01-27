from tools.echo import echo
from tools.calculator import calculator
from tools.knowledge import query_knowledge


def execute(step, decision, state):
    context = ""

    if step.needs_previous:
        last = list(state.step_results.values())[-1]
        context = f"(基于前一步结果: {last.get('result')})"

    if decision.selected_tool == "calculator":
        return calculator("1999 + 1996")

    if decision.selected_tool == "echo":
        return echo(f"{step.desc} {context}")

    if decision.selected_tool == "knowledge":
        # 将 step 描述传给知识检索函数
        return query_knowledge(step.desc)

    return {"ok": False, "error": "unknown_tool"}
