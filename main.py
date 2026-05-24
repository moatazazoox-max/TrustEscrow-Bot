import telebot
from telebot import types

# ضع التوكن الخاص بك هنا
API_TOKEN = '8806803636:AAGx0ck3UwL594FLx_G2BaFfwwXDux7d1v8'
bot = telebot.TeleBot(API_TOKEN)

# قاموس اللغات
LANGS = {
    'ar': {
        'welcome': "مرحباً بك في نظام TrustEscrow الآمن 🛡️.\nالرجاء اختيار لغتك:",
        'btn_ar': "🇸🇦 العربية",
        'btn_en': "🇬🇧 English"
    },
    'en': {
        'welcome': "Welcome to TrustEscrow Secure System 🛡️.\nPlease select your language:",
        'btn_ar': "🇸🇦 Arabic",
        'btn_en': "🇬🇧 English"
    }
}

# دالة البداية - اختيار اللغة
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_ar = types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    markup.add(btn_ar, btn_en)
    
    bot.send_message(message.chat.id, "مرحباً بك في TrustEscrow! \nWelcome to TrustEscrow!\n\nاختر لغتك | Select your language:", reply_markup=markup)

# التعامل مع اختيار اللغة
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_lang(call):
    lang = call.data.split('_')[1]
    # هنا يجب حفظ لغة المستخدم في قاعدة بيانات (مستقبلاً)
    
    text = "تم اختيار العربية" if lang == 'ar' else "Language set to English"
    bot.answer_callback_query(call.id, text)
    
    # القائمة الرئيسية بعد اختيار اللغة
    show_main_menu(call.message, lang)

def show_main_menu(message, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if lang == 'ar':
        btn1 = types.InlineKeyboardButton("🤝 فتح طلب وساطة جديد", callback_data="new_order")
        btn2 = types.InlineKeyboardButton("📄 شروط الخدمة", callback_data="terms")
    else:
        btn1 = types.InlineKeyboardButton("🤝 Open New Escrow", callback_data="new_order")
        btn2 = types.InlineKeyboardButton("📄 Terms of Service", callback_data="terms")
        
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "اختر ما تريد من القائمة:", reply_markup=markup)

# ... (باقي الكود الخاص بك الذي وضعته سابقاً) ...

def show_main_menu(message, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if lang == 'ar':
        btn1 = types.InlineKeyboardButton("🤝 فتح طلب وساطة جديد", callback_data="new_order")
        btn2 = types.InlineKeyboardButton("📄 شروط الخدمة", callback_data="terms")
    else:
        btn1 = types.InlineKeyboardButton("🤝 Open New Escrow", callback_data="new_order")
        btn2 = types.InlineKeyboardButton("📄 Terms of Service", callback_data="terms")
        
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "اختر ما تريد من القائمة:", reply_markup=markup)

# --- إضافة هذا الجزء في النهاية ---
import time
# دالة معالجة زر فتح طلب وساطة
@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def new_order_start(call):
    bot.send_message(call.message.chat.id, "الرجاء إدخال اسم الخدمة أو المنتج:")
    bot.register_next_step_handler(call.message, get_service_name)

def get_service_name(message):
    service_name = message.text
    bot.send_message(message.chat.id, f"تم تحديد الخدمة: {service_name}\nالآن، أدخل يوزر (Username) الطرف الآخر:")
    # هنا سنقوم بحفظ البيانات في قاعدة بيانات مؤقتة (سنطورها لاحقاً)
    bot.register_next_step_handler(message, get_partner_username, service_name)

def get_partner_username(message, service_name):
    partner = message.text
    bot.send_message(message.chat.id, f"الطرف الآخر: {partner}\nأخيراً، أدخل مبلغ الصفقة:")
    bot.register_next_step_handler(message, finish_order, service_name, partner)

def finish_order(message, service_name, partner):
    amount = message.text
    summary = f"✅ تم استلام تفاصيل طلبك:\n\nالخدمة: {service_name}\nالطرف الآخر: {partner}\nالمبلغ: {amount}\n\nجاري تجهيز عقد الوساطة..."
    bot.send_message(message.chat.id, summary)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5) # انتظر 5 ثواني إذا حدث خطأ ثم أعد المحاولة
