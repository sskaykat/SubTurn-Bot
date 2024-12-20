FROM python:3.9-slim-buster

WORKDIR /sub2clashbot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./bot.py" ]
