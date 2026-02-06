from fastapi import FastAPI
from models.application import FAFSAApplication

app = FastAPI(title="FAFSA Validation Service")

@app.get("/")
def health_check():
    return {"status": "running"}