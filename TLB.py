import os
import requests
from telegram import Bot
import schedule
import time

# خواندن متغیرهای محیطی که در Render تنظیم کردی
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def get_prices():
    url = "https://api.tgju.org/v1/market/summary"
    response = requests.get(url)
    data = response.json()["results"]

    prices = {
        "دلار": data["price_dollar_rl"]["p"],
        "تتر": data["price_tether_irr"]["p"],
        "یورو": data["price_eur"]["p"],
        "بیت‌کوین": data["crypto-bitcoin"]["p"],
        "طلا ۱۸ عیار": data["geram18"]["p"],
        "سکه امامی": data["sekeb"]["p"],
        "سکه بهار آزادی": data["sekeh"]["p"]
    }

    return prices

def send_prices_to_channel():
    bot = Bot(token=TOKEN)
    prices = get_prices()
    message = "قیمت‌های امروز:\n\n" + "\n".join([f"{k}: {v} تومان" for k, v in prices.items()])
    bot.send_message(chat_id=CHANNEL_ID, text=message)

schedule.every().day.at("12:15").do(send_prices_to_channel)  # زمان دلخواهتو بزار

while True:
    schedule.run_pending()
    time.sleep(1)
