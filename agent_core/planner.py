class Step:
    def __init__(self, id, desc, needs_previous=False):
        self.id = id
        self.desc = desc
        self.needs_previous = needs_previous


def plan(task: str):
    # 核心修复：根据传入的 task 动态判断步骤
    if any(keyword in task for keyword in ["学习", "重点", "计划", "谁是"]):
        return [
            Step("step_1", f"在知识库中搜索关于: {task}"),
            Step("step_2", "根据搜索到的计划内容进行总结回答", needs_previous=True),
        ]

    # 默认兜底：计算逻辑
    return [
        Step("step_1", "计算 1999 + 1996"),
        Step("step_2", "整理结果并回答", needs_previous=True),
    ]
