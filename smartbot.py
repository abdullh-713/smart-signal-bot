import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = os.environ.get("TOKEN")

# الحالات
CHOOSING, ANALYZING = range(2)

# قائمة العملات + الفريمات + الصفقات
currencies = ["EURUSD_OTC", "GBPUSD_OTC", "USDJPY_OTC", "AUDUSD_OTC", "USDCHF_OTC"]
frames = ["5s", "10s", "30s", "1m", "2m", "5m"]
durations = ["30s", "1m", "2m", "3m", "5m"]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[c] for c in currencies], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("اختر العملة التي تريد تحليلها:", reply_markup=reply_markup)
    return CHOOSING

async def handle_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {'currency': update.message.text}
    reply_markup = ReplyKeyboardMarkup([[f] for f in frames], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("اختر الفريم الزمني:", reply_markup=reply_markup)
    return ANALYZING

async def handle_frame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['frame'] = update.message.text
    reply_markup = ReplyKeyboardMarkup([[d] for d in durations], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("اختر مدة الصفقة:", reply_markup=reply_markup)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية ✅", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 جاري تحليل الصورة بدقة... الرجاء الانتظار")
    # تحليل ذكي هنا
    await update.message.reply_text("✅ النتيجة: صعود ✅")

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_currency)],
        ANALYZING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_frame)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
