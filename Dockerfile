FROM python:3.11-slim
LABEL maintainer="tironvadim1@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update && apt-get install -y \
    cron \
    gcc \
    zlib1g-dev \
    libjpeg-dev \
    musl-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ADD crontab /etc/cron.d/telegram_monitor_cron
RUN chmod 0644 /etc/cron.d/telegram_monitor_cron
RUN crontab /etc/cron.d/telegram_monitor_cron
RUN touch /var/log/cron.log
