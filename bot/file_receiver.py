# file_receiver.py
import os
from telegram import Update, File
from telegram.ext import ContextTypes

UPLOAD_DIR = "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.document is None:
        return

    document = update.message.document
    file_name = document.file_name

    if file_name is None:
        return

    if not file_name.endswith(".csv"):
        await update.message.reply_text("⚠️ الرجاء إرسال ملف بصيغة CSV فقط.")
        return

    file: File = await context.bot.get_file(document.file_id)
    file_path = os.path.join(UPLOAD_DIR, file_name)
    await file.download_to_drive(custom_path=file_path)

    await update.message.reply_text(f"✅ تم استلام الملف: {file_name}\nسيتم تحليله الآن...")

    # يمكنك استدعاء الدالة التحليلية هنا لاحقًا
    # analyze_file(file_path, update, context)
