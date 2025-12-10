import cv2
import numpy as np
import time
from ppadb.client import Client

from actions.basic import tap, screenshot_cv
from app import stop_event

from actions.advanced import (
    zenith_coin, claim_8h, 
    daily_trial, hidden_page, infinity, pillar_training, pillar, oni_house, guild,log_out,x_arena,puppet, legion,
    guild_boss, arena_automatic )

from actions.OCR import crop_region, read_number, read_text

class BotConfig:
    delay = 0.1
    threshold = 0.8

def auto_daily():
    zenith_coin()
    claim_8h()


def auto_side_tasks():
    daily_trial()
    time.sleep(0.2)
    hidden_page()
    time.sleep(0.2)
    pillar()
    time.sleep(0.4)


def auto_trial(pillars):
    pillar_training(pillars)

def auto_guild_bosss():
    guild_boss(50.0)
    time.sleep(1)

def auto_guild():
    guild()


def auto_arena():
    arena_automatic(n=1)

def auto_log():
    log_out()

def auto_x_arena():
    x_arena()

def auto_puppet():
    puppet()

def auto_oni():
    oni_house()

def auto_infinity():
    infinity()

def auto_legion():
    legion("lock3")
# ==================== ADB CONNECT ====================
# client = Client(host="127.0.0.1", port=5037)
# device = client.device("127.0.0.1:5555")

# if __name__ == "__main__":
#     print("=== START ===")

#     arena_automatic(2)

#     print("=== FINISHED ===")
