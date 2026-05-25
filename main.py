import telebot
from telebot import types
import threading
import os

API_TOKEN = os.getenv('API_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
bot = telebot.TeleBot(API_TOKEN)

# نصوص احترافية
TEXTS = {
    'welcome': (
        "```\n"
        "╔══════════════════════╗\n"
        "║     TRUST ESCROW     ║\n"
        "╚══════════════════════╝\n"
        "```\n\n"
        "🛡️ **Welcome to TrustEscrow**\n"
        "Your secure mediator for digital transactions.\n\n"
        "🛡️ **مرحباً بك في TrustEscrow**\n"
        "نظام الوساطة الأكثر أماناً للمعاملات الرقمية.\n\n"
        "--- اختر لغتك / Choose your language ---"
    ),
    'main_ar': "⚙️ **القائمة الرئيسية - Main Menu**\nكيف يمكنني مساعدتك اليوم؟",
    'terms': "📄 **شروط وأحكام الأمان:**\n\n🔹 1. لا نتعامل خارج المنصة لضمان حقوقك.\n🔹 2. يتم فحص وتأكيد التحويلات خلال **30 دقيقة** عمل.\n🔹 3. محفظتنا تدعم شبكة **Solana (SPL)** فقط.\n\n⚠️ *الالتزام بالشروط يحمي أموالك.*",
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🇦🇪 العربية", callback_data="lang_ar"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    bot.send_message(message.chat.id, TEXTS['welcome'], parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "lang_ar")
def lang_ar(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🚀 بدء صفقة جديدة | New Trade", callback_data="new_order"),
        types.InlineKeyboardButton("📄 شروط الأمان | Terms", callback_data="show_terms")
    )
    bot.edit_message_text(TEXTS['main_ar'], call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "show_terms")
def show_terms(call):
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع | Back", callback_data="lang_ar"))
    bot.edit_message_text(TEXTS['terms'], call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

# دوال الصفقة
@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def ask_service(call):
    bot.send_message(call.message.chat.id, "📦 **الخدمة؟ / Service Description?**")
    bot.register_next_step_handler(call.message, get_partner)

def get_partner(message):
    user_data = {message.chat.id: {'service': message.text}}
    bot.send_message(message.chat.id, "👤 **يوزر الطرف الآخر؟ / Partner Telegram Username?**")
    bot.register_next_step_handler(message, lambda m: get_amount(m, user_data))

def get_amount(message, user_data):
    user_data[message.chat.id]['partner'] = message.text
    bot.send_message(message.chat.id, "💰 **المبلغ بالـ USDT? / Amount in USDT?**")
    bot.register_next_step_handler(message, lambda m: finish_order(m, user_data))

def finish_order(message, user_data):
    d = user_data[message.chat.id]
    msg = f"✅ **تم فتح الطلب! / Order Created!**\n\n📦 الخدمة: {d['service']}\n👤 الطرف الآخر: {d['partner']}\n💰 المبلغ: {message.text} USDT"
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

if __name__ == '__main__':
    bot.polling(none_stop=True)
