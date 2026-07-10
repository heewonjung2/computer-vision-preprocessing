import cv2
import numpy as np
from pathlib import Path


def resize_image(image, width=224, height=224):
    # AI 모델 입력 크기에 맞도록 이미지 크기를 조정한다.
    # 기본 크기는 224×224이며, 필요하면 width와 height를 변경할 수 있다.
    return cv2.resize(image, (width, height))


def convert_to_grayscale(image):
    # 컬러 이미지를 흑백 이미지로 변환한다.
    # Grayscale은 색상 정보를 제거하고 밝기 정보만 남기므로 이미지 분석 및 전처리에 자주 사용된다.
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def normalize_image(image):
    # 이미지의 픽셀 값을 0~255 범위에서 0~1 범위로 정규화한다.
    # AI 모델 학습 시 데이터의 범위를 일정하게 맞추기 위해 사용한다.
    return image.astype(np.float32) / 255.0


def apply_blur(image, kernel_size=(5, 5)):
    # Gaussian Blur를 적용하여 이미지의 노이즈를 줄인다.
    return cv2.GaussianBlur(image, kernel_size, 0)


def flip_image(image):
    # 이미지를 좌우로 반전한다.
    # 데이터 증강(Data Augmentation)의 대표적인 기법이다.
    return cv2.flip(image, 1)


def rotate_image(image, angle=30):
    # 이미지를 지정한 각도만큼 회전한다.
    # 다양한 방향의 데이터를 생성하여 모델의 일반화 성능을 향상시킨다.
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    return cv2.warpAffine(image, matrix, (width, height))


def change_color(image, alpha=1.2, beta=30):
    # 이미지의 밝기와 대비를 조절하여 색상을 변화시킨다.
    # alpha는 대비, beta는 밝기를 의미한다.
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def is_dark_image(image, threshold=50):
    # 평균 밝기를 기준으로 너무 어두운 이미지를 판별한다.

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    return brightness < threshold


def detect_red_color(image, output_dir):
    # 이미지에서 빨간색 영역을 검출하여 결과 이미지를 저장한다.

    # AI 모델 입력 크기에 맞게 이미지 크기를 조정한다.
    image = resize_image(image)

    # OpenCV는 기본적으로 BGR 색상 공간을 사용하지만,
    # 색상을 기준으로 객체를 검출할 때는 HSV가 더 안정적이므로 변환한다.
    # 색(H), 채도(S), 명도(V)로 구성된다.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 빨간색은 HSV 색상환의 시작(0°)과 끝(180°)에 걸쳐 존재하기 때문에
    # 하나의 범위만으로는 모든 빨간색을 검출할 수 없다.
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # 두 개의 빨간색 범위에 대해 각각 마스크를 생성한다.
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # 두 마스크를 합쳐 모든 빨간색 영역을 하나의 마스크로 만든다.
    mask = mask1 + mask2

    # 마스크를 이용해 빨간색 영역만 남기고 나머지 색상은 제거한다.
    result = cv2.bitwise_and(image, image, mask=mask)

    # 현재 처리 중인 이미지의 결과 폴더에 저장하여
    # 여러 장의 이미지를 각각 관리할 수 있도록 한다.
    cv2.imwrite(
        str(output_dir / "red_filtered.jpg"),
        result
    )

    print("빨간색 검출 완료!")


def has_small_object(image, min_area=5000):
    """
    객체 크기 필터

    ① Grayscale: 객체를 찾기 쉽도록 색상을 제거한다.
    ② Threshold: 객체와 배경을 흰색/검은색으로 나눈다.
    ③ Contour: 객체의 외곽선을 찾는다.
    ④ Area: 가장 큰 객체의 면적을 계산한다.
    ⑤ 가장 큰 객체의 면적이 min_area보다 작으면 True를 반환한다.
    """

    # 가장 큰 객체의 면적이 5000픽셀보다 작으면 작은 객체로 판단한다.
    # 객체의 경계를 찾기 위해 흑백 이미지로 변환한다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 객체와 배경을 구분하기 위해 이진화한다.
    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # 객체의 외곽선(Contour)을 찾는다.
    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # 객체가 하나도 없으면 작은 객체로 판단한다.
    if len(contours) == 0:
        return True

    # 가장 큰 객체를 찾는다.
    largest_contour = max(contours, key=cv2.contourArea)

    # 가장 큰 객체의 면적을 계산한다.
    area = cv2.contourArea(largest_contour)

    # 가장 큰 객체의 면적이 기준보다 작으면 True를 반환한다.
    return area < min_area