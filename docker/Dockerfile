FROM python:3

RUN apt-get update && apt-get install -y snap firefox-esr wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

RUN echo 'import os' > config.py
RUN echo 'token_telegram = os.environ["TOKEN_TELEGRAM"]' >> config.py
RUN echo 'urlRU = os.environ["URL_RU"]' >> config.py
RUN echo 'logging_level = 20' >> config.py
RUN echo 'logging_file = None' >> config.py
RUN echo 'scraping_hour = int(os.environ["SCRAPING_HOUR"])' >> config.py
RUN echo 'id_feedback_chat = int(os.environ["ID_FEEDBACK_CHAT"])' >> config.py

CMD ["python", "./bot_telegram.py"]
