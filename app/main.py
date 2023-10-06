from decouple import config
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from .bot.bot import Bot
from .database.db_conn import create_db






def main() -> None:
    create_db()
    token = config('BOT_API')
    application = Application.builder().token(token).build()
    bot = Bot()
    application.add_handler(CommandHandler('start', bot.start))
    application.add_handler(CommandHandler('history', bot.history_review))
    application.add_handler(CommandHandler('help', bot.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.message))
    application.add_handler(CallbackQueryHandler(bot.callback_handler))
    application.run_polling()

if __name__ == '__main__':
    main()