from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="赵毅的 Agent API")

class TaskRequest(BaseModel):
    task: str

@app.post("/run")
async def handle_task(request: TaskRequest):
    # 调用核心的 run_agent 函数
    result = await run_agent(request.task)
    return {
        "status": result.status,
        "answer": result.result.get("answer") if result.result else "无结果",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
