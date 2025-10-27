from flask import Flask
import redis
import psycopg2
import os

app = Flask(__name__)

# Configuration via environment variables (Compose injects these)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

# Create Redis Client (connections are lazy)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_db_connection():
	return psycopg2.connect(
		host=DB_HOST,
		database=DB_NAME,
		user=DB_USER,
		password=DB_PASS
	)

@app.route("/")
def home():
	# Redis: increment a counter
	r.incr("hits")
	hits = r.get("hits")

	# Postgres: create a table if not exists and insert a row
	conn = get_db_connection()
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS visits (
			id SERIAL PRIMARY KEY,
			message TEXT,
			created_at TIMESTAMP DEFAULT NOW()
		);
	""")
	cur.execute("INSERT INTO visits (message) VALUES (%s)", ("Visited",))
	conn.commit()
	cur.execute("SELECT COUNT(*) FROM visits;")
	count = cur.fetchone()[0]
	cur.close()
	conn.close()

	return f"""
	<h1>Flask + Redis + Postgres</h1>
	<p>Redis hits: {hits}</p>
	<p>Postgres rows in visits: {count}</p>
	"""

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
