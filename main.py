from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="To-Do List API")


tasks: dict[int, "Task"] = {}
next_id = 1


class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False


class TaskOut(Task):
    id: int


@app.get("/")
def root():
    return {"message": "To-Do API is running. Visit /docs for Swagger UI."}



@app.post("/tasks", response_model=TaskOut)
def create_task(task: Task):
    global next_id
    new_task = TaskOut(id=next_id, **task.model_dump())
    tasks[next_id] = new_task
    next_id += 1
    return new_task



@app.get("/tasks", response_model=list[TaskOut])
def list_tasks():
    return list(tasks.values())



@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]



@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = TaskOut(id=task_id, **task.model_dump())
    tasks[task_id] = updated_task
    return updated_task



@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": f"Task {task_id} deleted"}
