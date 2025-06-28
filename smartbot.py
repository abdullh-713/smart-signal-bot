import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import random

# Telegram Bot Token
TOKEN = "7771451287:AAE4iDpGNlF0Sc0coAPImDa3XuVikyHJUM"
bot = telebot.TeleBot(TOKEN)

# الحالة المؤقتة لتخزين البيانات بين الخطوات
user_data = {}

@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🔁 تحليل جديد"))
    bot.send_message(chat_id, "👋 مرحبًا بك في SmartPatternX_bot!\nاختر ما تريد:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "🔁 تحليل جديد")
def step_asset(msg):
    chat_id = msg.chat.id
    user_data[chat_id] = {}
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("EURUSD", "GBPJPY", "USDJPY")
    bot.send_message(chat_id, "💱 اختر العملة:", reply_markup=markup)
    bot.register_next_step_handler(msg, step_timeframe)

def step_timeframe(msg):
    chat_id = msg.chat.id
    user_data[chat_id]["asset"] = msg.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("5 ثواني", "10 ثواني", "1 دقيقة")
    bot.send_message(chat_id, "⏱️ اختر الفريم الزمني:", reply_markup=markup)
    bot.register_next_step_handler(msg, step_duration)

def step_duration(msg):
    chat_id = msg.chat.id
    user_data[chat_id]["timeframe"] = msg.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("30", "60", "120")
    bot.send_message(chat_id, "⏳ اختر مدة الصفقة (بالثواني):", reply_markup=markup)
    bot.register_next_step_handler(msg, final_result)

def final_result(msg):
    chat_id = msg.chat.id
    user_data[chat_id]["duration"] = msg.text

    asset = user_data[chat_id]["asset"]
    timeframe = user_data[chat_id]["timeframe"]
    duration = user_data[chat_id]["duration"]

    # تحليل ذكي (تجريبي)
    decision = random.choice(["📈 صعود", "📉 هبوط", "⏳ انتظار"])
    result = f"✅ التحليل الذكي للعملة {asset}\nالفريم: {timeframe}\nالمدة: {duration} ثانية\n\n📌 القرار: {decision}"
    bot.send_message(chat_id, result)

@bot.message_handler(content_types=['photo', 'document'])
def handle_image(msg):
    bot.send_message(msg.chat.id, "📷 تم استلام الصورة. سيتم دعم التحليل المباشر من الشاشة قريبًا.")

print("✅ البوت قيد التشغيل...")
bot.infinity_polling()
