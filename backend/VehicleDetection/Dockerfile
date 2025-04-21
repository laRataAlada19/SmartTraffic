FROM python:3.13-slim

WORKDIR /app
COPY ./ ./

# Install only necessary Python packages for watching
RUN pip install --no-cache-dir -r requirements.txt

# Install cron and basic utilities
RUN apt-get update && apt-get install -y \
    cron \
    procps \
    && apt-get clean

# Set up crontab for VehicleDetection
COPY crontab_vehicle.txt /etc/cron.d/vehicle-cron
RUN chmod 0644 /etc/cron.d/vehicle-cron && crontab /etc/cron.d/vehicle-cron

# Make sure script is executable
RUN chmod +x /app/check_new_videos.py

# Create log file with appropriate permissions
RUN touch /var/log/cron_VehicleDetection.log && chmod 666 /var/log/cron_VehicleDetection.log

CMD ["cron", "-f"]

ENV DOCKER_ENV=true
ENV WATCH_DIR=/app/backend/VehicleDetection/videos/cam1