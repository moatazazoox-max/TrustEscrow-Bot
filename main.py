import telebot
from telebot import types
import os

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇦🇪 العربية", callback_data="lang_ar"))
    bot.send_message(message.chat.id, "🛡️ أهلاً بك في نظام الوساطة.\nWelcome to Escrow System.\n\nالرجاء اختيار اللغة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "lang_ar")
def lang_ar(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 بدء صفقة جديدة", callback_data="new_order"))
    bot.edit_message_text("⚙️ **القائمة الرئيسية:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def ask_service(call):
    user_data[call.message.chat.id] = {}
    bot.send_message(call.message.chat.id, "📦 ما هي الخدمة التي تريدها؟")
    bot.register_next_step_handler(call.message, get_partner)

def get_partner(message):
    user_data[message.chat.id]['service'] = message.text
    bot.send_message(message.chat.id, "👤 أرسل يوزر الطرف الآخر (المعرف):")
    bot.register_next_step_handler(message, get_amount)

def get_amount(message):
    user_data[message.chat.id]['partner'] = message.text
    bot.send_message(message.chat.id, "💰 كم المبلغ بالـ USDT؟")
    bot.register_next_step_handler(message, finish_order)

def finish_order(message):
    d = user_data.get(message.chat.id, {})
    amount = message.text
    msg = f"✅ **تم إنشاء الطلب بنجاح!**\n\n📦 الخدمة: {d.get('service')}\n👤 الطرف الآخر: {d.get('partner')}\n💰 المبلغ: {amount} USDT"
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    if message.chat.id in user_data: del user_data[message.chat.id]

if __name__ == '__main__':
    bot.polling(none_stop=True)
