from datetime import datetime
import os
import random

# دالة تحية حسب الوقت
def get_greeting_by_time(lang="ar"):
    
    hour = datetime.now().hour

    if lang == "en":
        if 5 <= hour < 12:
            return "Good morning ☀️"
        elif 12 <= hour < 17:
            return "Good afternoon 🌤️"
        elif 17 <= hour < 21:
            return "Good evening 🌇"
        else:
            return "Good night 🌙"
    else:
        if 5 <= hour < 12:
            return "صباح الخير ☀️"
        elif 12 <= hour < 17:
            return "مساء الخير 🌤️"
        elif 17 <= hour < 21:
            return "مساء النور 🌇"
        else:
            return "مساء الخير 🌙"

# دالة قراءة الملف النصي كسطور
def read_file_lines(filename):
    path = os.path.join("bot-responses", filename)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
            return lines
    except FileNotFoundError:
        return ["⚠️ الملف غير موجود."]

# اختيار رد عشوائي من ملف
def get_random_reply(filename):
    lines = read_file_lines(filename)
    return random.choice(lines)
# دالة 
def get_reply_by_intent(intent: str, lang: str = "en") -> str:
    filename = f"{intent}_{lang}.txt"
    path = os.path.join("bot-responses", filename)

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if intent == "who":
            # ❗ ارجع كل الأسطر مجمعة كسطر واحد
            return "\n".join(lines)

        return random.choice(lines)

    except FileNotFoundError:
        return "⚠️ الرد غير متوفر حاليًا."


def detect_user_language(user_text: str, user_context_lang: str = None, user_interface_lang: str = "en") -> str: # type: ignore
    from bot.knowledge_handler import is_english

    if user_context_lang:
        return user_context_lang

    if is_english(user_text):
        return "en"

    if any("\u0600" <= c <= "\u06FF" for c in user_text):  # Arabic Unicode range
        return "ar"

    return "ar" if "ar" in user_interface_lang.lower() else "en"

def detect_intent(user_text: str) -> str:
    user_text = user_text.strip().lower()

    status = ["كيف الحال", "اخبارك", "شو اخبارك", "عامل ايه", "كيف عامل", "how are you", "how are things", "what's up"]
    example_keywords = ["مثال", "كود", "example", "code"]
    greetings = ["سلام", "السلام", "مرحبا", "أهلا", "hi", "hello", "hey"]
    thanks = ["شكرا", "شكراً", "شكرًا", "ثانكس", "thanks", "thank you"]
    who = ["من انت", "أنت من", "انت منو", "who are you", "what are you"]
    bye = ["مع السلامة", "وداعًا", "باي", "bye", "goodbye", "see you"]

    if any(word in user_text for word in greetings):
        return "greeting"
    elif any(word in user_text for word in thanks):
        return "thanks"
    elif any(word in user_text for word in who):
        return "who"
    elif any(word in user_text for word in example_keywords):
        return "example"
    elif any(word in user_text for word in bye):
        return "bye"
    elif any(word in user_text for word in status):
        return "status"
    elif len(user_text.split()) <= 3:
        return "knowledge"
    else:
        return "unknown"

def clean_user_input(text: str) -> str:
    text = text.lower().strip()

    # كلمات زائدة تُحذف من البداية
    prefixes = ["ما هو", "ال", "ماهي", "اشرح", "اشرح لي", "عرف", "ما هي", "ماهيه", "ماهيّة", "ماهو", "what is", "explain", "define", "tell me about"]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            break

    # إزالة علامات الترقيم في النهاية
    return text.rstrip("؟!.").strip()
