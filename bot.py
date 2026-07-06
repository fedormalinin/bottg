import os
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from storage import save
from utils import detect_platform
from queue_worker import task_queue, start_worker


TOKEN = "8829186403:AAFh1r9UvmWMW56H8F3mtWo_hK-nZRtFnOU"


# отправка результата из очереди
async def send_result(app, chat_id, file_path=None, error=None):

    if error:
        await app.bot.send_message(chat_id, f"Ошибка: {error}")
        return

    if not file_path:
        await app.bot.send_message(chat_id, "Не удалось обработать видео")
        return

    with open(file_path, "rb") as video:
        await app.bot.send_video(chat_id, video)

    os.remove(file_path)


# callback для worker
def make_send_callback(app):

    def callback(chat_id, file_path, error=None):
        import asyncio
        asyncio.create_task(send_result(app, chat_id, file_path, error))

    return callback


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Привет!\nПришли ссылку на видео 🎥"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text
    user = update.effective_user

    platform = detect_platform(url)

    save({
        "id": user.id,
        "username": user.username,
        "time": str(datetime.now()),
        "platform": platform,
        "url": url,
    })

    await update.message.reply_text(
        f"📥 Ссылка принята\nПлатформа: {platform}\n⏳ Начинаю загрузку..."
    )

    task_queue.put((update.effective_chat.id, url))


def main():

    app = Application.builder().token(TOKEN).build()

    start_worker(make_send_callback(app))

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()