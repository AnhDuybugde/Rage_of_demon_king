import cv2
import numpy as np
import time
from ppadb.client import Client
from PIL import Image

from actions.basic import tap, convert_damage
from actions.advanced import guild
from actions.OCR import crop_region, read_number, read_easy

# ==================== ADB CONNECT ====================
client = Client(host="127.0.0.1", port=5037)
device = client.device("127.0.0.1:5555")

if __name__ == "__main__":
    print("=== START ===")

    guild()
    
    # img_path = r"C:/Users/jloy5/OneDrive/Documents/XuanZhi9/Pictures/Screenshots/Screenshot_20251208-093751.png"

    # # img = Image.open(img_path)
    # # img.show()
    # img = cv2.imread(img_path)              # ảnh màu BGR
    # pic = crop_region(img, 195, 605 , 420, 660)

    # # cv2.imshow("CROP", pic)
    # # cv2.waitKey(0)

    # dmg_text = read_damage_easy(pic)
    # print("OCR:", dmg_text)

    # # chuyển "230.61M" thành số thật
    # value = convert_damage(dmg_text)
    # print("DMG:", value)


    print("=== FINISHED ===")

