import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# التوكن الخاص بك
TOKEN = "7771451287:AAE4iDPqGNlFOSc0coAPImDa3XuVikyHJUM"

# تسجيل الأخطاء والمعلومات
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# بيانات المستخدم المؤقتة
user_data = {}

# القوائم الكاملة
currencies = ["EUR/USD OTC", "USD/JPY OTC", "AUD/CAD OTC", "GBP/USD OTC", "USD/CHF OTC", "NZD/USD OTC"]
timeframes = ["5 ثواني", "10 ثواني", "15 ثانية", "30 ثانية", "1 دقيقة", "2 دقيقة", "5 دقائق"]
durations = ["10 ثواني", "30 ثانية", "1 دقيقة", "2 دقيقة", "3 دقائق", "5 دقائق"]

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(c)] for c in currencies]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("اختر العملة:", reply_markup=reply_markup)

# اختيار العملة
async def handle_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {"currency": update.message.text}
    keyboard = [[KeyboardButton(t)] for t in timeframes]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("اختر الفريم الزمني:", reply_markup=reply_markup)

# اختيار الفريم
async def handle_timeframe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]["timeframe"] = update.message.text
    keyboard = [[KeyboardButton(d)] for d in durations]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("اختر مدة الصفقة:", reply_markup=reply_markup)

# اختيار المدة
async def handle_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id]["duration"] = update.message.text
    await update.message.reply_text(
        f"""تم اختيار:
عملة: {user_data[chat_id]["currency"]}
فريم: {user_data[chat_id]["timeframe"]}
مدة الصفقة: {user_data[chat_id]["duration"]}
اضغط 🔽 لتحليل السوق""")

# تحليل السوق
async def handle_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 جاري تحليل السوق الحقيقي...\n(يرجى الانتظار لحظات)")
    await update.message.reply_text("📊 القرار الذكي: (سيتم استكماله في المرحلة القادمة)")

# التشغيل الرئيسي
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^(EUR/USD OTC|USD/JPY OTC|AUD/CAD OTC|GBP/USD OTC|USD/CHF OTC|NZD/USD OTC)$"), handle_currency))
    app.add_handler(MessageHandler(filters.Regex("^(5 ثواني|10 ثواني|15 ثانية|30 ثانية|1 دقيقة|2 دقيقة|5 دقائق)$"), handle_timeframe))
    app.add_handler(MessageHandler(filters.Regex("^(10 ثواني|30 ثانية|1 دقيقة|2 دقيقة|3 دقائق|5 دقائق)$"), handle_duration))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_analysis))

    app.run_polling()

if __name__ == "__main__":
    main()
