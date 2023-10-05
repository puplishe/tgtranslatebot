from decouple import config
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from .bot.bot import Bot
from .database.db_conn import create_db






def main() -> None:
    create_db()
    token = config('BOT_API')
    bot = Bot() 
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.message))
    application.add_handler(CallbackQueryHandler(bot.keyboard, pattern='^keyboard$'))  
    application.add_handler(CallbackQueryHandler(bot.choose_language, pattern='^choose_language$'))  
    application.run_polling()

if __name__ == '__main__':
    main()