from fastapi import FastAPI, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from typing import List
import uvicorn

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message" : "Hello SeJun World"}
@app.post("/uploadfile/")
async def uploadFile(files: List[UploadFile] = File(...)):
    result = []

    for file in files:
        # 업로드된 이미지를 PIL Image로 열기
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        # 여기에서 이미지를 처리하거나 다른 작업을 수행할 수 있습니다.
        # 이 예제에서는 간단히 이미지의 크기를 가져와 결과 리스트에 추가합니다.
        image_size = image.size
        result.append({"filename": file.filename, "size": image_size})

    return result

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