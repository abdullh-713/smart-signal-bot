import os
from telegram.ext import ApplicationBuilder, CommandHandler

# استخدم التوكن من المتغير البيئي
TOKEN = os.environ.get("TOKEN")

async def start(update, context):
    await update.message.reply_text("🤖 البوت يعمل الآن بنجاح!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
