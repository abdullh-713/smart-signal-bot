import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# التوكن الخاص بك
TOKEN = "7771451287:AAE4iDpGNlF0Sc0coAPImDa3XuVikyHJUM"

# المراحل
SELECT_CURRENCY, SELECT_TIMEFRAME, SELECT_DURATION = range(3)

# إعداد سجل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# قائمة العملات OTC الحقيقية
currencies = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC",
    "USD/CHF OTC", "EUR/JPY OTC", "EUR/GBP OTC", "GBP/JPY OTC", "NZD/USD OTC",
    "Gold OTC", "Silver OTC", "BTC/USD OTC", "ETH/USD OTC"
]

# جميع الفريمات المتاحة
timeframes = ["5 ثواني", "10 ثواني", "30 ثانية", "1 دقيقة", "2 دقيقة", "5 دقائق", "15 دقيقة"]

# مدد الصفقات
durations = ["30 ثانية", "1 دقيقة", "2 دقيقة", "3 دقائق", "5 دقائق", "10 دقائق"]

# حفظ الحالة لكل مستخدم
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[c] for c in currencies], resize_keyboard=True)
    await update.message.reply_text("اختر العملة:", reply_markup=reply_markup)
    return SELECT_CURRENCY

async def select_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {'currency': update.message.text}
    reply_markup = ReplyKeyboardMarkup([[t] for t in timeframes], resize_keyboard=True)
    await update.message.reply_text("اختر الفريم الزمني:", reply_markup=reply_markup)
    return SELECT_TIMEFRAME

async def select_timeframe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id]['timeframe'] = update.message.text
    reply_markup = ReplyKeyboardMarkup([[d] for d in durations], resize_keyboard=True)
    await update.message.reply_text("اختر مدة الصفقة:", reply_markup=reply_markup)
    return SELECT_DURATION

async def select_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id]['duration'] = update.message.text
    data = user_data[update.effective_chat.id]
    
    # هنا سيتم تنفيذ التحليل الفعلي لاحقاً
    result = "🔍 جاري تحليل السوق...\n\n📊 العملة: {}\n🕓 الفريم: {}\n⏱️ المدة: {}\n\n📈 القرار: صعود ✅".format(
        data['currency'], data['timeframe'], data['duration']
    )
    
    await update.message.reply_text(result)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية. اكتب /start للبدء من جديد.")
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_CURRENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_currency)],
            SELECT_TIMEFRAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_timeframe)],
            SELECT_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_duration)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()
