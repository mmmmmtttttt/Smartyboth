import os
import tempfile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.analysis import clean_and_analyze_file
from bot.analysis_pdf import generate_analysis_pdf_reportlab_en
import pandas as pd

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    
    try:
        if update.message is None or update.message.document is None:
            await update.message.reply_text("⚠️ لم يتم إرسال ملف.")
            return

        file = update.message.document
        file_name = file.file_name or "uploaded_file.csv"
        file_path = os.path.join(tempfile.gettempdir(), file_name)

        await update.message.reply_text(f"📥 تم استلام الملف: {file_name}")
        file_obj = await file.get_file()
        await file_obj.download_to_drive(file_path)

        ALLOWED_EXTENSIONS = [".csv", ".xlsx", ".xls", ".json"]

        file_ext = os.path.splitext(file_name)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            msg = (
                "❌ لا يمكن تحليل هذا الملف. المدعومة هي: CSV, Excel, JSON"
                if lang == "ar"
                else "❌ Unsupported file type. Supported: CSV, Excel, JSON"
            )
            await update.message.reply_text(msg)
            return
        
        await update.message.reply_text("🔍 جاري تحليل الملف...")
        results = clean_and_analyze_file(file_path)
        if 'shape' not in results:
            await update.message.reply_text(f"❌ التحليل لم يكتمل. محتوى النتائج:\n{results}")
            return
        await update.message.reply_text("✅ تم الانتهاء من التحليل الأولي.")

        # ملخص التحليل
        await update.message.reply_text("📊 التحليل الإحصائي:\n" + results['stats_table'])
        await update.message.reply_text("🕳️ الخلايا الفارغة قبل التنظيف:\n" + results['nulls_before_table'])
        await update.message.reply_text("🧹 بعد التنظيف:\n" + results['nulls_after_table'])
        await update.message.reply_text("📄 أول 5 صفوف:\n" + results['first_rows'])
        await update.message.reply_text("📄 آخر 5 صفوف:\n" + results['last_rows'])
        # انشاء تقرير التحليل ملف PDF
        pdf_path = generate_analysis_pdf_reportlab_en(results)
        await update.message.reply_document(document=open(pdf_path, 'rb'), filename="analysis_report.pdf")
        # إرسال الملف المنظف
        with open(results['cleaned_file'], 'rb') as f:
            await update.message.reply_document(document=f, filename="cleaned_data.csv")

        # التحليل الإحصائي
        if isinstance(results['stats'], pd.DataFrame):
            await update.message.reply_text("📈 التحليل الإحصائي:\n" + results['stats'].head().to_string())

        # الرسم البياني
        if results.get('chart_path'):
            with open(results['chart_path'], 'rb') as chart:
                await update.message.reply_photo(chart)

        await update.message.reply_text("✅ التحليل اكتمل بنجاح. شكراً لاستخدامك البوت!")

        # رسالة الى المستخدم
        message_text = (
            "✅ <b>تم تحليل الملف بنجاح!</b>\n\n"
            "<b>📊 هل تبحث عن تحليل أكثر احترافية؟</b>\n"
            "تفاصيل أدق، معالجات متقدمة، واستخدام الذكاء الاصطناعي للتنبؤات الذكية.\n\n"
            "<b>📨 يمكنك التواصل مع <u>محمد طارق</u> عبر:</b>\n"
            "• 📧 <b>البريد:</b> <code>mohammedtarig820@gmail.com</code>\n"
            "• 📞 <b>رقم الهاتف:</b> <code>+966 558 971 433</code>\n"
            "• 💼 <b>Upwork:</b> من الزر أدناه 👇\n"
            "• 🔗 <b>LinkedIn:</b> من الزر أدناه 👇\n\n"
            "✨ <i>جاهز لتحويل بياناتك إلى قرارات ذكية.</i>"
        )

        # الأزرار
        keyboard = [
            [InlineKeyboardButton("📞 WhatsApp", url="https://wa.me/966558971433")],
            [InlineKeyboardButton("💼 Upwork", url="https://www.upwork.com/freelancers/~01249638f009ecc3c2")],
            [InlineKeyboardButton("🔗 LinkedIn", url="https://www.linkedin.com/in/mohammed-tarig-4a98a9209")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # إرسال الرسالة مع الزر
        await update.message.reply_text(message_text, parse_mode="HTML", reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء تحليل الملف:\n{str(e)}")
