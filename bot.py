import telebot
import os

# التوكن الخاص بك
TOKEN = "8752413289:AAH0Y3lEUN5VdBHTGPQZq1V_0jyvTw8UkSg"
bot = telebot.TeleBot(TOKEN)

user_video = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🎬 أهلاً بك في بوت التصميم يا دراكون\n\n"
        "📩 أرسل الفيديو أولاً، ثم اختر القالب:\n"
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
        bot.send_message(msg.chat.id, "✅ تم استلام الفيديو. اختر القالب الآن (1 أو 2 أو 3):")
    except Exception as e:
        bot.send_message(msg.chat.id, f"حدث خطأ أثناء تحميل الفيديو: {e}")

@bot.message_handler(func=lambda m: True)
def edit_video(msg):
    if msg.chat.id not in user_video:
        return

    choice = msg.text
    if choice not in ["1", "2", "3"]:
        bot.send_message(msg.chat.id, "❌ يرجى اختيار رقم صحيح (1 أو 2 أو 3)")
        return

    bot.send_message(msg.chat.id, "⏳ جاري التصميم... قد يستغرق الأمر ثواني")

    # اختيار الفلتر
    if choice == "1":
        cmd = 'ffmpeg -y -i input.mp4 -vf "drawtext=text=TikTok STYLE:fontsize=50:fontcolor=white:x=50:y=50,eq=contrast=1.3" -preset fast output.mp4'
    elif choice == "2":
        cmd = 'ffmpeg -y -i input.mp4 -vf "drawtext=text=CINEMATIC:fontsize=60:fontcolor=yellow:x=100:y=100,eq=contrast=1.4" -preset fast output.mp4'
    else:
        cmd = 'ffmpeg -y -i input.mp4 -vf "drawtext=text=SHORTS:fontsize=55:fontcolor=red:x=70:y=70,eq=contrast=1.2" -preset fast output.mp4'

    # تنفيذ الأمر
    os.system(cmd)

    # إرسال النتيجة
    try:
        if os.path.exists("output.mp4"):
            bot.send_video(msg.chat.id, open("output.mp4", "rb"), caption="✅ تم التصميم بنجاح!")
        else:
            bot.send_message(msg.chat.id, "⚠️ فشل تصميم الفيديو. تأكد من توفر FFmpeg على السيرفر.")
    except Exception as e:
        bot.send_message(msg.chat.id, f"خطأ في الإرسال: {e}")
    finally:
        # تنظيف الملفات
        if os.path.exists("input.mp4"): os.remove("input.mp4")
        if os.path.exists("output.mp4"): os.remove("output.mp4")
        if msg.chat.id in user_video: del user_video[msg.chat.id]

bot.polling()
