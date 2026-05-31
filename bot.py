import telebot
import os
import subprocess

# توكن البوت
TOKEN = "8752413289:AAH0Y3lEUN5VdBHTGPQZq1V_0jyvTw8UkSg"
bot = telebot.TeleBot(TOKEN)

user_video = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "🎬 أهلاً بك في بوت التصميم.\nأرسل الفيديو ثم اختر القالب (1 أو 2 أو 3)")

@bot.message_handler(content_types=['video'])
def get_video(msg):
    bot.send_message(msg.chat.id, "📥 جاري تحميل الفيديو...")
    file_info = bot.get_file(msg.video.file_id)
    downloaded = bot.download_file(file_info.file_path)
    with open("input.mp4", "wb") as f:
        f.write(downloaded)
    user_video[msg.chat.id] = "ready"
    bot.send_message(msg.chat.id, "✅ تم الاستلام. اختر القالب الآن:")

@bot.message_handler(func=lambda m: True)
def edit_video(msg):
    if msg.chat.id not in user_video: return
    choice = msg.text
    if choice not in ["1", "2", "3"]: return
    
    bot.send_message(msg.chat.id, "⏳ جاري التصميم...")
    
    filters = {
        "1": 'drawtext=text=TikTok:fontsize=50:fontcolor=white:x=50:y=50,eq=contrast=1.3',
        "2": 'drawtext=text=CINEMATIC:fontsize=60:fontcolor=yellow:x=100:y=100,eq=contrast=1.4',
        "3": 'drawtext=text=SHORTS:fontsize=55:fontcolor=red:x=70:y=70,eq=contrast=1.2'
    }

    cmd = f'ffmpeg -y -i input.mp4 -vf "{filters[choice]}" -preset fast output.mp4'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        with open("output.mp4", "rb") as video:
            bot.send_video(msg.chat.id, video, caption="✅ تم بنجاح!")
    except Exception as e:
        bot.send_message(msg.chat.id, f"خطأ: {e}")
    finally:
        for f in ["input.mp4", "output.mp4"]:
            if os.path.exists(f): os.remove(f)
        if msg.chat.id in user_video: del user_video[msg.chat.id]

bot.polling()
