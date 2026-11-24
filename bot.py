import os
import sqlite3
from datetime import datetime, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from database import DB_NAME

ADMIN_EMAIL = "tatkalvsadmin@gmail.com"
ADMIN_WHATSAPP = "9933784612"
ADMIN_TELEGRAM = "https://t.me/STATKALF"


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("BUY KEY", callback_data="buy"),
            InlineKeyboardButton("MY HISTORY", callback_data="history")
        ],
        [
            InlineKeyboardButton("MY KEY", callback_data="mykey"),
            InlineKeyboardButton("MY PRICING", callback_data="pricing")
        ],
        [
            InlineKeyboardButton("UPGRADE PRICING", callback_data="upgrade"),
            InlineKeyboardButton("SOS", callback_data="sos")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Multi Website Key Store!",
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    if query.data == "history":
        db = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("""
            SELECT id, product_id, status
            FROM orders
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

        rows = cursor.fetchall()
        db.close()

        message = "MY HISTORY\n\n"
        if rows:
            for row in rows:
                message += (
                    f"Order: {row['id']}\n"
                    f"Product ID: {row['product_id']}\n"
                    f"Status: {row['status']}\n\n"
                )
        else:
            message += "No purchase history found."

        await query.edit_message_text(message, reply_markup=main_menu())

    elif query.data == "mykey":
        db = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("""
            SELECT licence_key, expiry_date, status
            FROM licences
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

        rows = cursor.fetchall()
        db.close()

        message = "MY KEY\n\n"
        active_found = False

        for row in rows:
            expiry = datetime.fromisoformat(row["expiry_date"])
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)

            if row["status"] == "active" and expiry > datetime.now(timezone.utc):
                active_found = True
                message += (
                    f"Key: {row['licence_key']}\n"
                    f"Expiry: {row['expiry_date']}\n\n"
                )

        if not active_found:
            message += "You do not have an active key."

        await query.edit_message_text(message, reply_markup=main_menu())

    elif query.data == "pricing":
        db = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("SELECT name, price, validity FROM products")
        rows = cursor.fetchall()
        db.close()

        message = "MY PRICING\n\n"
        for row in rows:
            message += (
                f"{row['name']}\n"
                f"Price: ₹{row['price']}\n"
                f"Validity: {row['validity']} days\n\n"
            )

        if not rows:
            message += "No products available yet."

        await query.edit_message_text(message, reply_markup=main_menu())

    elif query.data == "sos":
        message = (
            "SOS SUPPORT\n\n"
            f"Email: {ADMIN_EMAIL}\n"
            f"WhatsApp: {ADMIN_WHATSAPP}\n"
            f"Telegram: {ADMIN_TELEGRAM}"
        )
        await query.edit_message_text(message, reply_markup=main_menu())

    elif query.data == "buy":
        await query.edit_message_text(
            "BUY KEY\n\nPayment setup is being completed.",
            reply_markup=main_menu()
        )

    elif query.data == "upgrade":
        await query.edit_message_text(
            "UPGRADE PRICING\n\nUpgrade system is being completed.",
            reply_markup=main_menu()
        )


def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()


if __name__ == "__main__":
    run_bot()
