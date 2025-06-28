import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler, ContextTypes

# 🧠 التوكن الخاص ببوتك
TOKEN = "7771451287:AAE4iDpGNlF0Sc0coAPImDa3XuVikyHJUM"

# 🛠️ إعدادات السجل لتتبع الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🧠 تحليل ذكي وهمي (استبدله بالخوارزميات لاحقًا)
def analyze_market(pair, timeframe, duration):
    # في الإصدار الأول: تحليل عشوائي كمثال
    from random import choice
    return choice(["📈 صعود", "📉 هبوط", "⏳ انتظار"])

# 🟢 بدء البوت
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💱 اختيار العملة", callback_data='choose_pair')],
        [InlineKeyboardButton("🕒 اختيار الفريم", callback_data='choose_timeframe')],
        [InlineKeyboardButton("⏱️ اختيار مدة الصفقة", callback_data='choose_duration')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 مرحبًا بك في بوت التحليل الذكي.\nيرجى اختيار الإعدادات:", reply_markup=reply_markup)

# 🔁 المتغيرات المؤقتة لحفظ اختيارات المستخدم
user_state = {}

# 🔘 الرد على الأزرار
async def button_handler(update: Update, context: CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == "choose_pair":
        keyboard = [
            [InlineKeyboardButton("EUR/USD", callback_data='pair_EURUSD')],
            [InlineKeyboardButton("GBP/USD", callback_data='pair_GBPUSD')],
            [InlineKeyboardButton("USD/JPY", callback_data='pair_USDJPY')],
        ]
        await query.edit_message_text("💱 اختر العملة:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("pair_"):
        pair = data.split("_")[1]
        user_state[user_id] = {"pair": pair}
        await query.edit_message_text(f"✅ تم اختيار العملة: {pair}\n\nالآن اختر الفريم:")
        keyboard = [
            [InlineKeyboardButton("5 ثواني", callback_data='tf_5s')],
            [InlineKeyboardButton("15 ثانية", callback_data='tf_15s')],
            [InlineKeyboardButton("1 دقيقة", callback_data='tf_1m')],
        ]
        await context.bot.send_message(chat_id=user_id, text="🕒 اختر الفريم الزمني:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("tf_"):
        tf = data.split("_")[1]
        user_state[user_id]["timeframe"] = tf
        await query.edit_message_text(f"✅ تم اختيار الفريم: {tf}\n\nالآن اختر مدة الصفقة:")
        keyboard = [
            [InlineKeyboardButton("30 ثانية", callback_data='dur_30s')],
            [InlineKeyboardButton("60 ثانية", callback_data='dur_60s')],
        ]
        await context.bot.send_message(chat_id=user_id, text="⏱️ اختر مدة الصفقة:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("dur_"):
        dur = data.split("_")[1]
        user_state[user_id]["duration"] = dur

        pair = user_state[user_id]["pair"]
        tf = user_state[user_id]["timeframe"]

        decision = analyze_market(pair, tf, dur)
        await query.edit_message_text(f"✅ تم اختيار المدة: {dur}\n\n📊 تحليل السوق جاري...")
        await context.bot.send_message(chat_id=user_id, text=f"📌 الزوج: {pair}\n🕒 الفريم: {tf}\n⏱️ المدة: {dur}\n\n🎯 القرار: {decision}")

# 🚀 تشغيل البوت
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
