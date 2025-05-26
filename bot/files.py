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

    lang = context.user_data.get("lang", "ar")  # type: ignore

    try:
        if update.message.document is None:
            msg = "⚠️ لم يتم إرسال ملف." if lang == "ar" else "⚠️ No file was sent."
            await update.message.reply_text(msg)
            return

        file = update.message.document
        file_name = file.file_name or "uploaded_file.csv"
        file_path = os.path.join(tempfile.gettempdir(), file_name)

        msg = f"📥 تم استلام الملف: {file_name}" if lang == "ar" else f"📥 File received: {file_name}"
        await update.message.reply_text(msg)
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

        msg = "🔍 جاري قراءة الملف وتحليله..." if lang == "ar" else "🔍 Reading and analyzing the file..."
        await update.message.reply_text(msg)
        results = clean_and_analyze_file(file_path, lang=lang)

        if 'shape' not in results:
            msg = "❌ التحليل لم يكتمل. المحتوى:" if lang == "ar" else "❌ Analysis failed. Details:"
            await update.message.reply_text(f"{msg}\n{results}")
            return

        msg = "📄 ملخص الملف:" if lang == "ar" else "📄 File summary:"
        await update.message.reply_text(msg)
        await update.message.reply_text(results['summary_text'])

        msg = "🧹 جارٍ تنظيف البيانات..." if lang == "ar" else "🧹 Cleaning the data..."
        await update.message.reply_text(msg)

        msg = (
            "✅ تم حذف الأعمدة والصفوف الفارغة والمكررة."
            if lang == "ar" else
            "✅ Removed empty and duplicate rows/columns."
        )
        await update.message.reply_text(msg)

        msg = (
            "✅ تم تعويض القيم المفقودة في الأعمدة الرقمية بـ 0، والنصية بـ 'undefined'."
            if lang == "ar" else
            "✅ Filled missing values: numeric with 0, text with 'undefined'."
        )
        await update.message.reply_text(msg)

        msg = "📊 بدء التحليل الإحصائي والرسم البياني..." if lang == "ar" else "📊 Starting statistical analysis and visualization..."
        await update.message.reply_text(msg)

        if results.get('prediction_result'):
            pred = results['prediction_result']
            if lang == "ar":
                msg = f"🤖 تم تنفيذ التنبؤ على العمود: <b>{pred['target']}</b>"
                msg += f"\n📈 نسبة الدقة (R²): <b>{pred['r2_score']}</b>"
                msg += "\n🔍 أمثلة (فعلي → متوقع):\n"
            else:
                msg = f"🤖 Prediction executed on column: <b>{pred['target']}</b>"
                msg += f"\n📈 Accuracy (R²): <b>{pred['r2_score']}</b>"
                msg += "\n🔍 Samples (Actual → Predicted):\n"

            for actual, pred_val in pred['sample_prediction']:  # type: ignore
                msg += f"• {round(actual, 2)} → {round(pred_val, 2)}\n"
            await update.message.reply_text(msg, parse_mode="HTML")

            if results.get('prediction_chart_path'):
                with open(results['prediction_chart_path'], 'rb') as chart:
                    await update.message.reply_photo(chart)

        msg = "📄 جارٍ إرسال تقرير التحليل الكامل..." if lang == "ar" else "📄 Sending the full analysis report..."
        await update.message.reply_text(msg)

        pdf_path = generate_analysis_pdf_reportlab_en(results)
        await update.message.reply_document(document=open(pdf_path, 'rb'), filename="analysis_report.pdf")

        with open(results['cleaned_file'], 'rb') as f:
            await update.message.reply_document(document=f, filename="cleaned_data.csv")

        if isinstance(results['stats'], pd.DataFrame):
            stats_text = results['stats'].head().to_string()
            msg = "📈 بعض الإحصائيات الرقمية:" if lang == "ar" else "📈 Some numeric statistics:"
            await update.message.reply_text(msg)
            await update.message.reply_text(stats_text)

        if results.get('chart_path'):
            await update.message.reply_photo(photo=open(results['chart_path'], 'rb'))

        if results.get('corr_path'):
            await update.message.reply_photo(photo=open(results['corr_path'], 'rb'))

        msg = "✅ تم الانتهاء من التحليل. شكراً لاستخدامك البوت!" if lang == "ar" else "✅ Analysis complete. Thank you for using the bot!"
        await update.message.reply_text(msg)

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
        ) if lang == "ar" else (
            "✅ <b>File analyzed successfully!</b>\n\n"
            "<b>📊 Looking for more advanced analysis?</b>\n"
            "Deeper insights, smarter AI predictions, and expert-level reporting.\n\n"
            "<b>📨 Contact <u>Mohammed Tarig</u> via:</b>\n"
            "• 📧 <b>Email:</b> <code>mohammedtarig820@gmail.com</code>\n"
            "• 📞 <b>Phone:</b> <code>+966 558 971 433</code>\n"
            "• 💼 <b>Upwork:</b> from the button below 👇\n"
            "• 🔗 <b>LinkedIn:</b> from the button below 👇\n\n"
            "✨ <i>Ready to turn your data into decisions.</i>"
        )

        keyboard = [
            [InlineKeyboardButton("📞 WhatsApp", url="https://wa.me/966558971433")],
            [InlineKeyboardButton("💼 Upwork", url="https://www.upwork.com/freelancers/~01249638f009ecc3c2")],
            [InlineKeyboardButton("🔗 LinkedIn", url="https://www.linkedin.com/in/mohammed-tarig-4a98a9209")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message_text, parse_mode="HTML", reply_markup=reply_markup)

    except Exception as e:
        msg = "❌ حدث خطأ أثناء تحليل الملف:" if lang == "ar" else "❌ An error occurred while analyzing the file:"
        await update.message.reply_text(f"{msg}\n{str(e)}")
