import json
from fastapi import FastAPI, HTTPException

app = FastAPI()

ID = 0
STATUS_LIST = ["Задача создана", "Задача в процессе выполнения", "Задача выполнена"]
DEFAULT_STATUS = STATUS_LIST[0]

def get_new_id():
    global ID
    ID += 1
    return ID

class Task:
    def __init__(self, name: str):
        self.task_id = get_new_id()
        self.name = name
        self.status = DEFAULT_STATUS
    def to_dict(self):
        return {
            "task_id": self.task_id,
            "name": self.name,
            "status": self.status,
        }


tasks: list[Task] = []

@app.get("/tasks")
def get_tasks() -> list[dict]:
    return [t.to_dict() for t in tasks]

@app.post("/tasks")
def create_task(name: str):
    new_task = Task(name)
    tasks.append(new_task)
    return new_task.to_dict()


@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            if t.status == DEFAULT_STATUS:
                t.status = STATUS_LIST[1]
            elif t.status == STATUS_LIST[1]:
                t.status = STATUS_LIST[2]
            else:
                t.status = STATUS_LIST[2]
    else:
        return HTTPException(status_code=404, detail="ID не найден")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task_id == task_id:
            tasks.remove(task)
    else:
        return HTTPException(status_code=404, detail="ID не найден")