# language_handler.py

from telegram import Update
from telegram.ext import ContextTypes

async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # type: ignore

    if query.data == "set_lang_ar": # type: ignore
        context.user_data["lang"] = "ar" # type: ignore
        await query.edit_message_text("✅ تم تعيين اللغة إلى العربية.") # type: ignore
    elif query.data == "set_lang_en": # type: ignore
        context.user_data["lang"] = "en" # type: ignore
        await query.edit_message_text("✅ Language set to English.") # type: ignore