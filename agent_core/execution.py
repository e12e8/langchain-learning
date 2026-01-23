from tools.echo import echo
from tools.calculator import calculator


def execute(step, decision, state):
    context = ""

    if step.needs_previous:
        last = list(state.step_results.values())[-1]
        context = f"(基于前一步结果: {last.get('result')})"

    if decision.selected_tool == "calculator":
        return calculator("1999 + 1996")

    if decision.selected_tool == "echo":
        return echo(f"{step.desc} {context}")

    return {"ok": False, "error": "unknown_tool"}
