import telebot
from telebot import types
import os

# ضع التوكن الخاص بك هنا
API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8'
bot = telebot.TeleBot(API_TOKEN)

ADMIN_USERNAME = "@HE_5TE"
WALLET_ADDRESS = "D5nB2WhVgKDpS2N3Zx7uXFNV1zMqXiBh777XnQFx4kpu"
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_ar = types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    markup.add(btn_ar, btn_en)
    bot.send_message(message.chat.id, "مرحباً بك في TrustEscrow! اختر لغتك:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_lang(call):
    lang = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup(row_width=1)
    if lang == 'ar':
        markup.add(types.InlineKeyboardButton("🤝 فتح طلب وساطة جديد", callback_data="new_order"),
                   types.InlineKeyboardButton("📄 شروط الخدمة", callback_data="terms_ar"))
    else:
        markup.add(types.InlineKeyboardButton("🤝 Open New Escrow", callback_data="new_order"),
                   types.InlineKeyboardButton("📄 Terms of Service", callback_data="terms_en"))
    bot.edit_message_text("اختر ما تريد:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('terms_'))
def show_terms(call):
    lang = call.data.split('_')[1]
    text = "🛡️ شروطنا: نحن وسيط محايد، نأخذ عمولة 3%، ونحفظ المال بأمان." if lang == 'ar' else "🛡️ Our Terms: We are a neutral mediator, 3% fee, secure holding."
    bot.answer_callback_query(call.id, text, show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def new_order_start(call):
    bot.send_message(call.message.chat.id, "الرجاء إدخال اسم الخدمة:")
    bot.register_next_step_handler(call.message, get_service_name)

def get_service_name(message):
    user_data[message.chat.id] = {'service': message.text}
    bot.send_message(message.chat.id, "أدخل يوزر الطرف الآخر:")
    bot.register_next_step_handler(message, get_partner_username)

def get_partner_username(message):
    user_data[message.chat.id]['partner'] = message.text
    bot.send_message(message.chat.id, "أدخل مبلغ الصفقة الإجمالي:")
    bot.register_next_step_handler(message, finish_order)

def finish_order(message):
    amount_str = message.text
    user_id = message.chat.id
    data = user_data.get(user_id, {})
    
    summary = (f"✅ تفاصيل طلبك:\n\nالخدمة: {data.get('service')}\nالطرف الآخر: {data.get('partner')}\nالمبلغ الإجمالي: {amount_str} USDT\n"
               f"العمولة: 3% (تُخصم)\n\n⚠️ أرسل المبلغ لمحفظتنا:\n`{WALLET_ADDRESS}`\n\n
