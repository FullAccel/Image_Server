from fastapi import FastAPI, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import logging
from domain import homeworkImage_router

tags_metadata = [
    {
        "name": "submit_homework",
        "description": "'https://chaeda-s3.s3.ap-northeast-2.amazonaws.com/images/origin_1_1_0.webp' 에서 1_1_0은 {userId} _ {homeworkId} _ {사진Index}"
    }
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(homeworkImage_router.router)
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
