from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_example_button(keyword: str):
    keyboard = [
        [InlineKeyboardButton("💡 Show Example", callback_data=f"example::{keyword}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_button(keyword: str, lang: str = "en"):
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Summary", callback_data=f"back::{lang}::{keyword}")]
    ]
    return InlineKeyboardMarkup(keyboard)
