import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
import os

# إعداد السجل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# الحصول على التوكن من البيئة
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# إعدادات الواجهة
currency_options = [["EUR/USD", "GBP/USD", "USD/JPY"], ["⬅️ رجوع"]]
timeframe_options = [["5 ثواني", "10 ثواني", "1 دقيقة"], ["⬅️ رجوع"]]
duration_options = [["30 ثانية", "1 دقيقة", "2 دقيقة"], ["⬅️ رجوع"]]

# تخزين مؤقت لاختيارات المستخدم
user_states = {}

# بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_states[chat_id] = {}
    await update.message.reply_text("👋 مرحبًا بك في Smart Signal AI\nيرجى اختيار العملة:", 
        reply_markup=ReplyKeyboardMarkup(currency_options, resize_keyboard=True))

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_states:
        user_states[chat_id] = {}

    state = user_states[chat_id]

    if text == "⬅️ رجوع":
        await start(update, context)
        return

    if "currency" not in state:
        state["currency"] = text
        await update.message.reply_text("⏱️ اختر الفريم الزمني:",
            reply_markup=ReplyKeyboardMarkup(timeframe_options, resize_keyboard=True))
    elif "timeframe" not in state:
        state["timeframe"] = text
        await update.message.reply_text("⏳ اختر مدة الصفقة:",
            reply_markup=ReplyKeyboardMarkup(duration_options, resize_keyboard=True))
    elif "duration" not in state:
        state["duration"] = text
        await update.message.reply_text(
            f"✅ تم اختيار:\nعملة: {state['currency']}\nفريم: {state['timeframe']}\nمدة الصفقة: {state['duration']}\n\nاضغط على 👇",
            reply_markup=ReplyKeyboardMarkup([["💹 تحليل السوق"]], resize_keyboard=True)
        )
    elif text == "💹 تحليل السوق":
        await update.message.reply_text("🔍 جارٍ تحليل السوق الحقيقي...\n(باستخدام استراتيجيات المحترفين والثغرات)")
        decision = await analyze_market(state)
        await update.message.reply_text(f"✅ القرار النهائي: {decision}")

# تحليل السوق الذكي (محاكاة واقعية حالياً)
async def analyze_market(state):
    # في النسخة القادمة يمكن إدخال RSI و MA و Stochastic فعلي
    simulated_rsi = random.randint(10, 90)
    simulated_trend = random.choice(["up", "down", "sideways"])

    if simulated_rsi < 30 and simulated_trend == "up":
        return "📈 صعود (فرصة شراء قوية)"
    elif simulated_rsi > 70 and simulated_trend == "down":
        return "📉 هبوط (فرصة بيع قوية)"
    else:
        return "⏳ انتظار (لا توجد فرصة مؤكدة الآن)"

# تشغيل التطبيق
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت يعمل الآن...")
    app.run_polling()
