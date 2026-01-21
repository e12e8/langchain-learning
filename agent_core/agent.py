# agent.py
"""
Agent 主执行循环（Day 6 修正版）
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from planner import Step, plan
from decision import decide, DecisionResult
from tool_registry import get_tool
from reflection import reflect
from state import State


@dataclass
class AgentResult:
    status: str                 # finished | incomplete | aborted
    result: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None
    state: Dict[str, Any] = None


async def run_agent(task: str) -> AgentResult:
    state = State()
    steps = plan(task)  # 假设你有 plan 函数返回 List[Step]

    # Agent 主循环
    for step in steps:
        decision: DecisionResult = decide(step, state)

        # 1️⃣ 如果没有选中工具，认为任务结束
        if decision.tool_name is None:
            return AgentResult(
                status="finished",
                result=state.last_success_result(),
                state=state.to_dict()
            )

        # 2️⃣ 执行工具
        tool = get_tool(decision.tool_name)
        if tool is None:
            return AgentResult(
                status="failed",
                reason=f"工具不存在: {decision.tool_name}",
                state=state.to_dict()
            )

        result = tool.run(state.build_context(step))

        # 3️⃣ 反思
        reflection = reflect(step, decision, result)

        state.record_step(
            step_id=step.id,
            tool=decision.tool_name,
            result=result,
            reflection=reflection
        )

        # 4️⃣ 是否重试
        if reflection["should_retry"]:
            continue

    return AgentResult(
        status="incomplete",
        state=state.snapshot()
    )