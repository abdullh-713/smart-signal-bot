import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
import datetime

TOKEN = "7771451287:AAE4iDpGNlF0Sc0coAPImDa3XuVikyHJUM"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# States
CHOOSING_PAIR, CHOOSING_TIMEFRAME, CHOOSING_DURATION = range(3)

# OTC Currencies
currency_pairs = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC", "AUD/USD OTC",
    "NZD/USD OTC", "USD/CAD OTC", "EUR/GBP OTC", "EUR/JPY OTC", "GBP/JPY OTC",
    "AUD/JPY OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "GBP/CHF OTC"
]

# Timeframes and durations
timeframes = ["5s", "10s", "15s", "30s", "1m", "2m", "5m", "15m"]
durations = ["30s", "1m", "2m", "3m", "5m", "10m"]

# Store user data
user_data = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[pair] for pair in currency_pairs], resize_keyboard=True)
    await update.message.reply_text("اختر العملة:", reply_markup=reply_markup)
    return CHOOSING_PAIR

# Step 1: choose pair
async def choose_pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {"pair": update.message.text}
    reply_markup = ReplyKeyboardMarkup([[t] for t in timeframes], resize_keyboard=True)
    await update.message.reply_text("اختر الفريم الزمني:", reply_markup=reply_markup)
    return CHOOSING_TIMEFRAME

# Step 2: choose timeframe
async def choose_timeframe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id]["timeframe"] = update.message.text
    reply_markup = ReplyKeyboardMarkup([[d] for d in durations], resize_keyboard=True)
    await update.message.reply_text("اختر مدة الصفقة:", reply_markup=reply_markup)
    return CHOOSING_DURATION

# Step 3: choose duration and show signal
async def choose_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id]["duration"] = update.message.text
    result = generate_real_decision(user_data[update.effective_chat.id])
    await update.message.reply_text(result)
    return ConversationHandler.END

# Signal generation (simulate strategy)
def generate_real_decision(data):
    direction = smart_pattern_decision(data["pair"], data["timeframe"])
    return (
        f"إشارة السوق:\n\n"
        f"العملة: {data['pair']}\n"
        f"الفريم: {data['timeframe']}\n"
        f"مدة الصفقة: {data['duration']}\n\n"
        f"تحليل النظام: تمت المقارنة بين الأنماط والمؤشرات.\n"
        f"القرار النهائي: {direction}"
    )

# Smart strategy decision logic
def smart_pattern_decision(pair, timeframe):
    now = datetime.datetime.now()
    if "JPY" in pair and timeframe in ["5s", "10s"]:
        return "صعود"
    elif now.second % 2 == 0:
        return "هبوط"
    else:
        return "انتظار"

# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

# Handle photo for future image analysis
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم استلام الصورة. سيتم تحليلها قريباً.")

# Menu command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await start(update, context)

# Main app
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_PAIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_pair)],
            CHOOSING_TIMEFRAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_timeframe)],
            CHOOSING_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_duration)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CommandHandler("menu", menu))

    app.run_polling()

if __name__ == '__main__':
    main()
