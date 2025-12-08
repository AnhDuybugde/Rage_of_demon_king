from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import bot_tasks
import subprocess


app = Flask(__name__)
log = []


# ---------------- MAIN PAGE ----------------
@app.route("/")
def index():
    return render_template("index.html", log=log,
                           delay=bot_tasks.BotConfig.delay,
                           threshold=bot_tasks.BotConfig.threshold)


@app.route("/tap", methods=["GET"])
def tap():
    x = request.args.get("x")
    y = request.args.get("y")
    if not x or not y:
        return jsonify({"status": "error", "message": "Missing x or y"}), 400

    # chạy lệnh adb tap
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
    return jsonify({"status": "ok", "x": x, "y": y})

# ---------------- TASKS ----------------
@app.route("/run_daily")
def run_daily():
    result = bot_tasks.auto_daily()
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_side_tasks")
def run_side_tasks():
    result = bot_tasks.auto_side_tasks()
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_guild_bosss")
def run_guild_bosss():
    result = bot_tasks.auto_guild_bosss()
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_guild")
def run_guild():
    result = bot_tasks.auto_guild()
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_arena")
def run_arena():
    result = bot_tasks.auto_arena()
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_trial_fire")
def run_trial_fire():
    result = bot_tasks.auto_trial(["fire"]) 
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_trial_water")
def run_trial_water():
    result = bot_tasks.auto_trial(["water"])
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_trial_wind")
def run_trial_wind():
    result = bot_tasks.auto_trial(["wind"])
    log.append(result)
    return redirect(url_for('index'))

@app.route("/run_trial_oni")
def run_trial_oni():
    result = bot_tasks.auto_trial(["oni"])
    log.append(result)
    return redirect(url_for('index'))

# ---------------- SETTINGS ----------------
@app.route("/update_config", methods=['POST'])
def update_config():
    bot_tasks.BotConfig.delay = float(request.form["delay"])
    bot_tasks.BotConfig.threshold = float(request.form["threshold"])
    log.append(f"Updated config: delay={bot_tasks.BotConfig.delay}, threshold={bot_tasks.BotConfig.threshold}")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
