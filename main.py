from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from typing import List
import uvicorn
import logging
from pydantic import BaseModel

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)


# 미들웨어를 사용하여 로그 출력
@app.middleware("http")
async def log_requests(request, call_next):
    # Request 로그 출력
    logging.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    # Response 로그 출력
    logging.info(f"Sent response: {response.status_code}")
    return response


@app.get("/hello")
def hello():
    return {"message": "Hello SeJun World"}


class ImageInfo(BaseModel):
    page: int
    image: UploadFile


@app.post("/homework/images/{user_id}/{homework_id}")
async def submit_homework(
        user_id: int,
        homework_id: int,
        images: list[UploadFile] = File(...)
):
    results = []
    for image in images:
        file_name = image.filename
        file_size = len(image.file.read())

        # 여기에서 이미지 처리 로직을 추가할 수 있습니다.
        # 예를 들어, 이미지를 저장하거나 다른 처리를 수행할 수 있습니다.

        results.append({
            "file_name": file_name,
            "file_size": f"{file_size} byte",
            "status": "success"
        })

    return {"results": results}


origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:5173",
    # 또는 "http://localhost:5173"
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
