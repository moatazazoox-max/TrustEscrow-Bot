import telebot
from telebot import types

# ضع التوكن الخاص بك هنا
API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8'
bot = telebot.TeleBot(API_TOKEN)

ADMIN_USERNAME = "@HE_5TE"
WALLET_ADDRESS = "D5nB2WhVgKDpS2N3Zx7uXFNV1zMqXiBh777XnQFx4kpu"

# القاموس النهائي: نصوص بسيطة ومباشرة للمبتدئين
TEXTS = {
    'ar': {
        'welcome': "🛡️ *أهلاً بك في TrustEscrow*\n\nنظام وساطة رقمي آمن. نستخدم محفظة *Phantom* مشفرة للأمان العالي.",
        'main_menu': "كيف يمكنني مساعدتك اليوم؟",
        'start_btn': "🚀 البدء بصفقة جديدة",
        'terms_btn': "📄 شروط الأمان",
        'service_prompt': "📦 ما هي الخدمة أو السلعة التي تتاجر بها؟",
        'partner_prompt': "👤 أدخل يوزر الطرف الآخر:",
        'amount_prompt': "💰 كم مبلغ الصفقة بالـ USDT؟",
        'summary': "✅ *تم فتح الطلب بنجاح!*\n\nالخدمة: {s}\nالطرف الآخر: {p}\nالمبلغ: {a} USDT\n\n⚠️ *تنبيه هام جداً:*\nمحفظتنا تستقبل USDT على شبكة **Solana (SPL)** فقط.\nإذا أرسلت على شبكة أخرى (مثل TRC20)، ستضيع أموالك نهائياً!",
    },
    'en': {
        'welcome': "🛡️ *Welcome to TrustEscrow*\n\nA safe and simple way to trade online. We help you trade safely without worrying about scams.",
        'main_menu': "How can I help you today?",
        'start_btn': "🚀 Start a new trade",
        'terms_btn': "📄 Safety Rules",
        'service_prompt': "📦 What are you trading?",
        'partner_prompt': "👤 Enter the other person's username:",
        'amount_prompt': "💰 How much money (USDT) is the trade?",
        'summary': "✅ *Order Created!*\n\nService: {s}\nTrading with: {p}\nAmount: {a} USDT\n\n⚠️ *IMPORTANT WARNING:*\nOur wallet ONLY uses the **Solana (SPL)** network.\nIf you send money using any other network (like TRC20 or ERC20), the money will be lost forever!",
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
        'ar': "📜 *شروط وأمان TrustEscrow*\n\n1. الأموال تُحفظ في محفظة Phantom مستقلة.\n2. يتم التحويل للبائع بعد تأكيدك.\n3. نستخدم شبكة *Solana* لسرعتها وتكلفتها المنخفضة.",
        'en': "📜 *TrustEscrow Safety Rules*\n\n1. Money is held in a secure Phantom wallet.\n2. Money is sent to the seller after you confirm.\n3. We use the *Solana* network because it is fast and cheap."
    }
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📖 دليل المحفظة", callback_data="wallet_guide"))
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
        'ar': ("📖 *دليل فتح محفظة رقمية*\n\n"
               "لإتمام الصفقة، تحتاج لمحفظة تدعم شبكة *Solana*.\n\n"
               "1️⃣ *بينانس (للمبتدئين):*\n[شرح بينانس](https://www.youtube.com/results?search_query=شرح+فتح+حساب+بينانس)\n"
               "2️⃣ *تراست واليت (تحكم كامل):*\n[شرح تراست واليت](https://www.youtube.com/results?search_query=شرح+إنشاء+محفظة+تراست+واليت)\n\n"
               "⚠️ *تنبيه:* لا ترسل عبر TRC20 أو ERC20. فقط شبكة **Solana (SPL)**!"),
        'en': ("📖 *Digital Wallet Setup Guide*\n\n"
               "To trade, you need a wallet that supports the *Solana* network.\n\n"
               "1️⃣ *Binance (Easy):*\n[Watch Binance Tutorial](https://www.youtube.com/results?search_query=how+to+create+a+binance+account)\n"
               "2️⃣ *Trust Wallet (Full Control):*\n[Watch Trust Wallet Tutorial](https://www.youtube.com/results?search_query=how+to+create+a+trust+wallet)\n\n"
               "⚠️ *WARNING:* Do not send via TRC20 or ERC20. Only use the **Solana (SPL)** network!")
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
