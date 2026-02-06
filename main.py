from fastapi import FastAPI

app = FastAPI(title="FAFSA Validation Service")

@app.get("/")
def health_check():
    return {"status": "running"}