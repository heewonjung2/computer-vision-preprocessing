from image_processing import detect_red_color, convert_to_grayscale
import cv2
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

image = cv2.imread(str(base_dir / "images" / "sample.jpg"))

gray = convert_to_grayscale(image)

cv2.imwrite(str(base_dir / "results" / "grayscale.jpg"), gray)

detect_red_color()

print("이미지 처리가 완료되었습니다.")

# Grayscale도 실행할 수 있도록 수정