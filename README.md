# To-Do List API

A tiny CRUD API for managing to-do tasks, built with [FastAPI](https://fastapi.tiangolo.com/).
Data lives **in memory only** — restarting the server wipes the list. That's intentional;
a real database comes later.

## What it does

| Method | Path          | Action                     |
|--------|---------------|-----------------------------|
| GET    | `/tasks`      | List all tasks              |
| GET    | `/tasks/{id}` | Get one task                |
| POST   | `/tasks`      | Create a task                |
| PUT    | `/tasks/{id}` | Update a task                |
| DELETE | `/tasks/{id}` | Delete a task                |

A `Task` looks like:
```json
{
  "title": "Buy milk",
  "description": "2% please",
  "completed": false
}
```
`title` is required. `description` and `completed` are optional.

## Run it locally

```bash
# 1. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload
```

The API is now running at `http://127.0.0.1:8000`.

## Try it in Swagger UI

FastAPI generates an interactive test page for free. With the server running, open:

**http://127.0.0.1:8000/docs**

Click any endpoint → "Try it out" → fill in the fields → "Execute". You'll see the
live request and response right there, no separate tool needed.

(There's also a plain machine-readable spec at `/openapi.json`, and an alternate
docs UI at `/redoc`.)

## Quick test with curl

```bash
# create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# list tasks
curl http://127.0.0.1:8000/tasks

# update task 1
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy oat milk", "completed": true}'

# delete task 1
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Project structure

```
todo-api/
├── main.py            # the whole API (~65 lines)
├── requirements.txt    # dependencies
├── README.md
└── .gitignore
```

## Publishing to GitHub

```bash
cd todo-api
git init
git add .
git commit -m "Build to-do list CRUD API with FastAPI"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Replace `<your-username>/<your-repo-name>` with your own GitHub repo (create an
empty one first on github.com — don't add a README there, or the push will conflict).
