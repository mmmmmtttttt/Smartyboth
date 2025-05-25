from telegram.ext import ApplicationBuilder
from bot.config import TELEGRAM_TOKEN
from bot.handlers import setup_handlers

if TELEGRAM_TOKEN is None:
	raise ValueError("TELEGRAM_TOKEN must not be None")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
setup_handlers(app)
print("🤖 Bot Is Run")
app.run_polling()