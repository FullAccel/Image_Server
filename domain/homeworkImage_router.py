from fastapi import APIRouter
from fastapi import File, UploadFile
from domain import image_api, textDecting

router = APIRouter(
    prefix="/homework/images",
)


@router.post("/{user_id}/{homework_id}", tags=["submit_homework"])
async def submit_homework(
        user_id: int = 1,  # 또는 다른 기본값
        homework_id: int = 1,  # 또는 다른 기본값
        images: list[UploadFile] = File(...)
):
    results = []
    for i, image in enumerate(images):
        origin_img = image_api.image_read(image)
        track_text_img = textDecting.track_text(origin_img)
        dilate_img = textDecting.dilate(track_text_img)
        homework_img = textDecting.find_real_detecting_img(dilate_img, origin_img)

        track_text_img = textDecting.track_text(homework_img)
        dilate_img = textDecting.dilate(track_text_img)
        rectangles = textDecting.getContours(dilate_img, homework_img)
        group_rectangles = textDecting.groupRectangle(homework_img, rectangles)
        problem_imgs = textDecting.divideRectangleImage(homework_img, group_rectangles)
        s3_saved_paths = textDecting.store_to_webp(user_id, homework_id, i, problem_imgs, homework_img)


        for problem in problem_imgs:
            problem = textDecting.make_edge(problem)
            track_text_problem = textDecting.track_text(problem)
            dilate_problem = textDecting.dilate(track_text_problem)
            problem_rectangles = textDecting.getContours(dilate_problem, problem)
            problem_group_rectangles = textDecting.groupRectangle(problem, problem_rectangles)
            num_and_answers_img = textDecting.find_num_and_answer(problem, problem_group_rectangles)
            textDecting.tesseract_ocr(num_and_answers_img)

        # 예를 들어, 이미지를 저장하거나 다른 처리를 수행할 수 있습니다.
        results = s3_saved_paths

    return results