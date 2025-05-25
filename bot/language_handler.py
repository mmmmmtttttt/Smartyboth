from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup

async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # type: ignore

    lang_code = query.data.replace("set_lang_", "")  # type: ignore
    context.user_data["lang"] = lang_code  # type: ignore

    if lang_code == "ar":
        await query.edit_message_text("✅ تم اختيار اللغة العربية.")  # type: ignore
        await update.effective_chat.send_message("سعدتُ بوصولك! ماذا تحب أن أقدّم لك؟ 📚") # type: ignore

        keyboard = [
            ["📊 تحليل البيانات", "🔐 كلمة مرور"],
            ["ℹ️ المساعدة", "ℹ️ عن البوت"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="اختر من الأوامر 👇"
        )

        await update.effective_chat.send_message("اختر من الأوامر التالية:", reply_markup=reply_markup)  # type: ignore

    else:
        await query.edit_message_text("✅ English language selected.")  # type: ignore
        await update.effective_chat.send_message("I'm glad you're here! What would you like me to help you with? 📚") # type: ignore

        keyboard = [
            ["📊 Data Analysis", "🔐 Password"],
            ["ℹ️ Help", "ℹ️ About Bot"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder="Choose from below 👇"
        )

        await query.message.reply_text("Please choose a command:", reply_markup=reply_markup)  # type: ignore
