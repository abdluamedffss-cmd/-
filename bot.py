import telebot
import os

TOKEN = "8752413289:AAH0Y3lEUN5VdBHTGPQZq1V_0jyvTw8UkSg"
bot = telebot.TeleBot(TOKEN)

user_video = {}

# /start
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🎬 أهلاً بك في بوت التصميم\n\n"
        "📩 أرسل فيديو ثم اختر قالب:\n"
        "1 - TikTok Style 🔥\n"
        "2 - Cinematic 🎥\n"
        "3 - Shorts ⚡"
    )

# استقبال الفيديو
@bot.message_handler(content_types=['video'])
def get_video(msg):
    file_info = bot.get_file(msg.video.file_id)
    downloaded = bot.download_file(file_info.file_path)

    with open("input.mp4", "wb") as f:
        f.write(downloaded)

    user_video[msg.chat.id] = "ready"

    bot.send_message(msg.chat.id, "🎨 اختر القالب الآن:\n1 / 2 / 3")

# اختيار القالب
@bot.message_handler(func=lambda m: True)
def edit_video(msg):
    if msg.chat.id not in user_video:
        return

    choice = msg.text

    bot.send_message(msg.chat.id, "⏳ جاري تصميم الفيديو...")

    # 🎬 قالب 1 - TikTok
    if choice == "1":
        cmd = (
            'ffmpeg -y -i input.mp4 '
            '-vf "drawtext=text=TikTok STYLE🔥:fontsize=50:fontcolor=white:x=50:y=50,'
            'eq=contrast=1.3:brightness=0.05,zoompan=z=1.2" '
            '-preset fast output.mp4'
        )

    # 🎥 قالب 2 - Cinematic
    elif choice == "2":
        cmd = (
            'ffmpeg -y -i input.mp4 '
            '-vf "drawtext=text=CINEMATIC🎬:fontsize=60:fontcolor=yellow:x=100:y=100,'
            'eq=contrast=1.4:brightness=-0.05" '
            '-preset fast output.mp4'
        )

    # ⚡ قالب 3 - Shorts
    else:
        cmd = (
            'ffmpeg -y -i input.mp4 '
            '-vf "drawtext=text=SHORTS⚡:fontsize=55:fontcolor=red:x=70:y=70,'
            'eq=contrast=1.2:brightness=0.1" '
            '-preset fast output.mp4'
        )

    os.system(cmd)

    bot.send_video(msg.chat.id, open("output.mp4", "rb"), caption="✅ تم تصميم الفيديو")

    del user_video[msg.chat.id]


bot.polling()
