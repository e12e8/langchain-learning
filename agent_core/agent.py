from state import State
from planner import plan
from decision import decide
from execution import execute
from reflection import reflect
from termination import should_terminate
from common_types import AgentResult
from finalizer import finalize

async def run_agent(task: str):
    state = State()
    steps = plan(task)

    for idx, step in enumerate(steps):
        while True:
            # 决策、执行和反思
            decision = decide(step, state)
            state.record_decision(step.id, decision)

            # 假设执行也是异步的（如果有网络调用）
            result = execute(step, decision, state)
            reflection = reflect(step, decision, result, state)

            state.record_step(step.id, decision.selected_tool, result, reflection)

            if should_terminate(reflection, state, idx, len(steps)):
                # 关键：await 异步总结，启用解释模式
                final_answer = await finalize(state, explain=True)

                return AgentResult(
                    status="finished",
                    result=final_answer,
                    reason=None,
                    state=state.to_dict(),
                )

            if not reflection["should_retry"]:
                break


    return AgentResult(
        status="incomplete",
        result=None,
        reason="步骤完成但未触发终止条件",
        state=state.to_dict()
    )