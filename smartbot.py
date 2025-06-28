from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# مراحل المحادثة
SELECTING_ACTION, AWAITING_IMAGE = range(2)

# واجهة الأزرار
main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📊 تحليل السوق")],
        [KeyboardButton("📷 تحليل مباشر"), KeyboardButton("🎥 بث مباشر")]
    ],
    resize_keyboard=True
)

# عند البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك في Smart Signal AI\nاختر من الأزرار:", reply_markup=main_menu)
    return SELECTING_ACTION

# تحليل السوق الوهمي
async def analyze_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 جارٍ تحليل السوق الحقيقي...\n(يرجى الانتظار)")
    await update.message.reply_text("📈 القرار الذكي: صعود (اختبار)")
    return SELECTING_ACTION

# طلب تحليل مباشر
async def ask_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 أرسل الآن صورة الشارت لتحليل مباشر")
    return AWAITING_IMAGE

# رسالة بث مباشر
async def live_stream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 البث المباشر مفعّل\n"
        "🔎 شارك شاشتك أو التقط صورة لتحليل ذكي"
    )
    return AWAITING_IMAGE

# تحليل الصورة
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 تم استلام الصورة\n⏳ جارٍ التحليل...")
    await update.message.reply_text("✅ التحليل: الاتجاه المتوقع = 📉 هبوط (تجريبي)")
    return SELECTING_ACTION

# إلغاء
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء. أرسل /start للعودة.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # المحادثة الرئيسية
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: MessageHandler(filters.TEXT & filters.Regex("تحليل السوق"), analyze_market)
            | MessageHandler(filters.Regex("تحليل مباشر"), ask_image)
            | MessageHandler(filters.Regex("بث مباشر"), live_stream),
            AWAITING_IMAGE: MessageHandler(filters.PHOTO, photo_handler)
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    # استقبال أي صورة في أي وقت
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    app.run_polling()
