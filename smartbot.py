import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# استخدام التوكن من متغير بيئي
TOKEN = os.getenv("TOKEN")

# إعدادات التسجيل (logs)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# قائمة العملات OTC
OTC_SYMBOLS = [
    "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "NZDUSD_otc",
    "EURJPY_otc", "GBPJPY_otc", "AUDCAD_otc", "AUDUSD_otc",
    "EURGBP_otc", "EURNZD_otc", "CADCHF_otc", "GBPNZD_otc"
]

# قائمة الفريمات الزمنية
TIMEFRAMES = ["5s", "10s", "15s", "30s", "1m", "2m", "3m", "5m"]

# مدد الصفقات
TRADE_DURATIONS = ["10s", "30s", "1m", "2m", "3m", "5m"]

# حفظ حالة المستخدم
user_state = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(symbol, callback_data=symbol)] for symbol in OTC_SYMBOLS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 اختر العملة OTC التي تريد تحليلها:", reply_markup=reply_markup)

# عند اختيار العملة
async def handle_symbol_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    symbol = query.data
    user_state[query.from_user.id] = {"symbol": symbol}

    keyboard = [[InlineKeyboardButton(tf, callback_data=f"timeframe:{tf}")] for tf in TIMEFRAMES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"✅ العملة المختارة: {symbol}\n\nالآن اختر الفريم الزمني:", reply_markup=reply_markup)

# عند اختيار الفريم
async def handle_timeframe_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    tf = query.data.split(":")[1]
    user_state[query.from_user.id]["timeframe"] = tf

    keyboard = [[InlineKeyboardButton(dur, callback_data=f"duration:{dur}")] for dur in TRADE_DURATIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"✅ فريم: {tf}\n\nاختر مدة الصفقة:", reply_markup=reply_markup)

# عند اختيار المدة
async def handle_duration_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    dur = query.data.split(":")[1]
    user_state[query.from_user.id]["duration"] = dur

    symbol = user_state[query.from_user.id]["symbol"]
    tf = user_state[query.from_user.id]["timeframe"]

    # تحليل وهمي (placeholder)
    decision = "📈 صعود"  # أو 📉 هبوط أو ⏸️ انتظار

    await query.edit_message_text(
        f"✅ الإعدادات:\nعملة: {symbol}\nالفريم: {tf}\nالمدة: {dur}\n\n📊 النتيجة: {decision}"
    )

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_symbol_selection, pattern="^(?!timeframe:|duration:).+"))
    app.add_handler(CallbackQueryHandler(handle_timeframe_selection, pattern="^timeframe:"))
    app.add_handler(CallbackQueryHandler(handle_duration_selection, pattern="^duration:"))

    app.run_polling()

if __name__ == "__main__":
    main()
