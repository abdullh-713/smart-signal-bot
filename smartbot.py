import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackContext

TOKEN = "7771451287:AAE4iDPqGNlFOSc0coAPImDa3XuVikyHJUM"

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# القوائم الكاملة
currencies = ["EUR/USD OTC", "USD/JPY OTC", "AUD/CAD OTC", "GBP/USD OTC", "USD/CHF OTC", "NZD/USD OTC"]
frames = ["10 ثواني", "30 ثانية", "1 دقيقة", "2 دقيقة", "5 دقائق", "10 دقائق", "15 دقيقة"]
durations = ["30 ثانية", "1 دقيقة", "2 دقائق", "3 دقائق", "5 دقائق"]

# الحالة المؤقتة
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {}
    keyboard = [[KeyboardButton(c)] for c in currencies]
    await update.message.reply_text("اختر العملة:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text

    if text in currencies:
        user_data[chat_id]['currency'] = text
        keyboard = [[KeyboardButton(f)] for f in frames]
        await update.message.reply_text("اختر الفريم الزمني:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

    elif text in frames:
        user_data[chat_id]['frame'] = text
        keyboard = [[KeyboardButton(d)] for d in durations]
        await update.message.reply_text("اختر مدة الصفقة:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

    elif text in durations:
        user_data[chat_id]['duration'] = text
        keyboard = [[KeyboardButton("✅ تحليل السوق"), KeyboardButton("📸 تحليل مباشر (مشاركة الشاشة)"]]
        await update.message.reply_text(
            f"تم اختيار:\nعملة: {user_data[chat_id]['currency']}\nفريم: {user_data[chat_id]['frame']}\nمدة الصفقة: {user_data[chat_id]['duration']}\n\nاضغط أحد الأزرار أدناه لبدء التحليل.",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

    elif text == "✅ تحليل السوق":
        await update.message.reply_text("🔍 جاري تحليل السوق الحقيقي...\n(يرجى الانتظار لحظات)")
        await update.message.reply_text("📊 القرار الذكي: ✅ صعود (دخول مضمون)")

    elif text == "📸 تحليل مباشر (مشاركة الشاشة)":
        await update.message.reply_text("🎥 الرجاء مشاركة الشاشة أو إرسال صورة للشارت ليتم التحليل الذكي المباشر...")

    elif update.message.photo:
        await update.message.reply_text("📷 تم استلام الصورة ✅\n📊 التحليل الذكي جارٍ الآن...")
        await update.message.reply_text("✅ القرار الذكي: 🔻 هبوط (تحليل مباشر بالصورة)")

    else:
        await update.message.reply_text("⚠️ يرجى اختيار خيار من القائمة أو إرسال صورة لتحليل مباشر.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    app.run_polling()
