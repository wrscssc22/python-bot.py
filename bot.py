import os
from dotenv import load_dotenv
import telebot

# تحميل متغيرات البيئة
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    raise Exception("❌ BOT_TOKEN أو ADMIN_ID غير موجود في .env")

ADMIN_ID = int(ADMIN_ID)
bot = telebot.TeleBot(TOKEN)

# قاموس الردود حسب الكلمات المفتاحية (يتم تحديثه ديناميكيًا من الأدمن)
RESPONSES = {
    "مرحبا": "👋 أهلًا وسهلًا! كيف أقدر أساعدك؟",
    "أهلاً": "🌸 أهلًا بك! يسعدني تواصلك.",
    "السلام": "🍍 وعليكم السلام ورحمة الله وبركاته.",
    "زواج": "💍 لدينا عروض مميزة للزواج، تواصل معنا للتفاصيل.",
    "حناء": "🌿 نقش الحناء متاح بأنواع خليجية ويمنية فخمة.",
    "السعر": "💰 الأسعار تختلف حسب نوع الخدمة. راسلنا لمعرفة التفاصيل.",
    "الأسعار": "💰 الأسعار تختلف حسب نوع الخدمة. راسلنا لمعرفة التفاصيل.",
    "موقع": "📍 نحن متواجدون في صنعاء - للتحديد بدقة يرجى مراسلتنا.",
    "حجز": "📆 للحجز يرجى إرسال الاسم والخدمة المطلوبة والتاريخ.",
    "رقم": "📞 للتواصل معنا عبر الواتساب: 777xxxxxxx",
    "واتس": "📱 راسلينا على واتساب من خلال هذا الرابط: https://wa.me/967777xxxxxx",
    "عرض": "🔥 عروضنا الحالية: خصم 20٪ على جميع الخدمات هذا الشهر!",
    "تجربة": "✨ يمكن ترتيب تجربة مجانية حسب التوفر. راسلينا لحجز الموعد.",
    "متى": "🕒 نحن متواجدون من الساعة 9 صباحًا حتى 9 مساءً يوميًا.",
    "شكرا": "🙏 عفوًا! تحت أمرك في أي وقت.",
    "شكرًا": "😊 على الرحب والسعة!",
    "كم": "💬 يرجى تحديد نوع الخدمة لمعرفة السعر بدقة.",
    "وين": "📍 موقعنا في صنعاء - وسنرسل لك الموقع عند الحجز."
}

# دالة للبحث عن رد مناسب
def get_response(text):
    for keyword, response in RESPONSES.items():
        if keyword in text:
            return response
    return "🤖 شكرًا لرسالتك! يرجى توضيح سؤالك أكثر لنتمكن من خدمتك."

# التعامل مع أي رسالة
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.lower()
    user_id = message.from_user.id

    # أوامر الأدمن
    if user_id == ADMIN_ID:
        if user_text.startswith("/اضف "):
            try:
                parts = user_text[5:].split("=>")
                if len(parts) != 2:
                    raise ValueError
                keyword = parts[0].strip()
                reply = parts[1].strip()
                RESPONSES[keyword] = reply
                bot.reply_to(message, f"✅ تم إضافة الرد:\n{keyword} => {reply}")
            except:
                bot.reply_to(message, "❌ الصيغة غير صحيحة. استخدم: /اضف كلمة => الرد")
            return

        elif user_text.startswith("/حذف "):
            keyword = user_text[6:].strip()
            if keyword in RESPONSES:
                del RESPONSES[keyword]
                bot.reply_to(message, f"🗑️ تم حذف الرد المرتبط بـ: {keyword}")
            else:
                bot.reply_to(message, "❌ لم يتم العثور على هذه الكلمة.")
            return

        elif user_text.startswith("/الردود"):
            if RESPONSES:
                msg = "📋 قائمة الردود الحالية:\n"
                for k, v in RESPONSES.items():
                    msg += f"- {k} => {v}\n"
                bot.reply_to(message, msg)
            else:
                bot.reply_to(message, "📭 لا توجد ردود بعد.")
            return

        elif user_text.startswith("/مساعدة"):
            help_text = (
                "🛠️ أوامر لوحة تحكم الأدمن:\n\n"
                "/اضف كلمة => الرد  - لإضافة رد تلقائي\n"
                "/حذف كلمة           - لحذف رد\n"
                "/الردود             - عرض كل الردود\n"
                "/مساعدة             - عرض هذه الرسالة"
            )
            bot.reply_to(message, help_text)
            return

    # رد عادي
    reply = get_response(user_text)
    bot.reply_to(message, reply)

bot.polling()
