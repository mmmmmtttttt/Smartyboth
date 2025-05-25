import json
import os
from telegram import Update
from telegram.ext import CallbackContext

async def handle_example_request(context: CallbackContext, lang: str, update: Update):
    # 🧠 جلب آخر موضوع تم التحدث عنه
    last_topic = context.user_data.get("last_topic") # type: ignore

    if not last_topic:
        msg = "❌ لا يوجد موضوع حالي لعرض المثال. جرب كتابة اسم دالة أو مكتبة أولًا." if lang == "ar" else "❌ Please mention a topic first."
        await update.message.reply_text(msg) # type: ignore
        return

    # 📁 اختيار ملف المعرفة حسب اللغة
    filename = "knowledge_en.json" if lang == "en" else "knowledge.json"
    path = os.path.join("knowledges", filename)

    # 🔑 اختيار مفتاح المثال المناسب
    example_key = "example" if lang == "en" else "مثال"

    # 📖 تحميل الملف واسترجاع المثال
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    entry = data.get(last_topic)
    if entry and isinstance(entry, dict) and example_key in entry:
        example = entry[example_key]
        title = "💡 <b>Example:</b>" if lang == "en" else "💡 <b>مثال:</b>"
        await update.message.reply_text( # type: ignore
            f"{title}\n<pre><code>{example}</code></pre>",
            parse_mode="HTML"
        )
    else:
        msg = "❌ No example available for the last topic." if lang == "en" else "❌ لا يوجد مثال متاح لهذا الموضوع."
        await update.message.reply_text(msg) # type: ignore
