from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()

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
    return{
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get('/health')
def health_description():
    return{
        "status": "ok" 
    }

# git add .
# git commit -m "Stage 1: root and health endpoints"
# git push

@app.get('/tasks')
def return_tasks():
    return tasks

@app.get('/tasks/{id}')
def task_with_id(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
        
    return JSONResponse(
        status_code = 404,
        content = {"error": f"Task {id} not found"}
    )

# git add .
# git commit -m "Stage 2: read endpoints with 404"