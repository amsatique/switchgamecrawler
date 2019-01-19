FROM python:2.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TELEGRAM_TOKEN
ENV TELEGRAM_CHANNEL_ID
ENV DELAY

CMD [ "python", "./crawler" ]
