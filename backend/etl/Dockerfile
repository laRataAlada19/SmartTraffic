# Start from Python image
FROM python:3.13-slim

WORKDIR /app

# These are relative to build context (./backend/etl)
COPY . . 

RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron procps

# Copy crontab file — this must exist *inside* ./backend/etl
COPY crontab_etl.txt /etc/cron.d/etl-cron
RUN chmod 0644 /etc/cron.d/etl-cron && crontab /etc/cron.d/etl-cron

# Ensure python3 points correctly
RUN ln -s /usr/local/bin/python /usr/bin/python3

# Make sure scripts are executable
RUN chmod +x /app/etl_process.py

# Create log file
RUN touch /var/log/cron_etl.log

CMD ["cron", "-f"]