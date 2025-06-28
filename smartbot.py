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
    "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDUSD_otc", "USDCHF_otc",
    "NZDUSD_otc", "EURJPY_otc", "GBPJPY_otc", "EURGBP_otc", "USDCAD_otc"
]

# قائمة الفريمات الزمنية
TIMEFRAMES = ["5s", "10s", "15s", "30s", "1m", "2m", "5m", "10m"]

# مدد الصفقات
TRADE_DURATIONS = ["10s", "30s", "1m", "2m", "3m", "5m"]

# حفظ حالة المستخدم
user_state = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(symbol, callback_data=f"symbol|{symbol}")]
                for symbol in OTC_SYMBOLS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 اختر العملة التي تريد تحليلها:", reply_markup=reply_markup)

# التعامل مع الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("|")
    action, value = data[0], data[1]

    chat_id = query.message.chat_id
    if chat_id not in user_state:
        user_state[chat_id] = {}

    if action == "symbol":
        user_state[chat_id]["symbol"] = value
        keyboard = [[InlineKeyboardButton(tf, callback_data=f"timeframe|{tf}")] for tf in TIMEFRAMES]
        await query.edit_message_text("⏱ اختر الفريم الزمني:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "timeframe":
        user_state[chat_id]["timeframe"] = value
        keyboard = [[InlineKeyboardButton(dur, callback_data=f"duration|{dur}")] for dur in TRADE_DURATIONS]
        await query.edit_message_text("⏳ اختر مدة الصفقة:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == "duration":
        user_state[chat_id]["duration"] = value
        state = user_state[chat_id]
        msg = (
            f"✅ تم اختيار الإعدادات التالية:\n"
            f"🔹 العملة: {state['symbol']}\n"
            f"🔹 الفريم الزمني: {state['timeframe']}\n"
            f"🔹 مدة الصفقة: {state['duration']}\n\n"
            f"🔍 جارٍ تحليل السوق...\n"
            f"📊 النتيجة: 🔽 *انتظار قرار التحليل الذكي*"
        )
        await query.edit_message_text(msg, parse_mode="Markdown")

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
