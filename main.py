import telebot
from telebot import types
import threading

# --- الإعدادات ---
API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8'
ADMIN_ID = '5335416450' # احصل عليه من بوت userinfobot
bot = telebot.TeleBot(API_TOKEN)
WALLET_ADDRESS = "D5nB2WhVgKDpS2N3Zx7uXFNV1zMqXiBh777XnQFx4kpu"

# --- نصوص البوت ---
TEXTS = {
    'ar': {
        'welcome': "🛡️ أهلاً بك في TrustEscrow.\nنظام وساطة آمن وموثوق للمعاملات الرقمية.",
        'main_menu': "كيف يمكنني مساعدتك اليوم؟",
        'start_btn': "🚀 بدء صفقة جديدة",
        'terms_btn': "📄 شروط الأمان",
        'service_prompt': "📦 ما هي الخدمة أو السلعة؟",
        'partner_prompt': "👤 أدخل يوزر الطرف الآخر:",
        'amount_prompt': "💰 أدخل المبلغ بالـ USDT:",
        'summary': "✅ *تم فتح الطلب بنجاح!*\n\nالخدمة: {s}\nالطرف الآخر: {p}\nالمبلغ: {a} USDT\n\n⚠️ *تنبيه:* محفظتنا تستقبل USDT على شبكة **Solana (SPL)** فقط!",
        'confirm_receipt': "✅ *تم التأكيد!* جاري فحص الخدمة.\nلديك 30 دقيقة للإبلاغ عن أي مشكلة. إذا كانت الخدمة سليمة، سيتم إنهاء الطلب تلقائياً.",
        'dispute_btn': "🚨 فتح نزاع (Dispute)",
        'dispute_alert': "🚨 *تنبيه نزاع!* المشتري يبلغ عن مشكلة في الطلب. يرجى التدخل فوراً!"
    },
    'en': {
        'welcome': "🛡️ Welcome to TrustEscrow.\nA secure gateway for your digital trades.",
        'main_menu': "How can I help you today?",
        'start_btn': "🚀 Start a new trade",
        'terms_btn': "📄 Safety Rules",
        'service_prompt': "📦 What are you trading?",
        'partner_prompt': "👤 Enter the other person's username:",
        'amount_prompt': "💰 How much money (USDT) is the trade?",
        'summary': "✅ *Order Created!*\n\nService: {s}\nTrading with: {p}\nAmount: {a} USDT\n\n⚠️ *WARNING:* Our wallet ONLY uses the **Solana (SPL)** network!",
        'confirm_receipt': "✅ *Confirmed!* Checking service.\nYou have 30 minutes to report any issue. If all is good, the order will finish automatically.",
        'dispute_btn': "🚨 Dispute",
        'dispute_alert': "🚨 *Dispute Alert!* The buyer has reported an issue. Please intervene immediately!"
    }
}

user_data = {}

# --- الدوال الأساسية ---
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
    show_main_menu(call.message, lang)

def show_main_menu(message, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(TEXTS[lang]['start_btn'], callback_data="new_order"),
               types.InlineKeyboardButton(TEXTS[lang]['terms_btn'], callback_data="terms"))
    bot.edit_message_text(TEXTS[lang]['main_menu'], message.chat.id, message.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def ask_service(call):
    lang = user_data[call.message.chat.id]['lang']
    bot.send_message(call.message.chat.id, TEXTS[lang]['service_prompt'])
    bot.register_next_step_handler(call.message, get_partner)

def get_partner(message):
    user_data[message.chat.id] = {**user_data.get(message.chat.id, {}), 'service': message.text}
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
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ تأكيد استلام الخدمة", callback_data="confirm_receipt"))
    bot.send_message(u_id, msg, parse_mode="Markdown", reply_markup=markup)

# --- نظام التأكيد والنزاع الذكي ---
@bot.callback_query_handler(func=lambda call: call.data == "confirm_receipt")
def user_confirmed(call):
    lang = user_data[call.message.chat.id]['lang']
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(TEXTS[lang]['dispute_btn'], callback_data="dispute_request"))
    
    bot.edit_message_text(TEXTS[lang]['confirm_receipt'], 
                          call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
    
    # تنبيه الأدمين بعد 30 دقيقة (1800 ثانية)
    threading.Timer(1800, lambda: notify_admin_to_release(call.message.chat.id, call.from_user.username)).start()

@bot.callback_query_handler(func=lambda call: call.data == "dispute_request")
def dispute_request(call):
    lang = user_data[call.message.chat.id]['lang']
    bot.send_message(ADMIN_ID, TEXTS[lang]['dispute_alert'] + f"\nالمشتري: @{call.from_user.username}")
    bot.answer_callback_query(call.id, "تم إبلاغ الأدمين بالنزاع.")

def notify_admin_to_release(chat_id, username):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ تحويل الأموال", callback_data="release_money"))
    bot.send_message(ADMIN_ID, f"🔔 *تنبيه:* انتهت الـ 30 دقيقة للطلب الخاص بـ @{username}. يرجى التحويل أو التأكد من عدم وجود نزاع.")

@bot.callback_query_handler(func=lambda call: call.data == "release_money")
def release_money(call):
    bot.send_message(call.message.chat.id, "✅ تم تأكيد التحويل. الصفقة انتهت بنجاح.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
