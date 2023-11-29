import matplotlib.pyplot as plt
import cv2
import numpy as np

def plt_imshow(title='image', img=None, figsize=(8, 5)):
    plt.figure(figsize=figsize)

    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []

            for i in range(len(img)):
                titles.append(title)

        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2BGR)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)

            plt.subplot(1, len(img),  i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])

        plt.show()
    else:
        if len(img.shape) <= 2:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(rgbImg, aspect='equal')
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()


def image_read(image):
    image_nparray = np.asarray(bytearray(image.file.read()), dtype=np.uint8)

    # 바이트 배열을 이미지로 디코드
    org_image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    # 이미지 출력
    plt_imshow("Original Image", org_image)

    return org_image
