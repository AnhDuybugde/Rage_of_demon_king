import cv2
import numpy as np
import time
from ppadb.client import Client

from actions.basic import tap, screenshot_cv

from actions.advanced import (
    zenith_coin, claim_8h, 
    daily_trial, hidden_page, infinity, pillar_training, pillar, oni_house, guild,
    guild_boss, arena_automatic )

from actions.OCR import crop_region, read_number, read_text
import threading

class BotConfig:
    delay = 0.1
    threshold = 0.8

current_thread = None
stop_flag = False

def start_task(func):
    global current_thread, stop_flag

    # báo task cũ dừng
    stop_flag = True

    # nếu thread cũ còn chạy → chờ nó tắt
    if current_thread and current_thread.is_alive():
        current_thread.join()

    # reset flag
    stop_flag = False

    # tạo thread mới
    current_thread = threading.Thread(target=func)
    current_thread.start()

def auto_daily():
    global stop_flag
    while not stop_flag:
        zenith_coin()
        claim_8h()
        time.sleep(1)   # simulate work
    print("STOPPED")


def auto_side_tasks():
    global stop_flag
    while not stop_flag:
        daily_trial()
        time.sleep(0.2)
        hidden_page()
        time.sleep(0.2)
        infinity()
        time.sleep(0.2)
        pillar()
        time.sleep(0.2)
        oni_house()
        time.sleep(1)

    print("STOPPED")

def auto_trial(pillars):
    global stop_flag
    while not stop_flag:
        pillar_training(pillars)

        time.sleep(1)
    print("STOPPED")


def auto_guild_bosss():
    global stop_flag
    while not stop_flag:
        guild_boss(2250)
        time.sleep(1)

    print("STOPPED")


def auto_guild():
    global stop_flag
    while not stop_flag:
        guild()

        time.sleep(1)
    print("STOPPED")


def auto_arena():
    global stop_flag
    while not stop_flag:
        arena_automatic(n=1)

        time.sleep(1)
    print("STOPPED")


# ==================== ADB CONNECT ====================
# client = Client(host="127.0.0.1", port=5037)
# device = client.device("127.0.0.1:5555")

# if __name__ == "__main__":
#     print("=== START ===")

#     arena_automatic(2)

#     print("=== FINISHED ===")
