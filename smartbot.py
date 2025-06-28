import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

keyboard = [
    ["💹 تحليل السوق"],
    ["📈 صعود", "📉 هبوط"],
    ["⏳ انتظار"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك في Smart Signal AI 📊\nاختر من الأزرار أدناه:", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💹 تحليل السوق":
        await update.message.reply_text("🔍 جارٍ تحليل السوق... (محاكاة فقط)")
    elif text == "📈 صعود":
        await update.message.reply_text("✅ تم تأكيد الاتجاه: صعود 🚀")
    elif text == "📉 هبوط":
        await update.message.reply_text("✅ تم تأكيد الاتجاه: هبوط 📉")
    elif text == "⏳ انتظار":
        await update.message.reply_text("⏱ يُفضل الانتظار حالياً.")
    else:
        await update.message.reply_text("⚠️ أمر غير معروف. الرجاء استخدام الأزرار فقط.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
