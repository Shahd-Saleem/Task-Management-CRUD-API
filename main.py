import os
import psycopg
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional 

from database import init_db  # Import the initialization logic

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically creates table and seeds initial tasks on startup
    init_db()
    yield

app = FastAPI(
    title="Task Management CRUD API",
    description="A simple CRUD API tool to manage tasks",
    version="1.0",
    lifespan=lifespan
)

def get_db_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))


class AddTask(BaseModel):
    title: str
    done: Optional[bool] = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.get("/")
def api_description():
    """Retrieve API metadata and available endpoints"""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get('/health')
def health_description():
    """Retrieve the API status"""
    return {
        "status": "ok" 
    }


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
    """Insert a new task into PostgreSQL database"""
    if not task_data.title or not task_data.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    clean_title = task_data.title.strip()
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
                (clean_title, task_data.done)
            )
            row = cur.fetchone()
            conn.commit()

            return {
                "id": row[0],
                "title": row[1],
                "done": bool(row[2])
            }


@app.put('/tasks/{id}')
def put_task(id: int, task_data: UpdateTask):
    """Update a task in the PostgreSQL database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (id,))
            task = cur.fetchone()

            if not task:
                return JSONResponse(
                    status_code=404,
                    content={"error": "Task not found"}
                )

            if task_data.title is None and task_data.done is None:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Empty/Invalid Body"}
                )

            new_title = task[1]
            if task_data.title is not None:
                if not task_data.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty if passed"}
                    )
                new_title = task_data.title.strip()

            new_done = task[2]
            if task_data.done is not None:
                new_done = task_data.done

            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s;",
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
    """Delete a task from the PostgreSQL database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM tasks WHERE id = %s;", (id,))
            task = cur.fetchone()

            if not task:
                return JSONResponse(
                    status_code=404,
                    content={"error": "Task not found"}
                )

            cur.execute("DELETE FROM tasks WHERE id = %s;", (id,))
            conn.commit()

            return Response(status_code=204)

        # Git Code Used:
        # git add FileName / .
        # git commit -m "COMMENT"
        # git push

        # For example:
        # git add main.py
        # git commit -m "Stage 3: Full CRUD on Postgres"
        # git push