import datetime

from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..database.db_crud import Db_Crud
from .deepl_api import translate


class Bot():
    def __init__(self) -> None:
        self.selected_language = None
        self.last_original_text = None

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Функция приветствия юзера после старта
        """
        await update.message.reply_html('hello please write what you need to translate', reply_markup=ForceReply(selective=True))

    async def choose_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton('Русский', callback_data='RU')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Выберите язык:', reply_markup=reply_markup)

    async def message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> ForceReply:
        """
        Обработчик запроса и сохранение запроса в бд
        """
        original_text = update.message.text
        self.last_original_text = original_text
        await self.choose_language(update, context)

    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Обработка кнопки и ответ переведенного текста пользователю
        """
        query = update.callback_query
        user_id = query.from_user.id
        callback_data = query.data
        self.selected_language = callback_data
        translated = await translate(self.last_original_text, self.selected_language)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Db_Crud().create_user_histroy(user_id, self.last_original_text, translated, timestamp)
        await query.answer(f'Перевод на {self.selected_language} в процессе!')
        await query.edit_message_text(f'Ваш перевод: \n{translated}')

    async def history_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        history = Db_Crud().get_translation_history(user_id)
        await update.message.reply_text(f'Ваша история переводов: \n{history}')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('/history - показывает историю ваших переводов')
