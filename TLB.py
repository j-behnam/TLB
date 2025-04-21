import telebot

# توکن ربات تلگرام خود را جایگزین کنید
API_TOKEN = '7679987839:AAFV6sETH78re1aDiS6fEHY8OJyK0aQGVGA'

# تنظیم پروکسی یا VPN
telebot.apihelper.proxy = {'https': 'http://103.251.166.55:2096/sub/User1-Safe?format=json'}

bot = telebot.TeleBot(API_TOKEN)

# مدیریت پیام "/start"
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! لطفاً پیام خود را ارسال کنید.")

# مدیریت پیام‌های دریافتی از کاربران
@bot.message_handler(func=lambda message: True)
def forward_message_to_admin(message):
    username = message.from_user.username if message.from_user.username else "کاربر بدون یوزرنیم"
    # ارسال پیام کاربر به مدیر
    bot.send_message(ADMIN_CHAT_ID, f"پیام جدید از @{username}:\n{message.text}")
    # اطلاع‌رسانی به کاربر
    bot.send_message(message.chat.id, "پیام شما به مدیر ارسال شد. لطفاً منتظر پاسخ باشید.")

# مدیریت پیام‌های دریافتی از مدیر
@bot.message_handler(func=lambda message: message.chat.id == int(ADMIN_CHAT_ID))
def send_response_to_user(message):
    try:
        # پیام باید به فرمت "@username: پاسخ شما" باشد
        if ":" in message.text:
            username, response = message.text.split(":", 1)
            username = username.strip().replace("@", "")  # حذف @ اگر وجود داشته باشد
            response = response.strip()

            # ارسال پاسخ به کاربر بر اساس یوزرنیم
            user_found = False
            for chat_id in bot.get_chat_ids():
                user = bot.get_chat(chat_id)
                if user.username == username:
                    bot.send_message(user.id, response)
                    user_found = True
                    break

            if user_found:
                bot.send_message(ADMIN_CHAT_ID, f"پاسخ شما برای @{username} ارسال شد.")
            else:
                bot.send_message(ADMIN_CHAT_ID, f"کاربر با یوزرنیم @{username} پیدا نشد.")
        else:
            bot.send_message(ADMIN_CHAT_ID, "لطفاً پیام را به فرمت '@username: پاسخ' ارسال کنید.")
    except Exception as e:
        bot.send_message(ADMIN_CHAT_ID, f"خطایی رخ داد: {e}")

# اجرای ربات
bot.polling()
