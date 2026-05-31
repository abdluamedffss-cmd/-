import telebot
import os
import subprocess

# التوكن الخاص بك
TOKEN = "8752413289:AAH0Y3lEUN5VdBHTGPQZq1V_0jyvTw8UkSg"
bot = telebot.TeleBot(TOKEN)

# قاموس لتخزين حالة الفيديو لكل مستخدم
user_video = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🎬 أهلاً بك في بوت دراكون للتصميم\n\n"
        "📩 أرسل لي الفيديو، ثم اختر القالب:\n"
        "1 - TikTok Style 🔥\n"
        "2 - Cinematic 🎥\n"
        "3 - Shorts ⚡"
    )

@bot.message_handler(content_types=['video'])
def get_video(msg):
    try:
        bot.send
