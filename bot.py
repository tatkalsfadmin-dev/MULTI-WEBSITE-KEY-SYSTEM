
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("BUY KEY 🛒", callback_data="buy"),
            InlineKeyboardButton("MY HISTORY 📜", callback_data="history")
        ],
        [
            InlineKeyboardButton("MY KEY 🔑", callback_data="mykey"),
            InlineKeyboardButton("MY PRICING 💎", callback_data="pricing")
        ],
        [
            InlineKeyboardButton("UPGRADE PRICING 🚀", callback_data="upgrade"),
            InlineKeyboardButton("SOS 🆘", callback_data="sos")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "WELCOME TO TATKAL KEY STORE\n\n"
        "Please select an option:",
        reply_markup=main_menu()
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        text = (
            "AVAILABLE PACKAGE\n\n"
            "30 DAYS KEY\n"
            "Price: ₹1200\n\n"
            "Select BUY NOW to continue."
        )
        keyboard = [[
            InlineKeyboardButton("BUY NOW", callback_data="buy_now")
        ]]

    elif query.data == "buy_now":
        text = (
            "PAYMENT CHECKOUT\n\n"
            "Payment will be available after the "
            "Razorpay integration is configured."
        )
        keyboard = []

    elif query.data == "history":
        text = "MY HISTORY\n\nNo purchase history found."

        keyboard = []

    elif query.data == "mykey":
        text = "MY KEY\n\nNo active licence found."
        keyboard = []

    elif query.data == "pricing":
        text = "MY PRICING\n\nNo active pricing record found."
        keyboard = []

    elif query.data == "upgrade":
        text = (
            "UPGRADE PRICING\n\n"
            "30 DAYS LICENCE → 60 DAYS LICENCE\n"
            "60 DAYS LICENCE → No upgrade available."
        )
        keyboard = []

    elif query.data == "sos":
        text = (
            "CUSTOMER SUPPORT\n\n"
            "Email: tatkalvsadmin@gmail.com\n"
            "WhatsApp: 9933784612\n"
            "Telegram: @STATKALF"
        )
        keyboard = []

    else:
        text = "Invalid option."
        keyboard = []

    if keyboard:
        keyboard.append([
            InlineKeyboardButton("BACK TO MENU", callback_data="menu")
        ])
    elif query.data != "menu":
        keyboard = [[
            InlineKeyboardButton("BACK TO MENU", callback_data="menu")
        ]]

    if query.data == "menu":
        await query.edit_message_text(
            "WELCOME TO TATKAL KEY STORE\n\nPlease select an option:",
            reply_markup=main_menu()
        )
    else:
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
  
