# finalizer.py
from llm_adapter import LLMAdapter
from explain import build_explanation


async def finalize(state, explain: bool = False) -> dict:
    facts = state.step_results

    prompt = f"""
你是一个严谨的助手，请根据以下【执行结果】回答用户问题。

【执行结果】：
{facts}

要求：
1. 只基于事实回答
2. 不得引入新的推理
3. 语言简洁自然
"""

    adapter = LLMAdapter()
    answer = await adapter.ainvoke(prompt)

    result = {
        "answer": answer,
        "evidence": facts,
        "confidence": 1.0
    }

    if explain:
        result["explanation"] = build_explanation(state.to_dict())

    return result
