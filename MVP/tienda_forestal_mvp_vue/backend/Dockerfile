FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

CMD ["python", "run.py"]

