#from fastapi import FastAPI
#app = FastAPI()

#@app.get('/')
#def hello_world():
#    return {"message": 'Hello World'}

from fastapi import FastAPI
app = FastAPI()

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
