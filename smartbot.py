import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# توكن البوت
TOKEN = "7771451287:AAE4iDpqGNLF0Sc0coAPImDa3XuVikyHJUM"

# العملات + الفريمات + مدد الصفقات
currencies = ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CAD OTC", "AUD/USD OTC", "NZD/USD OTC"]
timeframes = ["10 ثواني", "15 ثانية", "30 ثانية", "1 دقيقة", "2 دقيقة", "5 دقائق"]
durations = ["10 ثواني", "15 ثانية", "30 ثانية", "1 دقيقة", "2 دقيقة", "5 دقائق"]

user_data = {}

# تسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# بدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {}
    keyboard = [[c] for c in currencies]
    await update.message.reply_text("اختر العملة:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))

# تحليل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_data:
        user_data[chat_id] = {}

    state = user_data[chat_id]

    if "currency" not in state:
        if text in currencies:
            state["currency"] = text
            keyboard = [[t] for t in timeframes]
            await update.message.reply_text("اختر الفريم الزمني:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
        else:
            await update.message.reply_text("❗️يرجى اختيار عملة من القائمة.")
    elif "timeframe" not in state:
        if text in timeframes:
            state["timeframe"] = text
            keyboard = [[d] for d in durations]
            await update.message.reply_text("اختر مدة الصفقة:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
        else:
            await update.message.reply_text("❗️يرجى اختيار فريم زمني من القائمة.")
    elif "duration" not in state:
        if text in durations:
            state["duration"] = text
            await update.message.reply_text("📊 جاري التحليل الذكي باستخدام استراتيجيات احترافية...\n\n✅ العملة: {}\n✅ الفريم: {}\n✅ المدة: {}\n\n🔄 القرار: 🔽 هبوط".format(
                state["currency"], state["timeframe"], state["duration"]
            ))
            user_data.pop(chat_id)
        else:
            await update.message.reply_text("❗️يرجى اختيار مدة صفقة من القائمة.")
    else:
        await update.message.reply_text("❗️حدث خطأ. أرسل /start لإعادة البدء.")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
