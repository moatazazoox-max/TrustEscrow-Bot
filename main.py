import telebot
from telebot import types
import datetime

# إعدادات البوت
API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8'
bot = telebot.TeleBot(API_TOKEN)

ADMIN_USERNAME = "@HE_5TE"
WALLET_ADDRESS = "D5nB2WhVgKDpS2N3Zx7uXFNV1zMqXiBh777XnQFx4kpu"
user_data = {}

# وظيفة لحفظ السجلات (بدون قاعدة بيانات معقدة)
def save_order(user_id, service, partner, amount):
    with open("orders_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | ID: {user_id} | الخدمة: {service} | الطرف الآخر: {partner} | المبلغ: {amount} USDT\n")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤝 فتح طلب وساطة جديد", callback_data="new_order"))
    bot.send_message(message.chat.id, "مرحباً بك في TrustEscrow! نحن وسيطك الآمن.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def new_order(call):
    bot.send_message(call.message.chat.id, "أدخل اسم الخدمة:")
    bot.register_next_step_handler(call.message, get_service)

def get_service(message):
    user_data[message.chat.id] = {'service': message.text}
    bot.send_message(message.chat.id, "أدخل يوزر الطرف الآخر:")
    bot.register_next_step_handler(message, get_partner)

def get_partner(message):
    user_data[message.chat.id]['partner'] = message.text
    bot.send_message(message.chat.id, "أدخل مبلغ الصفقة:")
    bot.register_next_step_handler(message, confirm_order)

def confirm_order(message):
    amount = message.text
    user_id = message.chat.id
    data = user_data.get(user_id)
    
    # حفظ الصفقة في السجل
    save_order(user_id, data['service'], data['partner'], amount)
    
    summary = (f"✅ تم فتح طلب وساطة!\n\n"
               f"الخدمة: {data['service']}\n"
               f"الطرف الآخر: {data['partner']}\n"
               f"المبلغ: {amount} USDT\n\n"
               f"⚠️ أرسل المبلغ للمحفظة:\n`{WALLET_ADDRESS}`\n\n"
               f"بعد التحويل، تواصل مع الأدمين: {ADMIN_USERNAME}")
    
    bot.send_message(user_id, summary, parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"🔔 طلب جديد!\nالمشتري: {message.from_user.username}\nالخدمة: {data['service']}\nالمبلغ: {amount}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
