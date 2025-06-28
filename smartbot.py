import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ.get("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 مرحبًا بك في Smart Signal AI - البوت يعمل!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠 اكتب /start لبدء البوت. أرسل صورة لتحليل السوق.")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 تم استلام الصورة! يتم الآن تحليل السوق...")

    # هنا مستقبلاً نضيف كود تحليل الصورة والتوقع الذكي (صعود/هبوط/انتظار)
    await update.message.reply_text("📊 النتيجة: صعود ✅ (مثال توضيحي)")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    app.run_polling()


if __name__ == "__main__":
    main()
