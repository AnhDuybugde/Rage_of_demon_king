import cv2
import numpy as np
import time
from ppadb.client import Client

from actions.basic import tap, screenshot_cv, click_button, auto_battle, auto_arena, stable_screenshot, convert_damage
from actions.OCR import crop_region, read_easy

# ==================== ADB CONNECT ====================
client = Client(host="127.0.0.1", port=5037)
device = client.device("127.0.0.1:5555")


# ==================== QUEST FLOW ====================
def zenith_coin():
    click_button("x")
    click_button("x_small")
    tap(1400,400)
    tap(500,88)
    time.sleep(0.15)
    tap(777,668)
    time.sleep(0.15)
    tap(1050,600)
    click_button("inner_hall")
    click_button("join")
    click_button("back")
    click_button("back")
    click_button("back")

def claim_8h():
    click_button("battle")
    time.sleep(5)
    tap(637,624)
    click_button("claim_reward")
    time.sleep(0.1)
    tap(100,600)
    time.sleep(0.1)
    click_button("back")

def daily_trial():
    click_button("trials")
    click_button("daily_trial")
    click_button("quick_challenge")
    click_button("quick_challenge_2")
    time.sleep(0.2)
    tap(100,600)
    click_button("x_small")
    click_button("back")

def hidden_page():
    click_button("hidden_page")
    click_button("hidden_page_2")
    time.sleep(0.15)
    tap(1069,655)
    time.sleep(0.1)
    click_button("quick_battle")
    click_button("x_small")
    tap(100,600)
    click_button("back")
    click_button("daily_trial_2")

def infinity():
    tap(237,159)
    click_button("infinity_2")
    click_button("rush")
    click_button("confirm")
    tap(100,600)
    click_button("back")
    click_button("daily_trial_3")

def pillar_training(list):
    tap(960,370)
    click_button("pillar_training_2")
    for name in list:
        click_button(name)
        click_button("yellow_rush")
        tap(100,600)
        click_button("yellow_rush")
        tap(100,600)
        click_button("fight")
        click_button("yellow_battle")
        auto_battle("next_level", 9)
    click_button("back")  
    click_button("back")
    click_button("daily_trial_4")

def pillar():
    tap(882,171)
    click_button("pillar_2")
    time.sleep(0.2)
    click_button("shinobu")
    for i in range(20):
        tap(614,590)
        time.sleep(0.2)
    for i in range(2):
        tap(21,30)
        time.sleep(1)
    time.sleep(0.2)
    click_button("daily_trial_5")


def oni_house():
    tap(1053,159)
    click_button("oni_house")
    time.sleep(0.1)
    click_button("quick_select")
    click_button("yellow_enter")
    click_button("claim_reward")
    time.sleep(0.05)
    tap(600,600)
    click_button("rush")
    click_button("confirm")
    time.sleep(8)
    tap(600,600)
    tap(600,600)
    tap(1220, 264)
    time.sleep(0.1)
    for i in range(20):
        tap(885,291)
    tap(970,168)
    time.sleep(0.1)
    click_button("back")
    time.sleep(0.2)
    tap(233,155)


def skip_until(thressholds):
    while True:
        # 1) start
        tap(1200,670)
        time.sleep(0.3)

        # 2) skip
        tap(102, 686)

        # 3) save or retry 
        time.sleep(0.3)
        img = stable_screenshot(n=2)

        roi = crop_region(img,190, 606, 377, 660)   # tuỳ vị trí của game
        value = read_easy(roi)

        print("OCR value =", value)

        if value < thressholds:
            print("retry")
            click_button("retry")
        elif value > thressholds:
            print("save")
            click_button("save")
            tap(600,600)
            break

def guild_boss(thressholds):
    click_button("guild_boss_icon")
    for i in range(5):
        click_button("challenge")

        skip_until(thressholds)

        tap(100,600)
        time.sleep(6)


def analyze_arena():
    img = stable_screenshot(n=2)

    # ===== OCR Power =====
    power_imgs = [
        crop_region(img, 95, 410, 200, 440),
        crop_region(img, 395, 410, 500, 440),
        crop_region(img, 695, 410, 800, 440),
    ]

    raw_powers = [read_easy(p, "0123456789BMK.") for p in power_imgs]
    powers = [convert_damage(x) for x in raw_powers]

    # ===== OCR Name =====
    name_imgs = [
        crop_region(img, 48, 450, 223, 480),
        crop_region(img, 348, 450, 523, 480),
        crop_region(img, 648, 450, 823, 480),
    ]

    names = [read_easy(n, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-") for n in name_imgs]

    print("Raw Powers:", raw_powers)
    print("Powers:", powers)
    print("Names:", names)

    whitelist = ["Danibur26", "Wayu", "ArbitraryAlgier59", "TSL", "SunSword", "Ali_1", "Danibur_26", "Shinobu"]

    candidates = []
    # lọc theo whitelist
    for i in range(3):
        if powers[i] is not None and names[i] in whitelist:
            candidates.append((powers[i], i))

    # không có whitelist → lấy tất cả
    if not candidates:
        candidates = [(powers[i], i) for i in range(3) if powers[i] is not None]

    if not candidates:
        print("Không tìm được target phù hợp")
        return None

    # chọn người có power nhỏ nhất
    target_idx = min(candidates)[1]

    print("===> Target:", names[target_idx], "Power:", powers[target_idx])
    return target_idx

def attack_target(idx):
    if idx == 0:
        tap(135, 540)
    elif idx == 1:
        tap(440, 540)
    elif idx == 2:
        tap(740, 540)
    
def arena_automatic( n, list_images = ["in_battle_arena","yellow_back"] , next = "yellow_back" , timeout = 180):
    click_button("arena")
    time.sleep(0.1)
    click_button("arena_2")
    click_button("fight")
    time.sleep(0.3)
    for i in range(n):
        idx = analyze_arena()
        print(f"--- Trận {i+1}/{n} ---")
        if idx is not None:
            attack_target(idx)
        auto_arena(list_images,next,timeout)
    time.sleep(0.2)
    click_button("back")
    click_button("back")

def guild():
    click_button("guild")
    time.sleep(0.2)
    tap(814, 282)

    for _ in range(2):
        # chọn team 3 lần
        time.sleep(0.4)
        for _ in range(3):
            tap(1106, 673)

        click_button("yellow_battle")
        time.sleep(7)  # chờ dmg load xong

        tap(102, 686)
        time.sleep(0.3)

        img = stable_screenshot(n=2)

        # tọa độ chuẩn đã kiểm tra từ ảnh thật
        dmg = crop_region(img, 195, 605 , 420, 660)

        dmg_text = read_easy(dmg)
        print("OCR:", dmg_text)

        if dmg_text is None:
            print("Không xác định được")
            continue

        # chuyển "230.61M" thành số thật
        value = convert_damage(dmg_text)
        print("DMG:", value)

        if value > 10000:
            tap(600, 600)
            print("> 10000")
        else:
            tap(800, 600)
            print("< 10000")
   