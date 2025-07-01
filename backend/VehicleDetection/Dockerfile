FROM python:3.13-slim

WORKDIR /app
COPY ./ ./

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ultralytics lap

# Install cron and other utilities
RUN apt-get update && apt-get install -y \
    cron \
    procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up crontab
COPY crontab_vehicle.txt /etc/cron.d/vehicle-cron
RUN chmod 0644 /etc/cron.d/vehicle-cron && crontab /etc/cron.d/vehicle-cron

RUN chmod +x /app/check_new_videos.py

# Create log file
RUN touch /var/log/cron_VehicleDetection.log && chmod 666 /var/log/cron_VehicleDetection.log

CMD ["cron", "-f"]

ENV DOCKER_ENV=true
ENV WATCH_DIR=/app/backend/VehicleDetection/videos
