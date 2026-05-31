import telebot
import os
import subprocess

# التوكن الخاص بك
TOKEN = "8752413289:AAH0Y3lEUN5VdBHTGPQZq1V_0jyvTw8UkSg"
bot = telebot.TeleBot(TOKEN)

user_video = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🎬 أهلاً بك في بوت دراكون للتصميم\n\n"
        "📩 أرسل لي الفيديو، ثم اختر الرقم:\n"
        "1 - TikTok Style 🔥\n"
        "2 - Cinematic 🎥\n"
        "3 - Shorts ⚡"
    )

@bot.message_handler(content_types=['video'])
def get_video(msg):
    try:
        bot.send_message(msg.chat.id, "📥 جاري تحميل الفيديو...")
        file_info = bot.get_file(msg.video.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open("input.mp4", "wb") as f:
            f.write(downloaded)
        user_video[msg.chat.id] = "ready"
        bot.send_message(msg.chat.id, "✅ تم الاستلام. اختر القالب (1 أو 2 أو 3):")
    except Exception as e:
        bot.send_message(msg.chat.id, f"حدث خطأ: {e}")

@bot.message_handler(func=lambda m: True)
def edit_video(msg):
    if msg.chat.id not in user_video: return
    
    choice = msg.text
    if choice not in ["1", "2", "3"]:
        bot.send_message(msg.chat.id, "❌ اختر رقماً صحيحاً (1، 2، أو 3)")
        return

    bot.send_message(msg.chat.id, "⏳ جاري المعالجة...")

    # القوالب
    filters = {
        "1": 'drawtext=text=TikTok:fontsize=50:fontcolor=white:x=50:y=50,eq=contrast=1.3',
        "2": 'drawtext=text=CINEMATIC:fontsize=60:fontcolor=yellow
