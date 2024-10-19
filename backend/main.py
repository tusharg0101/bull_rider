from fastapi import FastAPI
from routes import router
import uvicorn

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
