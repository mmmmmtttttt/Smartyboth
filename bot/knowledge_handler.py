import json
import os
import re
from .utils import clean_user_input

def is_english(text: str) -> bool:
    # كلمات إنجليزية شائعة، حتى لو كانت قصيرة
    known_english_words = {"hi", "hello", "thanks", "thank", "bye", "good", "who", "what", "how", "you"}

    words = text.lower().strip().split()
    english_count = sum(1 for w in words if w in known_english_words or all(ord(c) < 128 for c in w if c.isalpha()))
    arabic_count = sum(1 for w in words if any('\u0600' <= c <= '\u06FF' for c in w))  # نطاق الحروف العربية

    # رجّح الكفة حسب الأغلبية أو الكلمة الوحيدة المعروفة
    if english_count > arabic_count:
        return True
    return False


def get_structured_response(user_input: str, user_lang: str = None, context=None) -> str: # type: ignore
    user_input = user_input.strip()

    # 1. تحديد اللغة يدويًا أو تلقائيًا
    english = user_lang == "en" if user_lang else is_english(user_input)

    # 2. اختيار ملف المعرفة حسب اللغة
    filename = "knowledge_en.json" if english else "knowledge.json"
    path = os.path.join("knowledges", filename)

    # 3. اختيار المفاتيح المناسبة حسب اللغة
    desc_key = "description" if english else "شرح"
    example_key = "example" if english else "مثال"
    functions_key = "functions" if english else "الدوال"
    libraries_key = "libraries" if english else "المكتبات"

    # 4. تحميل البيانات
    with open(path, "r", encoding="utf-8") as f:
        knowledge = json.load(f)

    # 5. استخراج الكلمة المفتاحية من داخل الجملة (مفتاح مطابق جزئيًا)
    cleaned_input = clean_user_input(user_input)
    
    matched_key = next(
        (key for key in knowledge if key.strip().lower() == cleaned_input.strip()),
        None
    )

    if context:
        context.user_data["last_topic"] = matched_key

    if not matched_key:
        matched_key = next(
            (key for key in knowledge if key.lower() in cleaned_input.lower()),
            None
        )
    
    if matched_key:
        if context:
            context.user_data["last_topic"] = matched_key
            print("🧠 saved topic in context =", context.user_data.get("last_topic"))
        entry = knowledge[matched_key]
        response = ""

        if isinstance(entry, dict):
            if desc_key in entry:
                response += f"📘 <b>{matched_key}</b>:\n{entry[desc_key]}\n\n"

            if libraries_key in entry:
                response += ("🔧 <b>Core Libraries:</b>\n" if english else "🔧 المكتبات الأساسية:\n")
                response += "\n".join(f"• <code>{lib}</code>" for lib in entry[libraries_key])
                response += ("\n\n✏️ Type a library name to learn more." if english else "\n\n✏️ اكتب اسم أي مكتبة لمعرفة المزيد عنها.")

            if functions_key in entry:
                response += ("\n\n🛠️ <b>Key Functions:</b>\n" if english else "\n\n🛠️ أبرز الدوال:\n")
                response += "\n".join(f"• <code>{func}</code>" for func in entry[functions_key])
                response += ("\n\n✏️ Type a function name to learn what it does." if english else "\n\n✏️ اكتب اسم أي دالة لمعرفة وظيفتها.")

        elif isinstance(entry, str):
            response = entry
        else:
            response = "📚 No explanation available." if english else "📚 لا يوجد شرح متاح."
    
        return response.strip()
    else:
        return (
            "❌ Sorry, I couldn't find an explanation. Try typing just: pandas or describe."
            if english
            else "❌ لم أتعرف على هذا الموضوع. جرب كتابة: pandas أو describe فقط."
        )
    
