FROM python:3.10

WORKDIR /app

COPY smartbot.py .

RUN pip install --no-cache-dir python-telegram-bot

CMD ["python", "smartbot.py"]
