import cv2
import os
import csv
import numpy as np
import time
from ppadb.client import Client

from actions.basic import tap, screenshot_cv, click_button, click_any, auto_battle, auto_arena, stable_screenshot, convert_damage
from actions.OCR import crop_region, read_easy, read_text

# ==================== ADB CONNECT ====================
client = Client(host="127.0.0.1", port=5037)
device = client.device("127.0.0.1:5555")


# ==================== QUEST FLOW ====================
def zenith_coin():
    click_button("x")
    click_any(["z&t","z&t_2"])
    time.sleep(0.15)
    tap(777,668)
    time.sleep(0.15)
    tap(1050,600)
    click_button("inner_hall")
    click_button("join")
    click_button("back")
    click_button("back")
    click_button("back")
    click_button("back")


def claim_8h():
    click_button("battle")
    time.sleep(7)
    tap(637,624)
    click_button("claim_reward")
    time.sleep(0.3)
    tap(100,600)
    time.sleep(0.3)
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
        time.sleep(1)
        click_button("yellow_battle")
        auto_battle("next_level", 9)
    click_button("back")  
    click_button("daily_trial_4")

def pillar():
    tap(882,171)
    click_button("pillar_2")
    time.sleep(0.2)
    click_button("shinobu")
    for i in range(20):
        tap(614,590)
        time.sleep(0.4)
    tap(21,30)
    time.sleep(1)
    click_button("back")
    time.sleep(0.5)
    tap(397,190)

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
    time.sleep(0.5)
    for i in range(20):
        tap(885,291)
    tap(970,168)
    time.sleep(0.1)
    click_button("back")
    time.sleep(0.5)
    tap(233,155)


def skip_until(thressholds):
    while True:
        # 1) start
        tap(1200,670)

        # 2) skip
        tap(102, 686)

        # 3) save or retry 
        time.sleep(2)
        img = stable_screenshot(n=2)

        roi = crop_region(img,560, 317, 659, 358)   
        value = read_easy(roi, "0123456789BMK.")

        if value is None:
            print("Không xác định được")
            continue

        value = convert_damage(value)
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
        while True:
            if click_button("challenge"):
                time.sleep(2)
                skip_until(thressholds)
            if click_button("victory"):
                break
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
        time.sleep(3)

        img = stable_screenshot(n=2)

        # tọa độ chuẩn đã kiểm tra từ ảnh thật
        dmg = crop_region(img, 195, 605 , 420, 660)
        dmg_text = read_easy(dmg, "0123456789BMK.")
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
   

def log_out():
    tap(63,70)
    time.sleep(0.3)
    tap(1080,663)
    time.sleep(2)
    click_button("close")
    time.sleep(0.3)
    tap(963,166)
    time.sleep(0.3)
    tap(637,491)
    time.sleep(0.2)


def x_arena():
    click_button("arena")
    click_button("x_arena")

    i = 0
    while i <= 10:
        print(f"---Trận {i+1}/10---")
        tap(157,356)
        time.sleep(2)
        tap(100,690)
        if click_button("yellow_back"):
            i+= 1
        if i == 10:
            break
    for i in range(2):
        click_button("back")
        time.sleep(0.3)


def puppet():
    click_button("puppet")
    time.sleep(0.2)
    click_button("puppet_2")
    time.sleep(0.5)
    i = 0
    while True:
        tap(1180, 656)
        tap(100,690)
        if click_button("victory_puppet"):
            i+=1
            if i == 5:
                break

    click_button("back")
    click_button("daily_trial_6")
    

def legion(lockdown):
    # click_button("legion_1")
    # time.sleep(1)
    # tap(150,220) #area1
    # # tap(500,410) #area2
    # # tap(860,520) #area3
    # # tap(1120,400) #area4
    # click_button("+")
    # click_button("M")
    # click_button("purchase")
    # time.sleep(0.2)
    # tap(340,676)
    for i in range(10):
        print(f"--Round {i+1}--")
        while True:
            if click_button(lockdown):
                tap(770,550)
            tap(1188,674)
            tap(102, 686)
            if click_button("victory"):
                break


def crawl(group_index):

    OPPONENT_TAPS = [
    (200, 300),
    (200, 450),
    (200, 600),
    (200, 750)
    ]

    CLOSE_BUTTON = (900, 200)

    NAME_REGION   = (100, 200, 700, 260)
    POWER_REGION  = (100, 330, 700, 390)

    results = []

    print(f"=== Scraping Group {group_index} ===")

    for idx, (x, y) in enumerate(OPPONENT_TAPS):
        print(f"Opponent {idx + 1}: tap to open...")

        tap(x, y)
        time.sleep(1)

        scrren = stable_screenshot(n=2)
        img = read_text(scrren, "0123456789BMK.")

        name = read_text(img, NAME_REGION)
        power = read_text(img, POWER_REGION)

        print(f"- Name: {name}")
        print(f"- Power: {power}\n")

        results.append({
            "name": name,
            "power": power
        })

        tap(*CLOSE_BUTTON)
        time.sleep(0.4)

    return results

def scrape_groups():
    all_opponents = []

    # Crawl dữ liệu
    for group in range(1, 17):
        group_data = crawl(group)  # crawl phải trả về list các dict, ví dụ [{"player": "...", "power": "..."}]
        all_opponents.extend(group_data)

    print("Done scraping 64 opponents.")

    # Lưu CSV
    path = r"C:\Users\jackw\Desktop\JLOY\Rage_of_demon_king\Data"
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "scraping_file.csv")

    if all_opponents:
        fieldnames = list(all_opponents[0].keys())
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_opponents)

    print(f"Saved CSV to {file_path}")
    return all_opponents
