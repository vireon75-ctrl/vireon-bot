from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN ="8834192376:AAG4UVZGw6fMR9x71__iGBz73wcfxm3b_yU" 

# Әр қолданушының мәліметтері
users = {}

def main_menu():
    keyboard = [
        [InlineKeyboardButton("👤 Менің профилім", callback_data="profile")],
        [InlineKeyboardButton("🎮 Ойындар", callback_data="games")],
        [InlineKeyboardButton("📞 Байланыс", callback_data="contact")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in users:
        users[user.id] = {
            "coins": 0,
            "points": 0
        }

    await update.message.reply_text(
        f"🤖 Vireon ботына қош келдің, {user.first_name}!\n\n"
        "Төмендегі мәзірден таңда:",
        reply_markup=main_menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    if user.id not in users:
        users[user.id] = {
            "coins": 0,
            "points": 0
        }

    if query.data == "profile":
        data = users[user.id]

        keyboard = [
            [InlineKeyboardButton("🔙 Басты мәзір", callback_data="home")]
        ]

        await query.edit_message_text(
            f"👤 СЕНІҢ ПРОФИЛІҢ\n\n"
            f"🏷 Атың: {user.first_name}\n"
            f"🆔 ID: {user.id}\n"
            f"⭐ Ұпай: {data['points']}\n"
            f"🪙 Монета: {data['coins']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "games":
        keyboard = [
            [InlineKeyboardButton("🪙 Монета лақтыру", callback_data="coin")],
            [InlineKeyboardButton("🎲 Кубик", callback_data="dice")],
            [InlineKeyboardButton("🔙 Басты мәзір", callback_data="home")]
        ]

        await query.edit_message_text(
            "🎮 ОЙЫНДАР МӘЗІРІ\n\n"
            "Ойын таңда:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "coin":
        result = random.choice(["🟡 Аверс", "⚪ Реверс"])

        if result == "🟡 Аверс":
            users[user.id]["coins"] += 1

        keyboard = [
            [InlineKeyboardButton("🪙 Қайта ойнау", callback_data="coin")],
            [InlineKeyboardButton("🔙 Ойындарға қайту", callback_data="games")]
        ]

        await query.edit_message_text(
            f"🪙 Монета лақтырылды!\n\n"
            f"Нәтиже: {result}\n"
            f"🪙 Монетаң: {users[user.id]['coins']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "dice":
        number = random.randint(1, 6)

        if number >= 4:
            users[user.id]["points"] += 1

        keyboard = [
            [InlineKeyboardButton("🎲 Қайта ойнау", callback_data="dice")],
            [InlineKeyboardButton("🔙 Ойындарға қайту", callback_data="games")]
        ]

        await query.edit_message_text(
            f"🎲 Кубик лақтырылды!\n\n"
            f"Нәтиже: {number}\n"
            f"⭐ Ұпайың: {users[user.id]['points']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "contact":
        keyboard = [
            [InlineKeyboardButton("🔙 Басты мәзір", callback_data="home")]
        ]

        await query.edit_message_text(
            "📞 БАЙЛАНЫС\n\n"
            "Сұрақтарың болса, админге жаза аласың.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "home":
        await query.edit_message_text(
            "🏠 БАСТЫ МӘЗІР\n\n"
            "Қажетті бөлімді таңда:",
            reply_markup=main_menu()
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Vireon бот іске қосылды! 🚀")
app.run_polling()
