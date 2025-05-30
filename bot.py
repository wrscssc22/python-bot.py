import os
from dotenv import load_dotenv
import telebot

# تحميل متغيرات البيئة
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("❌ متغير BOT_TOKEN غير موجود!")

bot = telebot.TeleBot(TOKEN)

# قاموس الكلمات المفتاحية وردودها
RESPONSES = {
    "مرحبا": "أهلًا وسهلًا! كيف أقدر أساعدك؟",
    "أهلاً": "أهلًا بك! يسعدني تواصلك 🌸",
    "زواج": "💍 لدينا عروض مميزة للزواج، راسلينا للتفاصيل.",
    "حناء": "🌿 نقش الحناء متاح بأنواع خليجية ويمنية.",
    "السعر": "💰 الأسعار تختلف حسب نوع الخدمة. تواصل معنا لمعرفة المزيد.",
    "الأسعار": "💰 الأسعار تختلف حسب نوع الخدمة. تواصل معنا لمعرفة المزيد.",
}

# دالة لاختيار الرد المناسب
def get_response(text):
    for keyword, response in RESPONSES.items():
        if keyword in text:
            return response
    return "شكرًا لرسالتك! يرجى توضيح سؤالك أكثر 😊"

# الرد على أي رسالة بناءً على الكلمات المفتاحية
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.lower()
    reply = get_response(user_text)
    bot.reply_to(message, reply)

bot.polling()
