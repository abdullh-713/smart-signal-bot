import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

TOKEN = '7771451287:AAE4iDpGNlF0Sc0coAPImDa3XuVikyHJUM'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة بدء التشغيل
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 اختر نوع العملة", callback_data='choose_asset')],
        [InlineKeyboardButton("⏱️ اختر الفريم الزمني", callback_data='choose_timeframe')],
        [InlineKeyboardButton("📈 اختر مدة الصفقة", callback_data='choose_duration')],
        [InlineKeyboardButton("🚀 تحليل الآن", callback_data='analyze')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 مرحباً بك في SmartPatternX_bot\nاختر ما تريد:", reply_markup=reply_markup)

# دالة لمعالجة الضغط على الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'choose_asset':
        await query.edit_message_text("✅ تم اختيار العملة: EURUSD (مثال)")
    elif query.data == 'choose_timeframe':
        await query.edit_message_text("✅ تم اختيار الفريم: 1 دقيقة")
    elif query.data == 'choose_duration':
        await query.edit_message_text("✅ تم اختيار مدة الصفقة: 2 دقيقة")
    elif query.data == 'analyze':
        await query.edit_message_text("🔍 يتم الآن تحليل السوق...\n📉 القرار: هبوط مضمون")

# تشغيل البوت
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()
