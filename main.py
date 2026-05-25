import telebot
from telebot import types
import threading
import os

# الإعدادات
API_TOKEN = os.getenv('API_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
bot = telebot.TeleBot(API_TOKEN)

TEXTS = {
    'ar': {
        'welcome': "🛡️ أهلاً بك في نظام الوساطة.",
        'main_menu': "كيف يمكنني مساعدتك؟",
        'start_btn': "🚀 بدء صفقة جديدة",
        'summary': "✅ *تم فتح الطلب!*\n\nالخدمة: {s}\nالطرف الآخر: {p}\nالمبلغ: {a} USDT\n\n⚠️ *تنبيه:* محفظتنا تقبل USDT على شبكة **Solana (SPL)** فقط!",
        'confirm_receipt': "✅ *تم التأكيد!* جاري فحص الخدمة (30 دقيقة).",
        'dispute_btn': "🚨 فتح نزاع (Dispute)",
        'dispute_alert': "🚨 *تنبيه نزاع!* المشتري يبلغ عن مشكلة."
    }
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"))
    bot.send_message(message.chat.id, "🛡️ أهلاً بك في نظام الوساطة.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "lang_ar")
def lang_ar(call):
    user_data[call.message.chat.id] = {'lang': 'ar'}
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🚀 بدء صفقة جديدة", callback_data="new_order"))
    bot.edit_message_text("كيف يمكنني مساعدتك؟", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def ask_service(call):
    bot.send_message(call.message.chat.id, "📦 ما هي الخدمة؟")
    bot.register_next_step_handler(call.message, get_partner)

def get_partner(message):
    user_data[message.chat.id] = {'service': message.text}
    bot.send_message(message.chat.id, "👤 يوزر الطرف الآخر:")
    bot.register_next_step_handler(message, get_amount)

def get_amount(message):
    user_data[message.chat.id]['partner'] = message.text
    bot.send_message(message.chat.id, "💰 المبلغ بالـ USDT:")
    bot.register_next_step_handler(message, finish_order)

def finish_order(message):
    amount = message.text
    d = user_data[message.chat.id]
    msg = TEXTS['ar']['summary'].format(s=d['service'], p=d['partner'], a=amount)
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ تأكيد استلام الخدمة", callback_data="confirm_receipt"))
    bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_receipt")
def user_confirmed(call):
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🚨 فتح نزاع", callback_data="dispute_request"))
    bot.edit_message_text(TEXTS['ar']['confirm_receipt'], call.message.chat.id, call.message.message_id, reply_markup=markup)
    threading.Timer(1800, lambda: notify_admin(call.message.chat.id, call.from_user.username)).start()

@bot.callback_query_handler(func=lambda call: call.data == "dispute_request")
def dispute_request(call):
    bot.send_message(ADMIN_ID, "🚨 *نزاع!* المشتري يبلغ عن مشكلة.")
    bot.answer_callback_query(call.id, "تم إبلاغ الإدارة.")

def notify_admin(chat_id, username):
    bot.send_message(ADMIN_ID, f"🔔 انتهت الـ 30 دقيقة للطلب الخاص بـ @{username}.")

if __name__ == '__main__':
    bot.polling(none_stop=True)

