from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import psutil
import datetime
import os

app = Flask(__name__)
DB_FILE = "system_data.db"

# Initialize Database
def init_db():
	conn = sqlite3.connect(DB_FILE)
	cur = conn.curser()
	cur.execute("""
		CREATE TABLE IF NOT EXIST stats (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			timestamp TEXT,
			cpu REAL
			memory REAL
			disk REAL
		)
	""")
	conn.commit()
	conn.close()

# Get system stats
def get_system_stats():
	return {
		"cpu": psutil.cpu_percentage(interval=1),
		"memory": psutil.virtual_memory().percent,
		"disk": psutil.disk_usage('/').percent,
		"timestamp": datetime.datetime.now().isoformat()
	}

# Save stats to DB
def save_stats():
	data = get_sytem_stats()
	conn = sqlite3.connect(DB_FILE)
	cur = conn.cursor()
	cur.execute("INSERT INTO stats (timestamp, cpu, memory, disk) VALUES (?, ?, ?, ?)",
			(data["timestamp"], data["cpu"], data["memory"], data["disk"]))
	conn.commit()
	conn.close()

# Background Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(save_stats, 'interval', seconds=60)
scheduler.start()

@app.route("/")
def home():
	return render_template("dashboard.html")

@app.route("/metrics")
def metrics():
	conn = sqlite3.conntect(DB_LITE)
	cur = conn.cursor()
	cur.execute("SELECT timestamp, cpu, memory, disk FROM stats ORDER by id DESC LIMIT 30")
	rows = cur.fetchall()
	conn.close()

	data = [{"timestamp": r[0]. "cpu": r[1], "memory": r[2], "disk": r[3]} for r in rows]
	return jsonify(data[::-1]) # reverse for chronological order

@app.route("/health")
def health():
	return {"status": "ok", "timestamp": datetime.datetime.now().isoformat()}


if __name__ == "__main__":
	init_db()
	app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
