class Step:
    def __init__(self, step_id: str, desc: str, needs_previous: bool = False):
        self.id = step_id
        self.desc = desc
        self.needs_previous = needs_previous


def plan(task: str):
    return [
        Step("step_1", "计算 1999 + 1996"),
        Step("step_2", "基于上一步结果，整理并输出最终答案", needs_previous=True),
    ]
