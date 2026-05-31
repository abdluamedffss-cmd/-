import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import TOKEN
from video_editor import process_video

os.makedirs("downloads", exist_ok=True)
os.makedirs("output", exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أرسل فيديو ليتم تعديله."
    )

async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    file = await context.bot.get_file(video.file_id)

    input_path = f"downloads/{video.file_id}.mp4"
    output_path = f"output/{video.file_id}.mp4"

    await file.download_to_drive(input_path)

    process_video(input_path, output_path)

    await update.message.reply_video(
        video=open(output_path, "rb"),
        caption="تمت معالجة الفيديو."
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.VIDEO, receive_video)
    )

    print("Bot Started")

    app.run_polling()

if __name__ == "__main__":
    main()
