import requests
import hashlib
import time
import os
from datetime import datetime
import pytz
from telegram import Bot

URL = "https://protectietemporara.gov.md/validare/?token=aea19728a39981f7639570afcb0d68f4760fa8b51980826001656990fc40217"
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(BOT_TOKEN)

def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def fetch_page():
    return requests.get(URL, timeout=30).text

def notify(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

last_hash = None
last_daily_ping = None
tz = pytz.timezone("Europe/Chisinau")

notify("🤖 Бот запущен и следит за изменениями")

while True:
    now = datetime.now(tz)

    weekday = now.weekday() < 5
    hour = now.hour

    check = False

    if weekday and 6 <= hour <= 18:
        check = True
    elif not weekday and hour == 12:
        check = True

    if check:
        page = fetch_page()
        h = get_hash(page)
        if last_hash and h != last_hash:
            notify("⚠️ Обнаружены изменения на странице!")
        last_hash = h

    if hour == 19 and (last_daily_ping != now.date()):
        notify("Я на месте. Всё под контролем 👀")
        last_daily_ping = now.date()

    time.sleep(3600)
