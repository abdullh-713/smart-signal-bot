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

# التوكن من المتغير البيئي
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# مراحل المحادثة
SELECTING_ACTION, AWAITING_IMAGE = range(2)

# قائمة الأزرار الرئيسية
menu_buttons = [
    [KeyboardButton("📊 تحليل السوق")],
    [KeyboardButton("📷 تحليل مباشر"), KeyboardButton("🎥 بث مباشر")],
]

reply_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في 🧠 Smart Signal AI\nاختر من الأزرار أدناه:",
        reply_markup=reply_markup
    )
    return SELECTING_ACTION

# تحليل السوق الوهمي (سيتم تطويره لاحقاً)
async def market_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 جارٍ تحليل السوق الحقيقي...\n(يرجى الانتظار)")
    await update.message.reply_text("📈 القرار الذكي: صعود (اختبار)")
    return SELECTING_ACTION

# طلب صورة يدوياً
async def image_analysis_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 أرسل الآن صورة واضحة للشارت لتحليل السوق")
    return AWAITING_IMAGE

# زر البث المباشر
async def live_stream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 تم تفعيل وضع التحليل المباشر!\n"
        "✅ شارك شاشة المنصة الآن.\n"
        "📸 التقط صورة أو انتظر التفعيل التلقائي.\n"
        "⚠️ تأكد من وجود: RSI + Bollinger + MA + Stochastic"
    )
    return AWAITING_IMAGE

# تحليل الصورة (سواء من زر أو إرسال مباشر)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 يتم تحليل الصورة الآن...")
    # (مكان التحليل الحقيقي للصورة)
    await update.message.reply_text("✅ تم التحليل: 📉 الاتجاه المتوقع = هبوط (محاكاة)")
    return SELECTING_ACTION

# إلغاء العملية
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم إلغاء العملية. أرسل /start للعودة.")
    return ConversationHandler.END

# تشغيل التطبيق
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: MessageHandler(
                filters.TEXT & filters.Regex("^(📊 تحليل السوق)$"), market_analysis
            )
            | MessageHandler(filters.Regex("^(📷 تحليل مباشر)$"), image_analysis_request)
            | MessageHandler(filters.Regex("^(🎥 بث مباشر)$"), live_stream),
            AWAITING_IMAGE: MessageHandler(filters.PHOTO, handle_photo),
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # استجابة لأي صورة مباشرة خارج المحادثة
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()
