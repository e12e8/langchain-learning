# agent.py - 智能体核心控制器
from dataclasses import dataclass
from planner import plan             # 导入任务规划模块
from decision import decide          # 导入决策模块
from execution import execute        # 导入工具执行模块
from reflection import reflect       # 导入反思模块
from termination import should_terminate  # 导入终止条件判断模块
from state import State              # 导入状态管理模块
import asyncio                     # 异步编程库


@dataclass
class AgentResult:
    status: str                      # 执行状态
    result: dict | None              # 执行结果
    reason: str | None               # 执行原因
    state: dict                      # 当前状态


async def run_agent(task: str) -> AgentResult:
    """运行完整 Agent 闭环"""
    # 初始化状态管理器
    state = State()
    # 生成任务执行步骤
    steps = plan(task)

    # 遍历执行每个步骤
    for step_idx, step in enumerate(steps):
        retry_count = 0
        max_retries = step.max_retries

        last_result = None
        last_reflection = None

        # 单步支持多次重试
        while retry_count <= max_retries:
            # 基于当前状态做出决策
            decision = decide(step, state)
            # 记录决策过程
            state.record_decision(step.id, decision)

            # 构建执行上下文
            context = state.build_context(step)
            # 执行选定的工具
            result = execute(decision.selected_tool, context)
            # 反思执行结果
            reflection = reflect(step, decision, result)

            # 记录执行详情
            state.record_step(
                step_id=step.id,
                tool=decision.selected_tool,  # 记录工具选择
                result=result,                # 记录执行结果
                reflection=reflection,        # 记录反思结果
            )

            last_result = result
            last_reflection = reflection

            # 如果执行成功则跳出重试循环
            if reflection.get("is_success", False):
                break

            # 如果不应重试则跳出重试循环
            if not reflection.get("should_retry", False):
                break

            retry_count += 1

        # 每步结束后判断是否整体终止
        if should_terminate(last_reflection, state, step_idx, len(steps)):
            return AgentResult(
                status="finished",         # 设置完成状态
                result=last_result,          # 返回最终结果
                reason=None,
                state=state.to_dict(),     # 返回当前状态快照
            )

    # 返回未完成状态
    return AgentResult(
        status="incomplete",
        result=None,
        reason="所有步骤执行完毕但未满足终止条件",
        state=state.to_dict(),           # 返回最终状态快照
    )