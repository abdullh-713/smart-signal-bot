import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# التوكن الرسمي للبوت
TOKEN = "7771451287:AAE4iDpqGNLF0Sc0coAPImDa3XuVikyHJUM"

# إعدادات التسجيل (logs)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# قائمة العملات OTC (اختصرنا بعضها لتجربة)
OTC_SYMBOLS = ["EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDUSD_otc", "NZDUSD_otc", "USDCAD_otc", "USDCHF_otc"]

# قائمة الفريمات الزمنية
TIMEFRAMES = ["5s", "10s", "15s", "30s", "1m", "2m", "5m"]

# مدد الصفقات
TRADE_DURATIONS = ["10s", "30s", "1m", "2m", "3m", "5m"]

# حفظ حالة المستخدم
user_state = {}

# /start command
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton(sym, callback_data=f"symbol:{sym}")] for sym in OTC_SYMBOLS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔍 اختر عملة OTC لبدء التحليل:", reply_markup=reply_markup)

# معالج الضغط على الأزرار
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("symbol:"):
        symbol = data.split(":")[1]
        user_state[query.from_user.id] = {"symbol": symbol}
        keyboard = [[InlineKeyboardButton(tf, callback_data=f"timeframe:{tf}")] for tf in TIMEFRAMES]
        await query.edit_message_text(f"✅ العملة المختارة: {symbol}\nاختر الفريم الزمني:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("timeframe:"):
        timeframe = data.split(":")[1]
        user_state[query.from_user.id]["timeframe"] = timeframe
        keyboard = [[InlineKeyboardButton(td, callback_data=f"duration:{td}")] for td in TRADE_DURATIONS]
        await query.edit_message_text(f"✅ الفريم: {timeframe}\nاختر مدة الصفقة:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("duration:"):
        duration = data.split(":")[1]
        state = user_state.get(query.from_user.id, {})
        symbol = state.get("symbol")
        timeframe = state.get("timeframe")

        # هنا يتم التحليل الذكي المفترض
        decision = smart_decision(symbol, timeframe, duration)
        text = f"✅ العملة: {symbol}\n📊 الفريم: {timeframe}\n⏱ مدة الصفقة: {duration}\n\n📈 القرار النهائي: {decision}"
        await query.edit_message_text(text)

# وظيفة التحليل الذكي (تجريبية حالياً)
def smart_decision(symbol, timeframe, duration):
    from random import choice
    return choice(["⬆️ صعود", "⬇️ هبوط", "⏸️ انتظار"])

# استقبال الصور (تحليل مستقبلي من الشاشة)
async def handle_photo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("📷 تم استلام الصورة، سيتم تحليلها قريبًا تلقائيًا...")

# الرسائل الأخرى
async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("❓ أرسل /start لاستخدام البوت.")

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    app.run_polling()

if __name__ == "__main__":
    main()
