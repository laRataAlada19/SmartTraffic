FROM python:3.13-slim

# Install dependencies
WORKDIR /app
COPY ./ ./
RUN pip install --no-cache-dir -r requirements.txt

# Ensure python3 is available (for cron jobs)
RUN ln -s /usr/local/bin/python /usr/bin/python3

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy crontab file and apply
COPY crontab.txt /etc/cron.d/VehicleDetection-cron
RUN chmod 0644 /etc/cron.d/VehicleDetection-cron && crontab /etc/cron.d/VehicleDetection-cron

# Give execution rights on the script
RUN chmod +x /app/main.py

# Create log file
RUN touch /var/log/cron_VehicleDetection.log

CMD cron && tail -f /var/log/cron_VehicleDetection.log
