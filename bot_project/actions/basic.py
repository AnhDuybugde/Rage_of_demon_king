import cv2
import numpy as np
import time
from ppadb.client import Client
import subprocess

# ==================== ADB CONNECT ====================
client = Client(host="127.0.0.1", port=5037)
device = client.device("127.0.0.1:5555")


# ======================================================
def tap(x, y):
    device.shell(f"input tap {x} {y}")
    time.sleep(0.1)  # delay nhẹ cho an toàn

def screencap():
    # Chạy adb exec-out để lấy raw PNG bytes
    raw = subprocess.run(
        ["adb", "exec-out", "screencap -p"],
        stdout=subprocess.PIPE
    ).stdout

    # Chuyển raw bytes -> numpy array
    arr = np.frombuffer(raw, dtype=np.uint8)

    # Decode thành ảnh OpenCV (BGR)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

def screenshot_cv():
    raw = device.screencap()
    arr = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

def stable_screenshot(n=5):
    best_img = None
    best_score = 0

    for _ in range(n):
        time.sleep(0.05)
        img = screenshot_cv()

        # bỏ ảnh lỗi
        if img is None or img.size == 0:
            continue

        # tính độ nét
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        score = cv2.Laplacian(gray, cv2.CV_64F).var()

        # chọn ảnh sắc nét nhất
        if score > best_score:
            best_score = score
            best_img = img

    return best_img  


# ==================== OPENCV: FIND TEMPLATE ====================
def find_button(screen, name, threshold=0.8):
    template = cv2.imread(f"buttons/{name}.png")
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        h, w = template.shape[:2]
        cx = max_loc[0] + w // 2
        cy = max_loc[1] + h // 2
        return (cx, cy, max_val)
    return None

def find_any(button_list, threshold=0.8):
    for btn in button_list:
        if find_button(btn, threshold):
            return True
    return False

def click_button(name, threshold=0.8, timeout=5):
    """Tìm và click nút trong X giây."""
    start = time.time()
    while time.time() - start < timeout:
        screen = screenshot_cv()
        pos = find_button(screen, name, threshold)

        if pos:
            x, y, score = pos
            print(f"[+] CLICK {name} ({score:.2f}) at {x},{y}")
            tap(x, y)
            return True
        

    print(f"[!] Không tìm thấy nút {name}")
    return False

def click_any(button_list, threshold=0.7):
    for btn in button_list:
        if click_button(btn, threshold):
            return True
    return False

def wait_for(image_name, timeout=8):
    import time
    start = time.time()

    while True:
        if click_button(image_name):  
            print(f"[+] Đã thấy {image_name}")
            return True
        
        if time.time() - start > timeout:
            print("[!] Hết thời gian chờ")
            return False

        time.sleep(1)  # đỡ tốn CPU

def wait_for_any(list_images, end_button, timeout):
    start = time.time()
    screen = screenshot_cv()

    while True:
        for img in list_images:
            if click_button(img):
                print(f"[+] Phát hiện {img}")
                return img

            if find_button(screen, end_button, threshold=0.8):
                break

        if time.time() - start > timeout:
            print("[!] TIMEOUT, không thấy ảnh nào")
            return None

        time.sleep(1)

def auto_battle(next,n):
    i = 0
    print(f"--- Trận {i+1}/{n+1} ---")
    while i < 10:
        if click_button(next):
            i += 1         
            print(f"--- Trận {i+1}/{n+1} ---")
        if i == 10 or click_button("out_pillar"):
            break
    tap(486,39)
    tap(486,39)

def auto_arena(list_images,next,timeout):
    # đợi trận kết thúc
    wait_for_any(list_images, next, timeout)
    
    # next battle
    click_button(next)

def convert_damage(text):
    if text is None:
        return 0
    
    text = text.upper()

    if text.endswith("M"):
        return float(text[:-1]) * 1_000_000
    if text.endswith("K"):
        return float(text[:-1]) * 1_000
    if text.endswith("B"):
        return float(text[:-1]) * 1_000_000_000

    # không có hậu tố
    return float(text)






