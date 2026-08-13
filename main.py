from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional 
import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

def init_db():
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL, 
        done boolean NOT NULL DEFAULT 0
        )
        """
        
    )
    conn.commit()
    cursor.execute("SELECT COUNT (*) FROM TASKS")
    count = cursor.fetchone()[0]

    if count == 0:
        tasks_list = [
            ('Cook a meal', 0),
            ('Study for exam', 1),
            ('Watch a movie', 1)
        ]
        cursor.executemany("INSERT INTO Tasks (title, done) values (?, ?)", tasks_list)
        conn.commit()

init_db()

app = FastAPI(
    title = "Task Management CRUD API",
    description= "A simple CRUD API tool to manage tasks",
    version= "1.0"
)

class AddTask(BaseModel):
    title : str
    done : Optional[bool] = False

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
    """Retrieve API tasks from SQLite database"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tasks')
    tasks = cursor.fetchall()

    new_list =[]
    for task in tasks:
        new_list.append(
            {
                'id': task['id'],
                'title' : task['title'],
                'done' : bool(task['done'])
            }
        )
    return new_list


    

@app.get('/tasks/{id}')
def task_with_id(id: int):
    """Retrieve API task based on a given ID from SQLite database"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tasks WHERE id = ?', (id,))
    task = cursor.fetchone()

    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return {
        'id': task['id'],
        'title': task['title'],
        'done': bool(task['done'])
    }
# git add .
# git commit -m "Stage 2: read endpoints with 404"

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

# @app.put('/tasks/{id}')
# def put_task(id:int, task_data: UpdateTask):
#     """Update a task with the requested ID"""
#     target = None    
#     for t in tasks:
#         if t['id'] == id:
#             target = t
#             break

#     if not target:
#         return JSONResponse(
#             status_code = 404,
#             content = {"error": "Unknown ID"}
#         )
    
#     if task_data.title is None and task_data.done is None:        
#         return JSONResponse(
#             status_code = 400,
#             content = {"error": "Empty/Invalid Body"}
#         )

#     if task_data.title is not None:
#         if not task_data.title.strip():
#             return JSONResponse(
#                 status_code = 400,
#                 content = {"error": "Title cannot be empty if passed"}
#             )
#         target["title"] = task_data.title.strip()

#     if task_data.done is not None:
#         target["done"] = task_data.done
#     return target

# @app.delete("/tasks/{id}", status_code=204)
# def delete_task(id: int):
#     """Delete a task with the requested ID"""
#     for i, task in enumerate(tasks):
#         if task['id'] == id:
#             del tasks[i]
#             return Response(status_code=204)
#     return JSONResponse(status_code=404, content={'error': 'Invalid ID'})

    # git add .
    # git commit -m "Stage 4: full CRUD"

    #git add .
    #git commit -m "Stage 5: Swagger UI"
    #git push


