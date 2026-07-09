from image_processing import (
    detect_red_color,
    convert_to_grayscale,
    normalize_image,
    apply_blur,
    flip_image,
    rotate_image
)
import cv2
from pathlib import Path

# 실행 위치가 달라져도 같은 파일을 찾기 위해 pathlib를 사용한다.
base_dir = Path(__file__).resolve().parent.parent

# 원본 이미지 불러오기
image = cv2.imread(str(base_dir / "images" / "sample.jpg"))

if image is None:
    print("이미지를 불러오지 못했습니다.")
    exit()

# Grayscale 변환
gray = convert_to_grayscale(image)
cv2.imwrite(str(base_dir / "results" / "grayscale.jpg"), gray)

# 이미지 정규화
normalized = normalize_image(image)

# 정규화된 이미지는 0~1 범위이므로 저장을 위해 다시 0~255 범위로 변환한다.
cv2.imwrite(
    str(base_dir / "results" / "normalized.jpg"),
    (normalized * 255).astype("uint8")
)

# Blur 적용
blurred = apply_blur(image)

cv2.imwrite(
    str(base_dir / "results" / "blur.jpg"),
    blurred
)

# 좌우 반전
flipped = flip_image(image)

cv2.imwrite(
    str(base_dir / "results" / "flipped.jpg"),
    flipped
)

# 이미지 회전
rotated = rotate_image(image)

cv2.imwrite(
    str(base_dir / "results" / "rotated.jpg"),
    rotated
)

# 빨간색 검출
detect_red_color()

print("이미지 처리가 완료되었습니다.")