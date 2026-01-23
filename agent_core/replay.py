# replay.py
from typing import List, Dict, Any


def replay(history: List[Dict[str, Any]]) -> str:
    """
    将 Agent 的 history 转换为可读的行为回放文本
    """
    lines = []

    for idx, item in enumerate(history, 1):
        if item["type"] == "decision":
            d = item["decision"]
            lines.append(
                f"[{idx}] DECISION | step={item['step_id']} | "
                f"selected={d['selected_tool']} | score={d['final_score']:.2f}"
            )
            for c in d["candidates"]:
                lines.append(
                    f"    - candidate={c['tool']} "
                    f"(rule={c['rule_score']}, "
                    f"history={c['history_score']}, "
                    f"llm={c['llm_score']} → final={c['final_score']:.2f})"
                )

        elif item["type"] == "execution":
            r = item["reflection"]
            lines.append(
                f"[{idx}] EXECUTE  | step={item['step_id']} | tool={item['tool']} | "
                f"success={r['is_success']} | confidence={r['confidence']:.2f}"
            )

            if r.get("counterfactual"):
                lines.append(
                    f"    ↳ counterfactual: alternative_tool="
                    f"{r['counterfactual']['alternative_tool']}"
                )

    return "\n".join(lines)
