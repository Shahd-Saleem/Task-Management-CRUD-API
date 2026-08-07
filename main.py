from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional 

app = FastAPI(
    title = "Task Management CRUD API",
    description= "A simple CRUD API tool to manage tasks",
    version= "1.0"
)

class AddTask(BaseModel):
    title : str

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

tasks = [
    {
        "id": 1,
        "title": "Inserting in a database",
        "done": False
    },

    {
        "id": 2,
        "title": "defining a function",
        "done": True
    },

    {
        "id": 3,
        "title": "printing a result",
        "done": True
    }
]

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
    """Retrieve API tasks"""
    return tasks

@app.get('/tasks/{id}')
def task_with_id(id: int):
    """Retrieve API task based on a given ID"""
    for task in tasks:
        if task["id"] == id:
            return task
        
    return JSONResponse(
        status_code = 404,
        content = {"error": f"Task {id} not found"}
    )
# git add .
# git commit -m "Stage 2: read endpoints with 404"

@app.post('/tasks', status_code = 201)
def post_task(task_data : AddTask):
    """Insert a new task in the list of tasks"""
    if not task_data.title:
        return JSONResponse(
            status_code = 400,
            content = {"error": "Title is required"}
        )
    if not task_data.title.strip():
        return JSONResponse(
            status_code = 400,
            content = {"error": "Title is empty"}
        )

    next_id = max([t["id"] for t in tasks], default = 0) + 1

    new_task = {
        "id": next_id,
        "title": task_data.title.strip(),
        "done": False
    }

    tasks.append(new_task)
    return new_task

#git add .
#git commit -m "Stage 3: create with validation"

@app.put('/tasks/{id}')
def put_task(id:int, task_data: UpdateTask):
    """Update a task with the requested ID"""
    target = None    
    for t in tasks:
        if t['id'] == id:
            target = t
            break

    if not target:
        return JSONResponse(
            status_code = 404,
            content = {"error": "Unknown ID"}
        )
    
    if task_data.title is None and task_data.done is None:        
        return JSONResponse(
            status_code = 400,
            content = {"error": "Empty/Invalid Body"}
        )

    if task_data.title is not None:
        if not task_data.title.strip():
            return JSONResponse(
                status_code = 400,
                content = {"error": "Title cannot be empty if passed"}
            )
        target["title"] = task_data.title.strip()

    if task_data.done is not None:
        target["done"] = task_data.done
    return target

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    """Delete a task with the requested ID"""
    for i, task in enumerate(tasks):
        if task['id'] == id:
            del tasks[i]
            return Response(status_code=204)
    return JSONResponse(status_code=404, content={'error': 'Invalid ID'})

    # git add .
    # git commit -m "Stage 4: full CRUD"

    #git add .
    #git commit -m "Stage 5: Swagger UI"
    #git push


