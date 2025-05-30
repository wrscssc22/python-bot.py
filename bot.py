import os
import json
from datetime import datetime, timedelta
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

def get_user_data(chat_id):
    if chat_id not in users:
        users[chat_id] = {
            "balance": 0,
            "referrals": [],
            "last_reward": None
        }
    return users[chat_id]

# التحقق من آخر مكافأة
def can_get_daily_reward(user_data):
    last = user_data["last_reward"]
    if not last:
        return True
    last_time = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - last_time >= timedelta(days=1)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_user.id)
    args = context.args
    ref = args[0] if args else None

    user = get_user_data(chat_id)

    # الإحالة
    if ref and ref != chat_id and ref in users and chat_id not in users[ref]["referrals"]:
        users[ref]["balance"] += 15
        users[ref]["referrals"].append(chat_id)
        await context.bot.send_message(chat_id=int(ref), text=f"🎉 لقد حصلت على 15 دولار من إحالة جديدة!")

    save_users()

    link = f"https://t.me/{context.bot.username}?start={chat_id}"
    keyboard = [
        ["👤 الحساب", "🎁 المكافأة اليومية"],
        ["💰 ربح المال من دعوة الاصدقاء 💰", "🏦 سحب الأرباح"],
        ["🔎 ما هذا البوت", "📍 مشاهدة الإعلانات"]
    ]
    await update.message.reply_text(
        f"🔥 شارك رابط الإحالة لكسب المال!\n{link}\n\n"
        f"🎁 تحصل على 5 دولار يوميًا عند الضغط على '🎁 المكافأة اليومية'",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# الأزرار
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_user.id)
    text = update.message.text
    user = get_user_data(chat_id)

    if text == "👤 الحساب":
        await update.message.reply_text(
            f"💼 حسابك:\nرصيدك: {user['balance']} دولار\nالإحالات: {len(user['referrals'])}"
        )

    elif text == "🎁 المكافأة اليومية":
        if can_get_daily_reward(user):
            user["balance"] += 5
            user["last_reward"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_users()
            await update.message.reply_text("✅ تم إضافة 5 دولار إلى رصيدك!")
        else:
            await update.message.reply_text("⏳ لقد حصلت على المكافأة اليوم، عد بعد 24 ساعة!")

    elif text == "💰 ربح المال من دعوة الاصدقاء 💰":
        link = f"https://t.me/{context.bot.username}?start={chat_id}"
        await update.message.reply_text(f"🔗 رابط الإحالة الخاص بك:\n{link}")

    elif text == "🏦 سحب الأرباح":
        if user["balance"] >= 500:
            await update.message.reply_text("✅ تم تقديم طلبك، سيتم مراجعته خلال 24 ساعة.")
            await context.bot.send_message(ADMIN_ID, f"🔔 طلب سحب من {chat_id}\nالرصيد: {user['balance']}")
        else:
            await update.message.reply_text("❌ يجب أن يكون لديك 500 دولار على الأقل للسحب.")

    elif text == "🔎 ما هذا البوت":
        await update.message.reply_text("🤖 بوت لربح المال من الإحالات والمكافآت اليومية.")

    elif text == "📍 مشاهدة الإعلانات":
        await update.message.reply_text("📢 لا توجد إعلانات حالياً.")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعمل الآن...")
    app.run_polling()
