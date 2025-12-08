import cv2
import numpy as np
import time
import subprocess
import pytesseract
import re
import easyocr
from paddleocr import PaddleOCR


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def crop_region(img, x1, y1, x2, y2):
    return img[y1:y2, x1:x2]


def parse_power(text):
    # ví dụ: "5.79M"
    match = re.search(r"(\d+\.?\d*)\s*([MK]?)", text)
    if not match:
        return None
    num = float(match.group(1))
    unit = match.group(2).upper()

    if unit == "M":
        num *= 1_000_000
    elif unit == "K":
        num *= 1_000

    return int(num)

def read_number(img):
    if img is None or img.size == 0:
        return 0

    # resize ×2
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # làm mượt và threshold
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # tăng độ dày số
    kernel = np.ones((2,2), np.uint8)
    th = cv2.dilate(th, kernel, iterations=1)

    # chỉ đọc số
    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(th, config=config)

    # lọc giữ lại digit
    digits = ''.join(c for c in text if c.isdigit())
    
    if digits == "":
        return 0

    return int(digits)

def read_text(img):
    if img.ndim == 2:
        gray = img
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(gray, config="--psm 7")
    text = text.strip().replace(" ", "")

    # lọc ký tự rác
    filtered = ''.join(c for c in text if c.isalpha())

    return str(filtered) if filtered.isalpha() else None


reader = easyocr.Reader(['en'], gpu=False, quantize=True)

def read_easy(input_img, allow):
    # Nếu input là PATH → đọc ảnh
    if isinstance(input_img, str):
        img = cv2.imread(input_img)

    # Nếu input là numpy array → dùng trực tiếp
    elif isinstance(input_img, np.ndarray):
        img = input_img

    else:
        raise ValueError("Input must be file path or numpy array")

    # Resize cho nhanh
    small = cv2.resize(img, None, fx=0.5, fy=0.5)

    # OCR
    result = reader.readtext(
        small,
        detail=0,
        contrast_ths=0.05,
        adjust_contrast=0.5,
        # allowlist="0123456789BMK.",
        allowlist = allow,
        paragraph=False
    )

    if not result:
        return None

    text = "".join(result)

    match = re.search(r"[\d\.]+[MK]?", text)
    if match:
        return match.group(0)

    return None
