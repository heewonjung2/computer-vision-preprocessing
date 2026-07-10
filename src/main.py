from image_processing import (
    detect_red_color,
    convert_to_grayscale,
    normalize_image,
    apply_blur,
    flip_image,
    rotate_image,
    change_color,
    is_dark_image,
    has_small_object
)

import cv2
from pathlib import Path

# 실행 위치가 달라져도 같은 파일을 찾기 위해 pathlib를 사용한다.
base_dir = Path(__file__).resolve().parent.parent

# images 폴더 안의 모든 jpg 파일을 가져온다.
image_paths = sorted((base_dir / "images").glob("*.jpg"))

for image_path in image_paths:

    print(f"\n===== {image_path.name} 처리 중 =====")

    # 이미지 읽기
    image = cv2.imread(str(image_path))

    if image is None:
        print(f"{image_path.name}을 불러오지 못했습니다.")
        continue

    # 현재 이미지(sample1, sample2...) 결과를 저장할 폴더 생성: 이미지마다 결과를 분리하여 저장, 관리와 확인이 편리.
    output_dir = base_dir / "results" / image_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    # Grayscale 변환
    gray = convert_to_grayscale(image)
    cv2.imwrite(
        str(output_dir / "grayscale.jpg"),
        gray
    )

    # 이미지 정규화
    normalized = normalize_image(image)

    # 정규화된 이미지는 0~1 범위이므로 저장을 위해 다시 0~255 범위로 변환한다.
    cv2.imwrite(
        str(output_dir / "normalized.jpg"),
        (normalized * 255).astype("uint8")
    )

    # Blur 적용
    blurred = apply_blur(image)
    cv2.imwrite(
        str(output_dir / "blur.jpg"),
        blurred
    )

    # 좌우 반전
    flipped = flip_image(image)
    cv2.imwrite(
        str(output_dir / "flipped.jpg"),
        flipped
    )

    # 이미지 회전
    rotated = rotate_image(image)
    cv2.imwrite(
        str(output_dir / "rotated.jpg"),
        rotated
    )

    # 색상 변화
    color_changed = change_color(image)
    cv2.imwrite(
        str(output_dir / "color_changed.jpg"),
        color_changed
    )

    # 평균 밝기 확인
    if is_dark_image(image):
        print("너무 어두운 이미지입니다.")
    else:
        print("정상 밝기 이미지입니다.")

    # 객체 크기 확인
    if has_small_object(image):
        print("객체가 너무 작습니다.")
    else:
        print("객체 크기가 적절합니다.")

    # 빨간색 검출
    detect_red_color(image, output_dir)

    print(f"{image_path.name} 전처리 완료!")


print("\n모든 이미지 처리가 완료되었습니다.")