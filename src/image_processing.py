import cv2
import numpy as np
from pathlib import Path


def resize_image(image, width=224, height=224):
   # AI 모델 입력 크기에 맞도록 이미지 크기를 조정한다.
   # 기본 크기는 224×224이며, 필요하면 width와 height를 변경할 수 있다.
    return cv2.resize(image, (width, height))

def convert_to_grayscale(image):
    # 컬러 이미지를 흑백 이미지로 변환
    # Grayscale은 색상 정보 제거, 밝기 정보만 남김-> 이미지 분석, 전처리에서 자주 사용.
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def normalize_image(image):
    # 이미지의 픽셀 값을 0~255 범위에서 0~1 범위로 정규화
    # AI 모델 학습 시 데이터의 범위를 일정하게 맞추기 위해 사용.
    return image.astype(np.float32) / 255.0

def detect_red_color():
    # 이미지에서 빨간색 영역을 검출하여 결과 이미지를 저장한다.
    # 현재 파일(src/image_processing.py)을 기준으로 프로젝트 최상위 폴더를 찾는다.
    # 어느 위치에서 실행하더라도 이미지 경로가 올바르게 지정된다.
    base_dir = Path(__file__).resolve().parent.parent

    image_path = base_dir / "images" / "sample.jpg"
    output_path = base_dir / "results" / "red_filtered.jpg"

    # OpenCV를 이용해 이미지를 읽어온다.
    image = cv2.imread(str(image_path))

    # 이미지를 불러오지 못한 경우 이후 함수에서 오류가 발생하므로
    # 먼저 예외 상황을 확인하고 함수를 종료한다.
    if image is None:
        print("이미지를 불러오지 못했습니다.")
        return
    
    # AI 모델 입력 크기에 맞게 이미지 크기를 조정한다.
    image = resize_image(image)

    # OpenCV는 기본적으로 BGR 색상 공간을 사용하지만,
    # 색상을 기준으로 객체를 검출할 때는 HSV가 더 안정적이므로 변환.
    # 색(H), 채도(S), 명도(V)로 구성.
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

    # 처리 결과를 파일로 저장하여 이후 확인하거나 재사용할 수 있도록 한다.
    cv2.imwrite(str(output_path), result)

    print("처리 완료!")