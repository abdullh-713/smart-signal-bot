import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CHOOSING_PAIR, CHOOSING_TIMEFRAME, CHOOSING_DURATION, ANALYZING = range(4)

currency_pairs = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC",
    "USD/CAD OTC", "EUR/JPY OTC", "NZD/USD OTC", "USD/CHF OTC"
]

timeframes = ["5 ثواني", "10 ثواني", "15 ثانية", "30 ثانية", "1 دقيقة", "2 دقيقة", "5 دقائق"]
durations = ["30 ثانية", "1 دقيقة", "2 دقيقة", "3 دقائق", "5 دقائق"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    reply_markup = ReplyKeyboardMarkup([[c] for c in currency_pairs] + [["رجوع"]], resize_keyboard=True)
    await update.message.reply_text("🔹 اختر العملة:", reply_markup=reply_markup)
    return CHOOSING_PAIR

async def choose_pair(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "رجوع":
        return await start(update, context)
    if text not in currency_pairs:
        await update.message.reply_text("⚠️ اختر عملة من القائمة.")
        return CHOOSING_PAIR
    context.user_data['pair'] = text
    reply_markup = ReplyKeyboardMarkup([[t] for t in timeframes] + [["رجوع"]], resize_keyboard=True)
    await update.message.reply_text("🕐 اختر الفريم الزمني:", reply_markup=reply_markup)
    return CHOOSING_TIMEFRAME

async def choose_timeframe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "رجوع":
        return await start(update, context)
    if text not in timeframes:
        await update.message.reply_text("⚠️ اختر فريم زمني من القائمة.")
        return CHOOSING_TIMEFRAME
    context.user_data['timeframe'] = text
    reply_markup = ReplyKeyboardMarkup([[d] for d in durations] + [["رجوع"]], resize_keyboard=True)
    await update.message.reply_text("⌛ اختر مدة الصفقة:", reply_markup=reply_markup)
    return CHOOSING_DURATION

async def choose_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "رجوع":
        reply_markup = ReplyKeyboardMarkup([[t] for t in timeframes] + [["رجوع"]], resize_keyboard=True)
        await update.message.reply_text("🕐 اختر الفريم الزمني:", reply_markup=reply_markup)
        return CHOOSING_TIMEFRAME
    if text not in durations:
        await update.message.reply_text("⚠️ اختر مدة من القائمة.")
        return CHOOSING_DURATION
    context.user_data['duration'] = text

    pair = context.user_data['pair']
    timeframe = context.user_data['timeframe']
    duration = context.user_data['duration']

    await update.message.reply_text(f"✅ تم اختيار:\n\n"
                                    f"💱 العملة: {pair}\n"
                                    f"⏱ الفريم الزمني: {timeframe}\n"
                                    f"⏳ مدة الصفقة: {duration}\n\n"
                                    f"🔍 تحليل السوق قيد التنفيذ...")

    from random import choice
    signal = choice(["📈 صعود", "📉 هبوط", "⏸ انتظار"])
    await update.message.reply_text(f"📊 نتيجة التحليل: {signal}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ تم إلغاء العملية. اكتب /start للبدء من جديد.")
    return ConversationHandler.END

if __name__ == '__main__':
    import asyncio

    async def main():
        app = ApplicationBuilder().token("7771451287:AAE4iDpGNlF0Sc0coAPImDa3XuVikyHJUM").build()

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
        print("🤖 Bot is running...")
        await app.run_polling()

    asyncio.run(main())
