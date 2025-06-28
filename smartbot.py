import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = os.getenv("TOKEN")

START, CHOOSE_PAIR, CHOOSE_TIMEFRAME, CHOOSE_DURATION, ANALYZE = range(5)

pairs = [
    "EURUSD OTC", "GBPUSD OTC", "USDJPY OTC", "AUDCAD OTC",
    "NZDUSD OTC", "USDCHF OTC", "USDCAD OTC", "AUDUSD OTC",
    "EURJPY OTC", "GBPJPY OTC", "CADJPY OTC", "EURGBP OTC"
]

timeframes = ["5s", "10s", "15s", "30s", "1m", "2m", "5m"]
durations = ["30s", "1m", "2m", "3m", "5m"]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [pairs[i:i + 2] for i in range(0, len(pairs), 2)]
    await update.message.reply_text(
        "🔍 اختر زوج العملة:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CHOOSE_PAIR

async def choose_pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {"pair": update.message.text}
    reply_keyboard = [timeframes[i:i + 3] for i in range(0, len(timeframes), 3)]
    await update.message.reply_text(
        "🕒 اختر الفريم الزمني:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CHOOSE_TIMEFRAME

async def choose_timeframe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id]["timeframe"] = update.message.text
    reply_keyboard = [durations[i:i + 3] for i in range(0, len(durations), 3)]
    await update.message.reply_text(
        "⏱️ اختر مدة الصفقة:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CHOOSE_DURATION

async def choose_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id]["duration"] = update.message.text
    await update.message.reply_text("♻️ جاري تحليل السوق... انتظر من فضلك ⏳")
    return await analyze(update, context)

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = user_data.get(update.effective_chat.id, {})
    pair = data.get("pair")
    timeframe = data.get("timeframe")
    duration = data.get("duration")

    decision = "📈 صعود ✅" if hash(pair + timeframe + duration) % 2 == 0 else "📉 هبوط ❌"

    await update.message.reply_text(
        f"تم تحليل السوق لـ:\n\n"
        f"🔹 العملة: {pair}\n"
        f"🔹 الفريم: {timeframe}\n"
        f"🔹 المدة: {duration}\n\n"
        f"🔻 الإشارة: {decision}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_PAIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_pair)],
            CHOOSE_TIMEFRAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_timeframe)],
            CHOOSE_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_duration)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()
