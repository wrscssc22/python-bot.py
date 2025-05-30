import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# تحميل بيانات المستخدمين
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = str(user.id)
    args = context.args
    referrer_id = args[0] if args else None

    if chat_id not in users:
        users[chat_id] = {"balance": 0, "referrals": []}

        # نظام الإحالة
        if referrer_id and referrer_id != chat_id and referrer_id in users:
            users[referrer_id]["balance"] += 15
            users[referrer_id]["referrals"].append(chat_id)
            await context.bot.send_message(
                chat_id=int(referrer_id),
                text=f"🎉 لقد حصلت على 15 دولار لإحالة {user.first_name}"
            )
        save_users()

    referral_link = f"https://t.me/{context.bot.username}?start={chat_id}"
    keyboard = [
        ["👤 الحساب", "💰 ربح المال من دعوة الاصدقاء 💰"],
        ["🏦 سحب الأرباح", "🎁 المكافأة"],
        ["🔎 ما هذا البوت", "📍 مشاهدة الإعلانات"]
    ]
    await update.message.reply_text(
        f"🔥 قم بمشاركة هذا الرابط للحصول على 15 دولار عن كل إحالة 👇\n{referral_link}\n\n"
        "💵 الحد الأدنى للسحب هو 500 دولار",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# التعامل مع الأزرار
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_user.id)
    text = update.message.text
    u = users.get(chat_id, {"balance": 0, "referrals": []})

    if text == "👤 الحساب":
        await update.message.reply_text(f"💼 حسابك:\nالرصيد: {u['balance']} دولار\nالإحالات: {len(u['referrals'])}")
    elif text == "💰 ربح المال من دعوة الاصدقاء 💰":
        link = f"https://t.me/{context.bot.username}?start={chat_id}"
        await update.message.reply_text(f"🔗 رابط الإحالة الخاص بك:\n{link}")
    elif text == "🏦 سحب الأرباح":
        if u["balance"] >= 500:
            await update.message.reply_text("✅ تم إرسال طلبك. سنتواصل معك خلال 24 ساعة.")
            # إعلام الأدمن
            await context.bot.send_message(ADMIN_ID, f"💸 طلب سحب جديد من: {update.effective_user.full_name} (ID: {chat_id})\nالرصيد: {u['balance']} دولار")
        else:
            await update.message.reply_text(f"❌ الحد الأدنى للسحب هو 500 دولار. رصيدك: {u['balance']} دولار")
    elif text == "🎁 المكافأة":
        await update.message.reply_text("🎁 لا توجد مكافآت حالياً. تابعنا لاحقاً.")
    elif text == "🔎 ما هذا البوت":
        await update.message.reply_text("🤖 هذا البوت يمكنك من كسب المال من خلال دعوة الأصدقاء.")
    elif text == "📍 مشاهدة الإعلانات":
        await update.message.reply_text("📢 لا توجد إعلانات حالياً.")
    else:
        pass

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعمل الآن...")
    app.run_polling()
