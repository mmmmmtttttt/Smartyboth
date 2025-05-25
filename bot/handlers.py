from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot.responses import handle_message
from .commands import (
    start, help, time_, date_, password_command,
    set_language, about, data_analysis
)
from .file_receiver import handle_document
from .files import handle_file
from .callbacks import handle_callback
from bot.language_handler import handle_language_callback


def setup_handlers(app):
    # 🟢 أوامر التليجرام
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("time", time_))
    app.add_handler(CommandHandler("date", date_))
    app.add_handler(CommandHandler("pass", password_command))
    app.add_handler(CommandHandler("set_lang", set_language))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("data_analysis", data_analysis))

    # 🟢 رفع الملفات (مستندات)
    # app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file)) # type: ignore

    # 🟢 التعامل مع زر اختيار اللغة
    app.add_handler(CallbackQueryHandler(handle_language_callback, pattern="^set_lang_"))

    # 🟢 أوامر الأزرار (عربي + إنجليزي) باستخدام regex
    app.add_handler(MessageHandler(filters.Regex("(?i)^📊 ?(تحليل البيانات|data analysis)$"), data_analysis))
    app.add_handler(MessageHandler(filters.Regex("(?i)^🔐 ?(كلمة مرور|password)$"), password_command))
    app.add_handler(MessageHandler(filters.Regex("(?i)^ℹ️ ?(المساعدة|help)$"), help))
    app.add_handler(MessageHandler(filters.Regex("(?i)^ℹ️ ?(عن البوت|about bot)$"), about))

    # 🟢 أي رسالة أخرى لا تطابق أمر يتم تحليلها كنص عام
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 🟢 أي ردود Inline إضافية (لو عندك ردود مخصصة)
    app.add_handler(CallbackQueryHandler(handle_callback))
