from fastapi import FastAPI
from models.application import FAFSAApplication
from validation import run_validations

app = FastAPI(title="FAFSA Validation Service")

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/validate")
def validate_application(application: FAFSAApplication):
    return run_validations(application)
