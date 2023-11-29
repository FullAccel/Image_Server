import cv2, os
from imutils.perspective import four_point_transform
import imutils
from domain import image_api
import numpy as np
import pytesseract
from domain import s3_upload

def track_text(img):
    """
    1. 흑백 이미지로 변환
    2. 가우시안 블러 적용 : 이미지를 부드럽게 만들고 노이즈를 감소
    3. 적응형 이진화 적용 : 검정색만 있는 이미지를 생성. 이를 통해 물체를 강조하고 배경을 제거
    4. Canny 에지 검출 : 물체의 윤곽선을 추출하거나 이미지에서 중요한 부분을 강조
    :param img: 원본 이미지
    :return:
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussianBlur = cv2.GaussianBlur(gray, (11,11), 0)
    adaptiveThreshold = cv2.adaptiveThreshold(gaussianBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    min_threshold, max_threshold = 75, 200
    edged = cv2.Canny(adaptiveThreshold, min_threshold, max_threshold)

    image_list_title = ['gray', 'gaussianBlur', 'adaptiveThreshold', 'edged']
    image_list = [gray, gaussianBlur, adaptiveThreshold, edged]
    # image_api.plt_imshow(image_list_title, image_list)

    return edged

def dilate(img):
    """
    커널 내의 픽셀이 하나라도 1인 경우, 중심을 중심으로 주변의 픽셀을 1로 만듭니다.
    이를 통해 이미지의 하얀색으로 된 영역의 넓이를 팽창시킵니다.
    이는 나중에 영역 인식을 더 쉽게 하는데 도움을 줍니다.
    :param img: 배경은 검정색 글자는 하얀색으로 변환된 이미지
    :return: 하얀색 영역이 팽창된 이미지
    """

    titles = []
    images = []
    #커널의 크기를 2X2로 생성합니다.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    #팽창 연산을 4번 진행합니다
    dilate = cv2.dilate(img, kernel, iterations=4)

    titles.append('dilate')
    images.append(dilate)
    # image_api.plt_imshow(titles,images)

    return dilate


def find_real_detecting_img(img, origin_img):
    """
    쓸데 없는 부분은 지우고 인식해야되는 부분만 남깁니다.
    :param img: dilate 된 이미지
    :param origin_img: 원본 이미지
    :return: 숙제 페이지 영역만 detecting해서 자른 이미지
    """
    titles = []
    images = []

    # contours를 찾아 크기순으로 정렬
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    homework_contour = None

    # 정렬된 contours를 반복문으로 수행하며 4개의 꼭지점을 갖는 도형을 검출
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)

        # contours가 크기순으로 정렬되어 있기때문에 제일 첫번째 사각형을 영수증 영역으로 판단하고 break
        if len(approx) == 4:
            homework_contour = approx
            break

    # 만약 추출한 윤곽이 없을 경우 오류
    if homework_contour is None:
        raise Exception(("숙제의 윤곽선을 딸 수 없습니다."))

    output = origin_img.copy()
    cv2.drawContours(output, [homework_contour], -1, (0, 255, 0), 2)
    titles.append("homework_contour")
    images.append(output)

    homework_img = four_point_transform(origin_img, homework_contour.reshape(4, 2))
    titles.append("howework_img")
    images.append(homework_img)

    image_api.plt_imshow(titles,images)

    return homework_img


def getContours(img, origin_img):
    """
    이진화된 img에서 윤곽선을 찾아내고, 해당 윤곽선을 감싸는 직사각형들의 정보를 추출
    :param img: 직사각형 영역 추출할 이미지
    :param origin_img: 원본 이미지
    :return: 직사각형 좌표 정보 리스트
    """
    rectangles = []
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            rectangles.append((x, y, w, h))  # 직사각형 정보를 목록에 추가

    copy_origin_img = origin_img.copy()
    for (x, y, w, h) in rectangles:
        cv2.rectangle(copy_origin_img, (x, y), (x + w, y + h), (36, 255, 12), 3)

    # image_api.plt_imshow('img', copy_origin_img)
    return rectangles


def groupRectangle(img, rectangles):
    """
    이미지에서 추출된 직사각형들을 필터링하고, 그룹핑하여 시각화하는 과정
    :param img: 원본 이미지
    :param rectangles: 인식된 사각형 영역 리스트
    :return:
    """
    title = []
    images = []
    filtered_rectangles = []
    img_height, img_width, _ = img.shape

    # 이상하게 인식된 사각형을 filtering 합니다.
    for x, y, w, h in rectangles:
        if w / h < 0.2:
            continue
        if w < img_width//2 and h < img_height//2:
            filtered_rectangles.append(((x, y, w, h)))

    filtered_img = img.copy()
    for x, y, w, h in filtered_rectangles:
        cv2.rectangle(filtered_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    title.append('filter')
    images.append(filtered_img)

    group_img = img.copy()
    grouped_rectangles, weights = cv2.groupRectangles(np.concatenate((filtered_rectangles, filtered_rectangles)), groupThreshold=1, eps=0.2)
    for x, y, w, h in grouped_rectangles:
        cv2.rectangle(group_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    title.append('group_img')
    images.append(group_img)

    image_api.plt_imshow(title, images)

    return grouped_rectangles


def divideRectangleImage(img, rectangles):
    """
    직사각형들을 하나의 이미지들로 잘라 이미지 list로 만듭니다.
    :param img:
    :param rectangles:
    :return:
    """
    titles = []
    images = []

    # Crop and save individual images for each rectangle
    for i, (x, y, w, h) in enumerate(rectangles):
        if i > 6:
            raise IndexError("사진 분할은 6장이상 될 수 없습니다.")
        cropped_img = img[y:y + h, x:x + w]
        titles.append(f'rectangle_{i + 1}')
        images.append(cropped_img)


    # Display the images
    # image_api.plt_imshow(titles, images)

    return images


def store_to_webp(user_id, homework_id, index, images, homework_img):
    """
        직사각형들을 하나의 이미지들로 잘라 이미지 목록을 반환합니다.
        :param img:
        :param rectangles:
        :return: 저장된 WebP 이미지 파일의 경로 목록
        """
    saved_paths = []

    os.makedirs('./images', exist_ok=True)

    filename = f'origin_{user_id}_{homework_id}_{index}.webp'
    cv2.imwrite(f'./images/{filename}', homework_img, [int(cv2.IMWRITE_WEBP_QUALITY), 100])
    s3_upload.upload_file(filename)
    saved_paths.append(f'{os.getenv("S3_URL")}/images/{filename}')
    os.remove(f'./images/{filename}')
    # 각 직사각형에 대해 이미지를 자르고 저장합니다.
    for i, image in enumerate(images):
        filename = f'problem_{user_id}_{homework_id}_{index}_{i + 1}.webp'
        # WebP 파일로 저장
        filepath = f'./images/{filename}'
        cv2.imwrite(filepath, image, [int(cv2.IMWRITE_WEBP_QUALITY), 100])

        s3_upload.upload_file(filename)
        os.remove(filepath)

        saved_paths.append(f'{os.getenv("S3_URL")}/images/{filename}')

    return saved_paths



def make_edge(img):
    # 이미지 너비와 높이 얻기
    height, width, _ = img.shape

    # 전체적인 사각형 좌표 계산
    x, y = 0, 0
    w, h = width, height

    # 이미지에 전체적인 사각형 선 그리기
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img


def find_num_and_answer(img, rectangles):
    def distance_from_origin(rect):
        x, y, _, _ = rect
        return (x - 0) ** 2 + (y - 0) ** 2  # x=0, y=0에서의 유클리드 거리의 제곱

    titles = []
    images = []
    num_and_answers_img = []
    # rectangles를 distance_from_origin 함수를 기준으로 정렬
    rectangles = sorted(rectangles, key=distance_from_origin, reverse=False)

    problem_num = rectangles[0]
    answer = rectangles[-1]

    # 좌표 추출
    x1, y1, w1, h1 = problem_num
    x2, y2, w2, h2 = answer

    # 이미지 crop
    num_image = img[y1:y1 + h1, x1:x1 + w1]
    answer_image = img[y2:y2 + h2, x2:x2 + w2]

    images = [num_image, answer_image]

    num_image = track_text(num_image)
    answer_image = track_text(answer_image)
    num_and_answers_img.append(num_image)
    num_and_answers_img.append(answer_image)

    titles = ['problem_num', 'answer','problem_num', 'answer']
    images.append(num_image)
    images.append(answer_image)

    image_api.plt_imshow(titles, images)

    return num_and_answers_img

def tesseract_ocr(imgs):
    options = "--psm 4"
    result = []
    for img in imgs:
        text = text = pytesseract.image_to_string(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), lang='eng', config=options)
        result.append(text)
        print("OCR 결과는")
        print(text)








