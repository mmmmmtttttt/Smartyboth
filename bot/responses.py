from telegram import Update
from telegram.ext import ContextTypes
from .utils import (
    get_greeting_by_time,
    get_random_reply,
    detect_user_language,
    detect_intent,
    get_reply_by_intent
)
from .logger import log_unknown_command
from bot.knowledge_handler import get_structured_response
from .buttons import get_example_button
from .intents import handle_example_request

import json
import os

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None or update.effective_user is None:
        return

    user_text = update.message.text.lower()

    # 👇 تحديد اللغة
    lang = detect_user_language(
        user_text,
        context.user_data.get("lang"),  # type: ignore
        update.effective_user.language_code or "en"
    )

    # 👇 التحية والردود حسب اللغة
    greeting = get_greeting_by_time(lang)
    reply_file = "greetings_en.txt" if lang == "en" else "greetings_ar.txt"
    reply = get_random_reply(reply_file)

    intent = detect_intent(user_text)

    if intent == "greeting":
        await update.message.reply_text(f"{greeting}\n{reply}")
        return

    elif intent == "thanks":
        await update.message.reply_text(get_reply_by_intent("thanks", lang))
        return

    elif intent == "who":
        await update.message.reply_text(get_reply_by_intent("who", lang), parse_mode="HTML")
        return
    
    elif intent == "bye":
        await update.message.reply_text(get_reply_by_intent("bye", lang))
        return
    
    elif intent == "example":
        await handle_example_request(context, lang, update)
        return


    elif intent == "knowledge":
        # 📘 الرد من قاعدة المعرفة
        answer = get_structured_response(user_text, user_lang=lang, context=context)

        # 🧠 استخراج الكلمة المفتاحية من قاعدة المعرفة لعرض الزر التفاعلي
        file = "knowledge_en.json" if lang == "en" else "knowledge.json"
        path = os.path.join("knowledges", file)
        with open(path, "r", encoding="utf-8") as f:
            knowledge = json.load(f)

        matched_key = next((key for key in knowledge if key.lower() in user_text.lower()), None)

        if matched_key:
            reply_markup = get_example_button(matched_key)
            await update.message.reply_text(answer, parse_mode="HTML", reply_markup=reply_markup)
        else:
            await update.message.reply_text(answer, parse_mode="HTML")

        if "❌" in answer:
            await update.message.reply_text("I'm here to help, try /help 📋" if lang == "en" else "أنا هنا للمساعدة، جرب تكتب /help 📋")
            log_unknown_command(update.effective_user.id, update.effective_user.username, user_text)  # type: ignore
        return

    # ❓ حالة غير معروفة
    await update.message.reply_text("I'm here to help, try /help 📋" if lang == "en" else "أنا هنا للمساعدة، جرب تكتب /help 📋")
    log_unknown_command(update.effective_user.id, update.effective_user.username, user_text)  # type: ignore
