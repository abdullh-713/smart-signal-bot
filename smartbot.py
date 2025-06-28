import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# تفعيل السجل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
user_states = {}

# الخيارات الكاملة
currencies = [["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC"],
              ["AUD/CAD OTC", "EUR/GBP OTC", "USD/CHF OTC"],
              ["⬅️ رجوع"]]

timeframes = [["5 ثواني", "10 ثواني", "15 ثانية"],
              ["30 ثانية", "1 دقيقة", "2 دقيقة"],
              ["⬅️ رجوع"]]

durations = [["15 ثانية", "30 ثانية", "1 دقيقة"],
             ["2 دقيقة", "3 دقيقة", "5 دقائق"],
             ["⬅️ رجوع"]]

main_menu = [["💹 تحليل السوق"], ["🔁 تغيير الخيارات"]]

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_states[chat_id] = {}
    await update.message.reply_text("👋 أهلاً بك في Smart Signal AI\n\nيرجى اختيار العملة:",
        reply_markup=ReplyKeyboardMarkup(currencies, resize_keyboard=True))

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_states:
        user_states[chat_id] = {}

    state = user_states[chat_id]

    # الرجوع
    if text == "⬅️ رجوع":
        if "duration" in state:
            del state["duration"]
            await update.message.reply_text("⏳ اختر مدة الصفقة:", reply_markup=ReplyKeyboardMarkup(durations, resize_keyboard=True))
        elif "timeframe" in state:
            del state["timeframe"]
            await update.message.reply_text("⏱️ اختر الفريم الزمني:", reply_markup=ReplyKeyboardMarkup(timeframes, resize_keyboard=True))
        elif "currency" in state:
            del state["currency"]
            await update.message.reply_text("💱 اختر العملة:", reply_markup=ReplyKeyboardMarkup(currencies, resize_keyboard=True))
        return

    # تغيير الإعدادات
    if text == "🔁 تغيير الخيارات":
        await start(update, context)
        return

    # تسلسل الإعداد
    if "currency" not in state:
        state["currency"] = text
        await update.message.reply_text("⏱️ اختر الفريم الزمني:",
            reply_markup=ReplyKeyboardMarkup(timeframes, resize_keyboard=True))
    elif "timeframe" not in state:
        state["timeframe"] = text
        await update.message.reply_text("⏳ اختر مدة الصفقة:",
            reply_markup=ReplyKeyboardMarkup(durations, resize_keyboard=True))
    elif "duration" not in state:
        state["duration"] = text
        await update.message.reply_text(
            f"✅ تم اختيار:\n\n"
            f"عملة: {state['currency']}\n"
            f"فريم: {state['timeframe']}\n"
            f"مدة الصفقة: {state['duration']}\n\n"
            f"اضغط 👇 لتحليل السوق",
            reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        )
    elif text == "💹 تحليل السوق":
        await update.message.reply_text("🔍 جاري تحليل السوق الحقيقي...\n(يرجى الانتظار لحظات)")
        await update.message.reply_text("📊 القرار الذكي: (سيتم استكماله في المرحلة القادمة)")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت يعمل الآن...")
    app.run_polling()
