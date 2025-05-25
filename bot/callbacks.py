import json
import os
from telegram import Update
from telegram.ext import ContextTypes
from .utils import detect_user_language

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # type: ignore

    user_text = query.message.text # type: ignore
    user_lang_pref = context.user_data.get("lang") # type: ignore
    user_interface_lang = update.effective_user.language_code or "en" # type: ignore
    lang = detect_user_language(user_text, user_lang_pref, user_interface_lang) # type: ignore

    filename = "knowledge_en.json" if lang == "en" else "knowledge.json"
    desc_key = "description" if lang == "en" else "شرح"
    example_key = "example" if lang == "en" else "مثال"
    functions_key = "functions" if lang == "en" else "الدوال"
    path = os.path.join("knowledges", filename)

    if query.data.startswith("example::"): # type: ignore
        keyword = query.data.split("::")[1].strip().lower() # type: ignore

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        entry = data.get(keyword)
        if entry and isinstance(entry, dict):
            example = entry.get(example_key)
            if example:
                from .buttons import get_back_button
                title = "💡 <b>Example:</b>" if lang == "en" else "💡 <b>مثال:</b>"
                await query.message.reply_text( # type: ignore
                    f"{title}\n<pre><code>{example}</code></pre>",
                    parse_mode="HTML",
                    reply_markup=get_back_button(keyword, lang)
                )
            else:
                msg = "❌ No example available." if lang == "en" else "❌ لا يوجد مثال متاح."
                await query.message.reply_text(msg, parse_mode="HTML") # type: ignore

    elif query.data.startswith("back::"): # type: ignore
        parts = query.data.split("::") # type: ignore
        lang = parts[1].strip()
        keyword = parts[2].strip().lower()

        filename = "knowledge_en.json" if lang == "en" else "knowledge.json"
        desc_key = "description" if lang == "en" else "شرح"
        example_key = "example" if lang == "en" else "مثال"
        functions_key = "functions" if lang == "en" else "الدوال"
        path = os.path.join("knowledges", filename)

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        entry = data.get(keyword)
        if entry and isinstance(entry, dict):
            response = f"📘 <b>{keyword}</b>:\n{entry.get(desc_key)}\n\n"
            if functions_key in entry:
                response += ("\n\n🛠️ <b>Key Functions:</b>\n" if lang == "en" else "\n\n🛠️ أبرز الدوال:\n")
                response += "\n".join(f"• <code>{func}</code>" for func in entry[functions_key])

            from .buttons import get_example_button
            await query.message.reply_text( # type: ignore
                response.strip(),
                parse_mode="HTML",
                reply_markup=get_example_button(keyword)
            )
