FROM python:3.13-slim

# Install dependencies
WORKDIR /app
COPY ./ ./
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy crontab file and apply
COPY crontab.txt /etc/cron.d/etl-cron
RUN chmod 0644 /etc/cron.d/etl-cron && crontab /etc/cron.d/etl-cron

# Give execution rights on the ETL script
RUN chmod +x /app/etl_process.py

# Create log file
RUN touch /var/log/cron_etl.log

CMD cron && tail -f /var/log/cron_etl.log
