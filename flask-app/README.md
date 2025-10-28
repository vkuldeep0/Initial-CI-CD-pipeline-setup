# Flask + Redis + Postgres (Docker Compose)

This project demonstrates a multi-container setup using Docker Compose:
- Flask (Python web app)
- Redis (in-memory cache)
- Postgres (relational database)

## Features
- Simple Flask app that increments a Redis counter and writes a visit row to Postgres.
- Dockerfile builds the Flask image.
- docker-compose.yml orchestrates all services and their network.
- Postgres uses a named volume to persist data.

## Run locally
1. Build and start:
   ```bash
   docker compose up --build
   ```
2. Visit: http//localhost:5000
3. Stop:
	docker compose down

# Files
- app.py : Flask application and DB/Redis logic
- Dockerfile : image build instructions
- docker-compose.yml - service definitions
- Adding CI\CD pipeline
