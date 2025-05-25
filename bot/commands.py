from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
import string

# دالة بداية تشغيل البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is None:
        return

    await update.message.reply_text("سعدتُ بوصولك! ماذا تحب أن أقدّم لك؟ 📚")
    await update.message.reply_text("لعرض الاوامر المتاحة أكتب /help")

# دالة لمعرفة الاوامر المتاحة
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    lang = context.user_data.get("lang", "ar")  # type: ignore # اللغة المختارة

    if lang == "ar":
        msg = '''
<b>🛠️ الأوامر المتاحة:</b>

<code>/start</code> — بدء تشغيل البوت  
<code>/help</code> — عرض هذه المساعدة  
<code>/time</code> — عرض الوقت الحالي  
<code>/date</code> — عرض تاريخ اليوم  
<code>/about</code> — من أنا؟  
<code>/pass</code> — توليد كلمة مرور آمنة  
<code>/set_lang</code> — تغيير اللغة: العربية / English
<code>/data_analysis - تحليل البيانات

✨ <i>يمكنك أيضًا سؤالي عن تحليل البيانات باستخدام بايثون!</i>
'''
    else:
        msg = '''
<b>🛠️ Available Commands:</b>

<code>/start</code> — Start the bot  
<code>/help</code> — Show this help message  
<code>/time</code> — Show current time  
<code>/date</code> — Show today's date  
<code>/about</code> — Who am I?  
<code>/pass</code> — Generate a strong password  
<code>/set_lang</code> — Change language: English / العربية
<code>/data_analysis - Data Analysis

✨ <i>You can also ask me about data analysis using Python!</i>
'''
    await update.message.reply_text(msg, parse_mode="HTML")

# دالة لعرض الزمن الحالي
async def time_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    lang = context.user_data.get("lang", "ar") # type: ignore
    now = datetime.now().time().strftime("%H:%M:%S")
    text = f"الوقت الآن: {now}" if lang == "ar" else f"Current time: {now}"
    await update.message.reply_text(text)

# دالة لعرض تاريخ اليوم
async def date_(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    lang = context.user_data.get("lang", "ar") # type: ignore
    today = datetime.now().date().strftime("%d-%m-%Y")
    text = f"تاريخ اليوم: {today}" if lang == "ar" else f"Today's date: {today}"
    await update.message.reply_text(text)

# دالة لتوليد كلمة مرور
async def password_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    lang = context.user_data.get("lang", "ar") # type: ignore

    all_char = string.ascii_letters + string.digits
    serial_list = []
    count = random.randint(8, 16)
    while len(serial_list) < count:
        char = random.choice(all_char)
        if len(serial_list) == 0 and (char.islower() or char.isdigit()):
            continue
        serial_list.append(char)

    info = (
        "✅ تم توليد كلمة مرور آمنة:"
        if lang == "ar"
        else "✅ A strong password has been generated:"
    )
    await update.message.reply_text(info)
    await update.message.reply_text("".join(serial_list))

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    lang = context.user_data.get("lang", "ar") # type: ignore

    if lang == "ar":
        msg = (
            "🤖 <b>أنا SmartyBot</b>، مساعدك الذكي لتحليل البيانات باستخدام بايثون!\n"
            "💡 أستطيع شرح تحليل البيانات، تنفيذ تحليل بيانات، توليد تقارير، التحدث بلغتين.\n"
            "✨ صُنع بإتقان بواسطة <b>محمد طارق</b>."
        )
    else:
        msg = (
            "🤖 <b>I'm SmartyBot</b>, your smart assistant for data analysis using Python!\n"
            "💡 I can explain Data Analysis, run data analysis, generate reports, and speak both languages.\n"
            "✨ Created with care by <b>Mohammed Tarig</b>."
        )

    await update.message.reply_text(msg, parse_mode="HTML")

async def data_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    lang = context.user_data.get("lang", "ar") # type: ignore

    if lang == "ar":
        msg = (
            "🤖 <b>تحليل البيانات</b>، يتم تحليل البيانات باستخدام بايثون\n"
            "🧰 <b>الادوات المستخدم:</b>\n"
            "🐍 <code>Python => لغة البرمجة" \
            "🔢 <code>Numpy => مكتبة تساعد في ترتيب المصفوفات"
            "🧼 <code>Pandas => مكتبة تساعد في تنظيف و تحليل البيانات"
            "📊 <code>Matplotlib => مكتبة للرسم البياني"
            "📈 <code>Seaborn => مكتبة للرسم البياني الحديث"

            "📤 <b>يمكنك رفع الملف الان مباشرة لتحليله</b>"
            "ℹ️ <i>ملحوظة: يتم تحليل الملفات الاتية فقط:</i>"
            "📁 <code>CSV | EXCEL | JSON"
        )
    else:
        msg = (
            "🤖 <b>Data Analysis</b> is performed using Python\n"
            "🧰 <b>Tools used:</b>\n"
            "🐍 <code>Python</code> => Programming language\n"
            "🔢 <code>Numpy</code> => Library for working with arrays\n"
            "🧼 <code>Pandas</code> => Library for cleaning and analyzing data\n"
            "📊 <code>Matplotlib</code> => Library for data visualization\n"
            "📈 <code>Seaborn</code> => Modern statistical visualization library\n\n"

            "📤 <b>You can now upload your file for analysis</b>\n"
            "ℹ️ <i>Note: Only the following file types are supported:</i>\n"
            "📁 <code>CSV | EXCEL | JSON</code>"
        )

    await update.message.reply_text(msg, parse_mode="HTML")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    keyboard = [
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="set_lang_ar"),
            InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر اللغة / Choose language:", reply_markup=reply_markup)
