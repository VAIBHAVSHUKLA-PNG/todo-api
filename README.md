# To-Do List API (now with SQLite)

A CRUD API for managing to-do tasks, built with [FastAPI](https://fastapi.tiangolo.com/)
and backed by a real **SQLite** database. Unlike the first version of this project
(which kept tasks in a Python list in memory), your data now **survives a server
restart** — it lives in a file called `tasks.db` sitting right next to `main.py`.

## Why SQLite?

- It needs no separate database server to install or run — the whole database is
  one file on disk.
- Python's standard library already includes a SQLite driver (`sqlite3`), so no
  extra dependency was needed for the database itself.
- It's the natural next step up from "array in memory": same SQL concepts you'd
  use with Postgres or MySQL later, but zero setup.

## Where the database file lives

`tasks.db` is created automatically, in the same folder as `main.py`, the first
time you run the app. It is **not** committed to GitHub (see `.gitignore`) —
each person who clones this repo gets their own fresh database, auto-created and
auto-seeded with 3 example tasks on first run.

## What it does

| Method | Path                       | Action                                    |
|--------|----------------------------|--------------------------------------------|
| GET    | `/tasks`                   | List tasks (supports `?search=`, `?done=`, `?sort=title`) |
| GET    | `/tasks/{id}`              | Get one task                                |
| POST   | `/tasks`                   | Create a task — `201` on success, `400` if `title` is missing |
| PUT    | `/tasks/{id}`              | Update a task                                |
| DELETE | `/tasks/{id}`              | Delete a task                                |
| GET    | `/stats`                   | Task counts (total / completed / pending), via SQL `COUNT()` |

A `Task` looks like:
```json
{
  "title": "Buy milk",
  "done": false
}
```
`title` is required. `done` is optional (defaults to `false`).

Unknown ids return `404` with `{"error": "Task not found"}`.

## Run it locally

```bash
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. The database file `tasks.db` is created
automatically on first run, with 3 example tasks seeded in — restart the server
as many times as you like, the seed data only inserts once and your own tasks
stick around.

## Try it in Swagger UI

**http://127.0.0.1:8000/docs** — click any endpoint → "Try it out" → fill in
fields → "Execute".

## Look inside the database yourself

Download [DB Browser for SQLite](https://sqlitebrowser.org/), open `tasks.db`,
and go to the **Execute SQL** tab. A few queries to try:

```sql
-- list every task
SELECT * FROM tasks;

-- only completed tasks
SELECT * FROM tasks WHERE done = 1;

-- how many tasks exist
SELECT COUNT(*) FROM tasks;

-- mark everything as done
UPDATE tasks SET done = 1;

-- clean out completed tasks
DELETE FROM tasks WHERE done = 1;
```

Example run (from the "Execute SQL" tab, with the API's seed data loaded):

```
sqlite> SELECT * FROM tasks;
id  title          done
1   Buy milk       0
2   Walk the dog   0
3   Learn SQL      0
```

Change something here and immediately hit `GET /tasks` in Swagger UI — you'll
see your database edit reflected instantly, no server restart needed. That's
the core idea of this assignment: the API and the database are two separate
layers, and either one can change the same underlying data.

> 📸 **Add your own screenshot here** of DB Browser for SQLite with `tasks.db`
> open, to show in your submission.

## Quick test with curl

```bash
# create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'

# list tasks, with filters
curl "http://127.0.0.1:8000/tasks?search=milk"
curl "http://127.0.0.1:8000/tasks?done=false"
curl "http://127.0.0.1:8000/tasks?sort=title"

# update task 1
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy oat milk", "done": true}'

# delete task 1
curl -X DELETE http://127.0.0.1:8000/tasks/1

# stats
curl http://127.0.0.1:8000/stats
```

## Project structure

```
todo-api/
├── main.py            # the whole API, including the SQLite layer (~160 lines)
├── requirements.txt
├── README.md
├── .gitignore          # ignores tasks.db so everyone gets a fresh database
└── tasks.db            # created automatically on first run (not in git)
```

## Publishing to GitHub

```bash
git add .
git commit -m "Stage 5: database documentation"
git push
```

(If this is a brand-new repo rather than a continuation of Assignment 1, see the
first commit's README for the full `git init` / `git remote add` sequence.)
