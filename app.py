from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from ppadb.client import Client

import bot_tasks
import subprocess
from threading import Event, Thread

app = Flask(__name__)
log = []

# Kết nối ADB
# ==================== ADB CONNECT ====================
client = Client(host="127.0.0.1", port=5037)
device = client.device("127.0.0.1:5555")


USERNAME = "admin"
PASSWORD = "anhduy54"

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        "Authentication required", 401,
        {"WWW-Authenticate": 'Basic realm="Login"'}
    )

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- MAIN PAGE ----------------
@app.route("/")
def index():
    return render_template("index.html", log=log,
                           delay=bot_tasks.BotConfig.delay,
                           threshold=bot_tasks.BotConfig.threshold)

@app.route("/tap", methods=["GET"])
def tap():
    # lấy tọa độ
    x = request.args.get("x")
    y = request.args.get("y")
    if not x or not y:
        return jsonify({"status": "error", "message": "Missing x or y"}), 400

    # chạy lệnh adb tap
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
    return jsonify({"status": "ok", "x": x, "y": y})

# ---------------- TASKS ----------------
current_thread = None
stop_event = Event()

def start_task(target):
    global current_thread

    # Stop task cũ
    stop_event.set()

    # Chờ dừng hoàn toàn
    if current_thread and current_thread.is_alive():
        current_thread.join()

    # Reset stop và chạy task mới
    stop_event.clear()
    current_thread = Thread(target=target)
    current_thread.start()

@app.route("/run_daily")
def run_daily():
    start_task(bot_tasks.auto_daily())
    
    return redirect(url_for('index'))

@app.route("/run_side_tasks")
def run_side_tasks():
    start_task(bot_tasks.auto_side_tasks())
    
    return redirect(url_for('index'))

@app.route("/run_guild_bosss")
def run_guild_bosss():
    start_task(bot_tasks.auto_guild_bosss())
    
    return redirect(url_for('index'))

@app.route("/run_guild")
def run_guild():
    start_task(bot_tasks.auto_guild())
    
    return redirect(url_for('index'))

@app.route("/run_arena")
def run_arena():
    start_task(bot_tasks.auto_arena())
    
    return redirect(url_for('index'))

@app.route("/run_trial_all")
def run_trial_all():
    start_task(bot_tasks.auto_trial(["fire", "water", "wind", "oni"])) 
    
    return redirect(url_for('index'))

@app.route("/run_trial_fire")
def run_trial_fire():
    start_task(bot_tasks.auto_trial(["fire"]))
    
    return redirect(url_for('index'))

@app.route("/run_trial_water")
def run_trial_water():
    start_task(bot_tasks.auto_trial(["water"]))
    
    return redirect(url_for('index'))

@app.route("/run_trial_wind")
def run_trial_wind():
    start_task(bot_tasks.auto_trial(["wind"]))
    
    return redirect(url_for('index'))

@app.route("/run_trial_oni")
def run_trial_oni():
    start_task(bot_tasks.auto_trial(["oni"]))
    return redirect(url_for('index'))

@app.route("/log_out")
def log_out():
    start_task(bot_tasks.auto_log())
    return redirect(url_for('index'))

@app.route("/run_x_arena")
def run_x_arena():
    start_task(bot_tasks.auto_x_arena())
    return redirect(url_for('index'))

@app.route("/run_puppet")
def run_puppet():
    start_task(bot_tasks.auto_puppet())
    return redirect(url_for('index'))

@app.route("/run_oni")
def run_oni():
    start_task(bot_tasks.auto_oni())
    return redirect(url_for('index'))

@app.route("/run_infinity")
def run_infinity():
    start_task(bot_tasks.auto_infinity())
    return redirect(url_for('index'))

@app.route("/run_legion")
def run_legion():
    start_task(bot_tasks.auto_legion())
    return redirect(url_for('index'))

@app.route("/run_scraping")
def run_scraping():
    start_task(bot_tasks.auto_craw())
    return redirect(url_for('index'))
# ---------------- SETTINGS ----------------
@app.route("/update_config", methods=['POST'])
def update_config():
    bot_tasks.BotConfig.delay = float(request.form["delay"])
    bot_tasks.BotConfig.threshold = float(request.form["threshold"])
    log.append(f"Updated config: delay={bot_tasks.BotConfig.delay}, threshold={bot_tasks.BotConfig.threshold}")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

