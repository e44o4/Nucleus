from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Network Automation Platform Running"}