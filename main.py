import sqlite3
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

DB_FILE = "tasks.db"

app = FastAPI(title="To-Do List API (SQLite)")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [("Buy milk", 0), ("Walk the dog", 0), ("Learn SQL", 0)],
        )
        conn.commit()
    conn.close()


init_db()


class Task(BaseModel):
    title: str
    done: bool = False


class TaskOut(Task):
    id: int


def row_to_task(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


# The assignment spec wants errors shaped like {"error": "..."} instead of
# FastAPI's default {"detail": "..."}, so we override both handlers.
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": "title is required"})


@app.get("/")
def root():
    return {"message": "To-Do API (SQLite) is running. Visit /docs for Swagger UI."}


# --- READ (all, with optional search/filter/sort — see README) ---
@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(search: str | None = None, done: bool | None = None, sort: str | None = None):
    query = "SELECT * FROM tasks WHERE 1=1"
    params: list = []
    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
    if done is not None:
        query += " AND done = ?"
        params.append(int(done))
    if sort == "title":
        query += " ORDER BY title"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [row_to_task(r) for r in rows]


# --- BONUS: stats using SQL's COUNT() instead of counting in Python ---
@app.get("/stats")
def get_stats():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    completed = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
    conn.close()
    return {"total": total, "completed": completed, "pending": total - completed}


# --- READ (one) ---
@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return row_to_task(row)


# --- CREATE ---
@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: Task):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, int(task.done))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "title": task.title, "done": task.done}


# --- UPDATE ---
@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: Task):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task.title, int(task.done), task_id),
    )
    conn.commit()
    conn.close()
    return {"id": task_id, "title": task.title, "done": task.done}


# --- DELETE ---
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": f"Task {task_id} deleted"}
