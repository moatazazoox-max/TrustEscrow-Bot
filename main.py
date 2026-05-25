import telebot
from telebot import types

API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8'
bot = telebot.TeleBot(API_TOKEN)

ADMIN_USERNAME = "@HE_5TE"
WALLET_ADDRESS = "D5nB2WhVgKDpS2N3Zx7uXFNV1zMqXiBh777XnQFx4kpu"

# القاموس الثنائي للغة
TEXTS = {
    'ar': {
        'welcome': "🛡️ *أهلاً بك في TrustEscrow*\n\nنظام وساطة رقمي آمن. نستخدم محفظة *Phantom* مشفرة للأمان العالي.",
        'main_menu': "اختر الإجراء المطلوب:",
        'start_btn': "🚀 البدء بصفقة جديدة",
        'terms_btn': "📄 شروط الأمان",
        'service_prompt': "📦 ما هي الخدمة أو السلعة؟",
        'partner_prompt': "👤 أدخل يوزر الطرف الآخر:",
        'amount_prompt': "💰 أدخل المبلغ (USDT):",
        'summary': "✅ *تم فتح الطلب بنجاح!*\n\nالخدمة: {s}\nالطرف الآخر: {p}\nالمبلغ: {a}\n\n⚠️ *تنبيه هام:* \nمحفظتنا هي *Phantom* وتستقبل USDT على شبكة **Solana (SPL)** فقط.\nإرسال عملات عبر شبكات أخرى (مثل TRC20) سيؤدي لضياع أموالك فوراً!",
    },
    'en': {
        'welcome': "🛡️ *Welcome to TrustEscrow*\n\nSecure digital escrow. We use *Phantom* wallet for high-security transactions.",
        'main_menu': "Please choose an action:",
        'start_btn': "🚀 Start New Escrow",
        'terms_btn': "📄 Safety Terms",
        'service_prompt': "📦 What is the service/item?",
        'partner_prompt': "👤 Enter partner's username:",
        'amount_prompt': "💰 Enter amount (USDT):",
        'summary': "✅ *Order Created Successfully!*\n\nService: {s}\nPartner: {p}\nAmount: {a}\n\n⚠️ *Critical Warning:* \nOur wallet is *Phantom* and accepts USDT on **Solana (SPL)** network ONLY.\nSending via other networks (like TRC20) will result in permanent loss!",
    }
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
               types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    bot.send_message(message.chat.id, "🛡️ Welcome to TrustEscrow", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_lang(call):
    lang = call.data.split('_')[1]
    user_data[call.message.chat.id] = {'lang': lang}
    show_main_menu(call.message, lang, edit=True, message_id=call.message.message_id)

def show_main_menu(message, lang, edit=False, message_id=None):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(TEXTS[lang]['start_btn'], callback_data="new_order"),
               types.InlineKeyboardButton(TEXTS[lang]['terms_btn'], callback_data="terms"))
    
    if edit:
        bot.edit_message_text(TEXTS[lang]['main_menu'], message.chat.id, message_id, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, TEXTS[lang]['main_menu'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "terms")
def show_terms(call):
    lang = user_data[call.message.chat.id]['lang']
    terms_text = {
        'ar': "📜 *شروط وأمان TrustEscrow*\n\n1. الأموال تُحفظ في محفظة Phantom مستقلة.\n2. يتم التحويل للبائع بعد تأكيدك.\n3. نستخدم شبكة *Solana* لضمان السرعة.",
        'en': "📜 *TrustEscrow Safety Terms*\n\n1. Funds held in an isolated Phantom wallet.\n2. Released after your confirmation.\n3. We use *Solana* network for speed."
    }
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📖 دليل المحفظة (Phantom/Solana)", callback_data="wallet_guide"))
    markup.add(types.InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data="back_to_menu"))
    bot.edit_message_text(terms_text[lang], call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    lang = user_data[call.message.chat.id]['lang']
    show_main_menu(call.message, lang, edit=True, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "wallet_guide")
def show_wallet_guide(call):
    lang = user_data[call.message.chat.id]['lang']
    guide_text = {
        'ar': ("📖 *دليل محفظة Phantom وشبكة Solana*\n\n"
               "1️⃣ محفظتنا هي *Phantom* وتستقبل USDT حصراً على شبكة *Solana (SPL)*.\n"
               "2️⃣ [شرح فتح محفظة Phantom](https://www.youtube.com/results?search_query=how+to+setup+phantom+wallet)\n\n"
               "⚠️ *تنبيه:* لا ترسل عبر TRC20 أو ERC20 أبداً. فقط شبكة Solana!"),
        'en': ("📖 *Phantom Wallet & Solana Network Guide*\n\n"
               "1️⃣ Our wallet is *Phantom* and accepts USDT on *Solana (SPL)* ONLY.\n"
               "2️⃣ [How to setup Phantom](https://www.youtube.com/results?search_query=how+to+setup+phantom+wallet)\n\n"
               "⚠️ *Warning:* Never send via TRC20 or ERC20. Solana network only!")
    }
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="terms"))
    bot.edit_message_text(guide_text[lang], call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def ask_service(call):
    lang = user_data[call.message.chat.id]['lang']
    bot.send_message(call.message.chat.id, TEXTS[lang]['service_prompt'])
    bot.register_next_step_handler(call.message, get_partner)

def get_partner(message):
    user_data[message.chat.id]['service'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['partner_prompt'])
    bot.register_next_step_handler(message, get_amount)

def get_amount(message):
    user_data[message.chat.id]['partner'] = message.text
    lang = user_data[message.chat.id]['lang']
    bot.send_message(message.chat.id, TEXTS[lang]['amount_prompt'])
    bot.register_next_step_handler(message, finish_order)

def finish_order(message):
    amount = message.text
    u_id = message.chat.id
    d = user_data[u_id]
    lang = d['lang']
    msg = TEXTS[lang]['summary'].format(s=d['service'], p=d['partner'], a=amount)
    msg += f"\n\n📍 *Phantom Address:* `{WALLET_ADDRESS}`\n📞 Support: {ADMIN_USERNAME}"
    bot.send_message(u_id, msg, parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"🔔 New Order from {message.from_user.username}\nService: {d['service']}\nAmount: {amount}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
