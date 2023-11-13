from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message" : "Hello SeJun World"}


origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",# 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # TODO 로컬 배포
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # TODO 실서버 배포
    uvicorn.run("main:app", host="0.0.0.0", port=8000)