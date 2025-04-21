import os
import requests
from telegram import Bot
import schedule
import time

# گرفتن توکن و آی‌دی کانال از محیط
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

# تنظیم زمان ارسال پیام (مثلاً ساعت ۱۲ ظهر)
schedule.every().day.at("12:16").do(send_prices_to_channel)

while True:
    schedule.run_pending()
    time.sleep(1)
