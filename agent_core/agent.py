# agent.py
from dataclasses import dataclass
from planner import plan
from decision import decide
from execution import get_tool
from reflection import reflect
from termination import should_terminate
from state import State


@dataclass
class AgentResult:
    status: str
    result: dict | None
    reason: str | None
    state: dict


async def run_agent(task: str) -> AgentResult:
    state = State()
    steps = plan(task)

    for step in steps:
        # ───────────── 决策阶段 ─────────────
        decision = decide(step, state)

        # ⭐ 记录决策轨迹（Day 8 核心）
        state.record_decision(step.id, decision)

        tool = get_tool(decision.selected_tool)

        # ───────────── 执行阶段 ─────────────
        result = tool.run(state.build_context(step))

        # ───────────── 反思阶段 ─────────────
        reflection = reflect(step, decision, result)

        # ───────────── 记录执行 ─────────────
        state.record_step(
            step_id=step.id,
            tool=decision.selected_tool,
            result=result,
            reflection=reflection,
        )

        # ───────────── 终止判断 ─────────────
        if should_terminate(reflection):
            return AgentResult(
                status="finished",
                result=result,
                reason=None,
                state=state.to_dict(),
            )

    return AgentResult(
        status="incomplete",
        result=None,
        reason="steps finished but not terminated",
        state=state.to_dict(),
    )
