import telebot
from telebot import types
import time

# التوكن يتم جلبه من Railway Variables
import os
API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8' 
bot = telebot.TeleBot(API_TOKEN)

# الإعدادات الخاصة بك
ADMIN_USERNAME = "@HE_5TE"
WALLET_ADDRESS = "D5nB2WhVgKDpS2N3Zx7uXFNV1zMqXiBh777XnQFx4kpu"

# قاموس مؤقت لحفظ الطلبات
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🤝 فتح طلب وساطة جديد", callback_data="new_order")
    markup.add(btn1)
    bot.send_message(message.chat.id, "مرحباً بك في نظام TrustEscrow الآمن 🛡️\nنحن هنا لضمان حقوقك في صفقاتك.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def new_order_start(call):
    bot.send_message(call.message.chat.id, "الرجاء إدخال اسم الخدمة أو المنتج:")
    bot.register_next_step_handler(call.message, get_service_name)

def get_service_name(message):
    user_id = message.chat.id
    user_data[user_id] = {'service': message.text}
    bot.send_message(user_id, "الآن، أدخل يوزر (Username) الطرف الآخر:")
    bot.register_next_step_handler(message, get_partner_username)

def get_partner_username(message):
    user_id = message.chat.id
    user_data[user_id]['partner'] = message.text
    bot.send_message(user_id, "أدخل مبلغ الصفقة (بـ USDT):")
    bot.register_next_step_handler(message, finish_order)

def finish_order(message):
    user_id = message.chat.id
    amount = message.text
    data = user_data[user_id]
    
    # رسالة للعميل
    summary = (f"✅ تم فتح طلب الوساطة بنجاح!\n\n"
               f"الخدمة: {data['service']}\n"
               f"الطرف الآخر: {data['partner']}\n"
               f"المبلغ: {amount} USDT\n\n"
               f"⚠️ **الرجاء إرسال المبلغ إلى المحفظة التالية:**\n`{WALLET_ADDRESS}`\n\n"
               f"بعد التحويل، تواصل مع الأدمين: {ADMIN_USERNAME}")
    
    bot.send_message(user_id, summary, parse_mode="Markdown")
    
    # رسالة تنبيه لك (الأدمين)
    alert_msg = (f"🔔 **طلب وساطة جديد!**\n"
                 f"المستخدم: @{message.from_user.username}\n"
                 f"الخدمة: {data['service']}\n"
                 f"الطرف الآخر: {data['partner']}\n"
                 f"المبلغ: {amount}")
    
    # محاولة إرسال التنبيه لك
    try:
        bot.send_message(ADMIN_USERNAME, alert_msg, parse_mode="Markdown")
    except:
        pass

if __name__ == '__main__':
    bot.polling(none_stop=True)
