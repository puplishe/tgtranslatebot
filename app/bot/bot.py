import os
import sqlite3
import datetime
from telegram.ext import ContextTypes
from telegram import ForceReply, Update
from .deepl_api import translate
from ..database.db_crud import Db_Crud
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Bot():
    def __init__(self) -> None:
        pass
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Функция приветствия юзера после старта
        """
        user = update.effective_user
        await update.message.reply_html('hello please write what you need to translate', reply_markup=ForceReply(selective=True))


    async def choose_language(self):
        keyboard = [
            [InlineKeyboardButton("Английский", callback_data="EN-US")],
            [InlineKeyboardButton("Немецкий", callback_data="GER")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выберите язык:", reply_markup=reply_markup)
        return reply_markup

    async def keyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("Перевести", callback_data="translate")],
            [InlineKeyboardButton("Выход", callback_data="exit")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выберите опцию:", reply_markup=reply_markup)
        if reply_markup == 'translate':
            lang = await self.choose_language(update, context)
            return lang
        else:
            return reply_markup


    async def message(self, update:Update) -> ForceReply:
        """
        Возвращает переведенный текст и заносит запрос в бд 
        """
        lang = await self.keyboard(update)
        if lang == 'exit':
            await update.message.reply_text(f'Вы выбрали выход')
        else:
            print(lang)
            translated = await translate(update.message.text, 'lang')
            user_id = update.effective_user.id
            original_text = update.message.text
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Db_Crud().create_user_histroy(user_id, original_text, translated, timestamp)
            await update.message.reply_text(f'here ur translated text: \n{translated}')