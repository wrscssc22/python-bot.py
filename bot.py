import os
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# قراءة التوكن والمعرف من متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # اجعلها رقم صحيح

# تخزين الرقم السري لكل مستخدم
user_secrets = {}

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    secret = random.randint(1, 10)
    user_secrets[chat_id] = secret
    update.message.reply_text("🎯 خمن رقم من 1 إلى 10!")

def guess(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_secrets:
        update.message.reply_text("أرسل /start لتبدأ اللعبة.")
        return

    try:
        guess = int(text)
    except ValueError:
        update.message.reply_text("رجاءً أرسل رقم فقط.")
        return

    secret = user_secrets[chat_id]

    if guess == secret:
        update.message.reply_text(f"🎉 صحيح! الرقم هو {secret}. أرسل /start للعب من جديد.")
        del user_secrets[chat_id]
    else:
        update.message.reply_text("❌ خطأ! حاول رقم ثاني.")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN غير موجود في متغيرات البيئة.")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, guess))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
