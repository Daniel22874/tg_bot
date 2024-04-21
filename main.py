import re
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from datetime import datetime
from telegram import ReplyKeyboardRemove
import requests


reply_keyboard = [['help', 'Скачивание видео со сторонних ресурсов', 'Конвертор видео', 'Скачивание фото и документов со сторонних ресурсов', 'pass']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def open_keyboard(update, context):
    await update.message.reply_text(
        "Клавиатура Появилась",
        reply_markup=markup
    )


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Хорошо, убрали клавиатуру",
        reply_markup=ReplyKeyboardRemove()
    )


async def help_command(update, context):
    user_input = update.message.text
    if user_input == 'help':
        reply_keyboard = [['Сколько время', 'Цель проекта']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            "Выберите опцию:",
            reply_markup=markup
        )


async def handle_button_press(update, context):
    user_input = update.message.text
    if user_input == 'Сколько время':
        current_time = datetime.now().strftime('%H:%M:%S')
        await update.message.reply_text(current_time)
    elif user_input == 'Цель проекта':
        await update.message.reply_text('''Проект представляет из себя бота, который даёт пользователю возможности:
        1. Скачивание видео со сторонних ресурсов (YouTube, TikTok, Pinterest);
        2. Конвертация видео в любые форматы;
        3. Скачивание любых других данных со сторонних ресурсов (фото, документы и т.д.).
                                            ''')


async def save_from_www(update, link):
    user_input = update.message.text
    if user_input == 'Скачивание фото и документов со сторонних ресурсов':
        await update.message.reply_text('Введите ссылку на файл для скачивания: ')


async def save_from_www2(update, link):
    user_input = update.message.text
    filename = user_input.split('/')[-1]
    await update.message.reply_text(filename)
    r = requests.get(user_input, allow_redirects=True)
    open(filename, "wb").write(r.content)
    await update.message.reply_document(filename)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот. Вот мои функции", reply_markup=markup
    )


def main():
    application = Application.builder().token('6273204407:AAHc-578ru2Uie1JQnypi7YjdXL3fUU2-ew').build()

    async def start(update, context):
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я бот. Вот мои функции", reply_markup=markup
        )

    async def nach(update, context):
        await start(update, context)

    application.add_handler(MessageHandler(filters.Regex('^help$'), help_command))
    application.add_handler(MessageHandler(filters.Regex('^Сколько время$|^Цель проекта$'), handle_button_press))
    application.add_handler(CommandHandler('nachalo', nach))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("open", open_keyboard))
    application.add_handler(MessageHandler(filters.Regex('^Скачивание фото и документов со сторонних ресурсов$'), save_from_www))
    application.add_handler(MessageHandler(filters.TEXT, save_from_www2))
    application.run_polling()


if __name__ == '__main__':
    main()
