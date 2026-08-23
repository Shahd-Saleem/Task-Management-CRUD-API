import os
import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional 

load_dotenv()

app = FastAPI(
    title="Task Management CRUD API",
    description="A simple CRUD API tool to manage tasks",
    version="1.0"
)

def get_db_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))

class AddTask(BaseModel):
    title: str
    done: Optional[bool] = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


#tasks = [
#    {
#        "id": 1,
#        "title": "Inserting in a database",
#        "done": False
#    },
#
#    {
#        "id": 2,
#        "title": "defining a function",
#        "done": True
#    },
#
#    {
#        "id": 3,
#        "title": "printing a result",
#        "done": True
#    }
#]


#@app.get('/')
#def hello_world():
#    return {"message": 'Hello World'}
# Stage 0 DONE

@app.get("/")
def api_description():
    """Retrieve API metadata and available endpoints"""
    return{
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get('/health')
def health_description():
    """Retrieve the API status"""
    return{
        "status": "ok" 
    }

# git add .
# git commit -m "Stage 1: root and health endpoints"
# git push

@app.get('/tasks')
def return_tasks():
    """Retrieve API tasks from PostgreSQL database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
            rows = cur.fetchall()
            
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "done": bool(row[2])
                }
                for row in rows
            ]

@app.get('/tasks/{id}')
def task_with_id(id: int):
    """Retrieve API task based on a given ID from PostgreSQL database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (id,))
            task = cur.fetchone()

            if not task:
                return JSONResponse(
                    status_code=404,
                    content={"error": "Task not found"}
                )

            return {
                "id": task[0],
                "title": task[1],
                "done": bool(task[2])
            }

@app.post("/tasks", status_code=201)
def post_task(task_data: AddTask):
    """Insert a new task into SQLite database"""

    if not task_data.title or not task_data.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    clean_title = task_data.title.strip()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (clean_title, task_data.done)
    )
    conn.commit()

    new_id = cursor.lastrowid

    return {
        "id": new_id,
        "title": clean_title,
        "done": task_data.done
    }


#git add .
#git commit -m "Stage 3: create with validation"

@app.put('/tasks/{id}')
def put_task(id: int, task_data: UpdateTask):
    """Update a task in the SQLite database"""
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Tasks WHERE id = ?", (id,))
    task = cursor.fetchone()

    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": "Unknown ID"}
        )

    if task_data.title is None and task_data.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Empty/Invalid Body"}
        )

    new_title = task['title']
    if task_data.title is not None:
        if not task_data.title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty if passed"}
            )
        new_title = task_data.title.strip()

    new_done = task['done']
    if task_data.done is not None:
        if task_data.done:
            new_done = 1
        else:
            new_done = 0

    cursor.execute(
        "UPDATE Tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, id)
    )
    conn.commit()

    return {
        "id": id,
        "title": new_title,
        "done": bool(new_done)
    }

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    """Delete a task from the SQLite database"""
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Tasks WHERE id = ?", (id,))
    task = cursor.fetchone()

    if not task:
        return JSONResponse(
            status_code=404,
            content={'error': 'Invalid ID'}
        )

    cursor.execute("DELETE FROM Tasks WHERE id = ?", (id,))
    conn.commit()

    return Response(status_code=204)


    # git add .
    # git commit -m "Stage 4: full CRUD"

    #git add .
    #git commit -m "Stage 5: Swagger UI"
    #git push


