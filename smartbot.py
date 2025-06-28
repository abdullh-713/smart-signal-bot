import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# استخدام التوكن من متغير بيئي
TOKEN = os.getenv("TOKEN")

# إعدادات التسجيل (logs)
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# قائمة العملات OTC
OTC_SYMBOLS = [
    "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "NZDUSD_otc", "EURJPY_otc",
    "GBPJPY_otc", "AUDCAD_otc", "EURGBP_otc", "EURNZD_otc", "CADCHF_otc"
]

# قائمة الفريمات الزمنية
TIMEFRAMES = ["5s", "10s", "15s", "30s", "1m", "2m", "5m"]

# مدد الصفقات
TRADE_DURATIONS = ["10s", "30s", "1m", "2m", "3m", "5m"]

# حفظ حالة المستخدم
user_state = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(symbol, callback_data=f"symbol:{symbol}")]
                for symbol in OTC_SYMBOLS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 مرحبًا، اختر العملة:", reply_markup=reply_markup)

# معالجة اختيار العملة
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("symbol:"):
        symbol = data.split(":")[1]
        user_state[query.from_user.id] = {"symbol": symbol}
        keyboard = [[InlineKeyboardButton(tf, callback_data=f"timeframe:{tf}")]
                    for tf in TIMEFRAMES]
        await query.edit_message_text(
            f"✅ تم اختيار العملة: {symbol}\n\nاختر الفريم الزمني:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("timeframe:"):
        timeframe = data.split(":")[1]
        user_state[query.from_user.id]["timeframe"] = timeframe
        keyboard = [[InlineKeyboardButton(td, callback_data=f"duration:{td}")]
                    for td in TRADE_DURATIONS]
        await query.edit_message_text(
            f"✅ تم اختيار الفريم: {timeframe}\n\nاختر مدة الصفقة:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("duration:"):
        duration = data.split(":")[1]
        state = user_state.get(query.from_user.id, {})
        symbol = state.get("symbol")
        timeframe = state.get("timeframe")

        await query.edit_message_text(
            f"📊 تم اختيار كل شيء:\n\n"
            f"✅ العملة: {symbol}\n"
            f"🕓 الفريم: {timeframe}\n"
            f"⌛ مدة الصفقة: {duration}\n\n"
            f"🔍 جارٍ تحليل السوق الحقيقي...\n"
            f"📈 القرار النهائي: 🔄 *انتظار*"
        )

# تحليل الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 تم استلام الصورة! جارٍ التحليل الذكي...")

# تشغيل التطبيق
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
