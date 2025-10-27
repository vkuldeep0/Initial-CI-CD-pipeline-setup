FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy app after installing deps
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
