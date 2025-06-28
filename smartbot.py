import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ قراءة التوكن من متغير البيئة
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# ✅ الرد على أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال! أهلاً بك في Smart Signal Bot 🚀")

# ✅ نقطة تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
