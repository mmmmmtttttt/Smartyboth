from telegram.ext import CommandHandler, MessageHandler, filters
from .responses import handle_message
from .commands import start, help, time_, date_, password_command, set_language, about, data_analysis
from .file_receiver import handle_document
from .files import handle_file
from telegram.ext import CallbackQueryHandler
from .callbacks import handle_callback
from bot.language_handler import handle_language_callback


def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("time", time_))
    app.add_handler(CommandHandler("date", date_))
    app.add_handler(CommandHandler("pass", password_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(CommandHandler("set_lang", set_language))
    app.add_handler(CallbackQueryHandler(handle_language_callback, pattern="^set_lang_"))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("data_analysis", data_analysis))
    app.add_handler(CallbackQueryHandler(handle_callback))


