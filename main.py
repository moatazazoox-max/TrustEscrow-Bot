import telebot
from telebot import types
import threading
import os

API_TOKEN = os.getenv('API_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
bot = telebot.TeleBot(API_TOKEN)

# نصوص البوت
TEXTS = {
    'welcome': "🛡️ أهلاً بك في نظام الوساطة الآمن.",
    'terms': "📄 **شروط الأمان:**\n1. لا نتعامل خارج المنصة.\n2. يتم التأكد من التحويل خلال 30 دقيقة.\n3. محفظتنا تدعم Solana (SPL) فقط.",
    'summary': "✅ *تم فتح الطلب!*\n\nالخدمة: {s}\nالطرف الآخر: {p}\nالمبلغ: {a} USDT\n\n⚠️ *تنبيه:* محفظتنا تقبل USDT على شبكة **Solana (SPL)** فقط!",
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"))
    bot.send_message(message.chat.id, TEXTS['welcome'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "lang_ar")
def lang_ar(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🚀 بدء صفقة جديدة", callback_data="new_order"),
               types.InlineKeyboardButton("📄 شروط الأمان", callback_data="show_terms"))
    bot.edit_message_text("كيف يمكنني مساعدتك؟", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "show_terms")
def show_terms(call):
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="lang_ar"))
    bot.edit_message_text(TEXTS['terms'], call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

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
    d = user_data[message.chat.id]
    amount = message.text
    msg = TEXTS['summary'].format(s=d['service'], p=d['partner'], a=amount)
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ تأكيد استلام الخدمة", callback_data="confirm_receipt"))
    bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_receipt")
def confirm(call):
    bot.edit_message_text("✅ *تم التأكيد!* جاري فحص الخدمة (30 دقيقة).", call.message.chat.id, call.message.message_id)
    threading.Timer(1800, lambda: bot.send_message(ADMIN_ID, f"🔔 انتهت الـ 30 دقيقة للطلب الخاص بـ {call.from_user.username}")).start()

if __name__ == '__main__':
    bot.polling(none_stop=True)

