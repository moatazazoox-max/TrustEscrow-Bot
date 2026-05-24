import telebot
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "مرحباً بك في نظام TrustEscrow AI! أنا جاهز لإدارة العمليات.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=run).start()
    bot.infinity_polling()

