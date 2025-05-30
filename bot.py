import os
import telebot

# قراءة التوكن ومعرف الأدمن من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN:
    raise Exception("❌ متغير البيئة BOT_TOKEN غير موجود!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def reply_all(message):
    reply = "مرحبًا! تم استلام رسالتك ✅"

    # إرسال نسخة من الرسالة إلى الأدمن (اختياري)
    if ADMIN_ID:
        try:
            bot.send_message(ADMIN_ID, f"📩 رسالة من {message.from_user.first_name}: {message.text}")
        except Exception as e:
            print(f"فشل في إرسال الرسالة للأدمن: {e}")

    bot.reply_to(message, reply)

bot.polling()
