# ✅ [2] files.py - النسخة التفاعلية مع المستخدم خطوة بخطوة

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

    lang = context.user_data.get("lang", "ar") # type: ignore

    try:
        if update.message.document is None:
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

        await update.message.reply_text("🔍 جاري قراءة الملف وتحليله...")
        results = clean_and_analyze_file(file_path)

        if 'shape' not in results:
            await update.message.reply_text(f"❌ التحليل لم يكتمل. المحتوى:\n{results}")
            return

        await update.message.reply_text("📄 ملخص الملف:")
        await update.message.reply_text(results['summary_text'])

        await update.message.reply_text("🧹 جارٍ تنظيف البيانات...")
        await update.message.reply_text("✅ تم حذف الأعمدة والصفوف الفارغة والمكررة.")
        await update.message.reply_text("✅ تم تعويض القيم المفقودة في الأعمدة الرقمية بـ 0، والنصية بـ 'undefined'.")

        await update.message.reply_text("📊 بدء التحليل الإحصائي والرسم البياني...")

        if results.get('prediction_result'):
            pred = results['prediction_result']
            msg = f"🤖 تم تنفيذ التنبؤ على العمود: <b>{pred['target']}</b>" # type: ignore
            msg += f"📈 نسبة الدقة (R²): <b>{pred['r2_score']}</b>" # type: ignore
            msg += "🔍 أمثلة (فعلي → متوقع):\n"
            for actual, pred_val in pred['sample_prediction']: # type: ignore
                msg += f"• {round(actual,2)} → {round(pred_val,2)}" # type: ignore
            await update.message.reply_text(msg, parse_mode="HTML")

            if results.get('prediction_chart_path'):
                with open(results['prediction_chart_path'], 'rb') as chart:
                    await update.message.reply_photo(chart)
                    
        await update.message.reply_text("📄 جارٍ إرسال تقرير التحليل الكامل...")

        pdf_path = generate_analysis_pdf_reportlab_en(results)
        await update.message.reply_document(document=open(pdf_path, 'rb'), filename="analysis_report.pdf")

        with open(results['cleaned_file'], 'rb') as f:
            await update.message.reply_document(document=f, filename="cleaned_data.csv")

        if isinstance(results['stats'], pd.DataFrame):
            stats_text = results['stats'].head().to_string()
            await update.message.reply_text("📈 بعض الإحصائيات الرقمية:")
            await update.message.reply_text(stats_text)

        if results.get('chart_path'):
            await update.message.reply_photo(photo=open(results['chart_path'], 'rb'))

        if results.get('corr_path'):
            await update.message.reply_photo(photo=open(results['corr_path'], 'rb'))

        await update.message.reply_text("✅ تم الانتهاء من التحليل. شكراً لاستخدامك البوت!")

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

        keyboard = [
            [InlineKeyboardButton("📞 WhatsApp", url="https://wa.me/966558971433")],
            [InlineKeyboardButton("💼 Upwork", url="https://www.upwork.com/freelancers/~01249638f009ecc3c2")],
            [InlineKeyboardButton("🔗 LinkedIn", url="https://www.linkedin.com/in/mohammed-tarig-4a98a9209")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message_text, parse_mode="HTML", reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء تحليل الملف:\n{str(e)}")
