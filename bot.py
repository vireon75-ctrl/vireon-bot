from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import random
import os


# =========================
# BOT TOKEN
# =========================

TOKEN = "ЖАҢА_TOKEN_ОСЫ_ЖЕРГЕ"


# =========================
# PDF ФАЙЛ
# =========================

PDF_PATH = "/storage/emulated/0/Download/Хранитель персиков.pdf"


# =========================
# ҚОЛДАНУШЫЛАР
# =========================

users = {}


# =========================
# БАСТЫ МӘЗІР
# =========================

def main_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "👤 Менің профилім",
                callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                "🎮 Ойындар",
                callback_data="games"
            )
        ],
        [
            InlineKeyboardButton(
                "📚 Кітапхана",
                callback_data="library"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Байланыс",
                callback_data="contact"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# /START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if user.id not in users:

        users[user.id] = {
            "coins": 0,
            "points": 0
        }

    await update.message.reply_text(

        f"🤖 Vireon ботына қош келдің, "
        f"{user.first_name}!\n\n"

        "Төмендегі мәзірден таңда:",

        reply_markup=main_menu()
    )


# =========================
# БАТЫРМАЛАР
# =========================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user = query.from_user


    if user.id not in users:

        users[user.id] = {
            "coins": 0,
            "points": 0
        }


    # =========================
    # ПРОФИЛЬ
    # =========================

    if query.data == "profile":

        data = users[user.id]

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 Басты мәзір",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(

            f"👤 СЕНІҢ ПРОФИЛІҢ\n\n"

            f"🏷 Атың: {user.first_name}\n"
            f"🆔 ID: {user.id}\n"
            f"⭐ Ұпай: {data['points']}\n"
            f"🪙 Монета: {data['coins']}",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # ОЙЫНДАР
    # =========================

    elif query.data == "games":

        keyboard = [

            [
                InlineKeyboardButton(
                    "🪙 Монета лақтыру",
                    callback_data="coin"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎲 Кубик",
                    callback_data="dice"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 Басты мәзір",
                    callback_data="home"
                )
            ]

        ]

        await query.edit_message_text(

            "🎮 ОЙЫНДАР МӘЗІРІ\n\n"
            "Ойын таңда:",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # МОНЕТА
    # =========================

    elif query.data == "coin":

        result = random.choice(
            ["🟡 Аверс", "⚪ Реверс"]
        )


        if result == "🟡 Аверс":

            users[user.id]["coins"] += 1


        keyboard = [

            [
                InlineKeyboardButton(
                    "🪙 Қайта ойнау",
                    callback_data="coin"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 Ойындарға қайту",
                    callback_data="games"
                )
            ]

        ]


        await query.edit_message_text(

            f"🪙 Монета лақтырылды!\n\n"

            f"Нәтиже: {result}\n"

            f"🪙 Монетаң: "
            f"{users[user.id]['coins']}",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # КУБИК
    # =========================

    elif query.data == "dice":

        number = random.randint(1, 6)


        if number >= 4:

            users[user.id]["points"] += 1


        keyboard = [

            [
                InlineKeyboardButton(
                    "🎲 Қайта ойнау",
                    callback_data="dice"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 Ойындарға қайту",
                    callback_data="games"
                )
            ]

        ]


        await query.edit_message_text(

            f"🎲 Кубик лақтырылды!\n\n"

            f"Нәтиже: {number}\n"

            f"⭐ Ұпайың: "
            f"{users[user.id]['points']}",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # КІТАПХАНА
    # =========================

    elif query.data == "library":

        keyboard = [

            [
                InlineKeyboardButton(
                    "📖 Хранитель персиков",
                    callback_data="book_peach"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 Басты мәзір",
                    callback_data="home"
                )
            ]

        ]


        await query.edit_message_text(

            "📚 КІТАПХАНА\n\n"
            "Кітапты таңда:",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # ХРАНИТЕЛЬ ПЕРСИКОВ
    # =========================

    elif query.data == "book_peach":

        if not os.path.exists(PDF_PATH):

            await query.message.reply_text(

                "❌ PDF файл табылмады!\n\n"

                "Файл мына жерде болуы керек:\n"

                f"{PDF_PATH}"
            )

            return


        await query.message.reply_text(

            "📖 Хранитель персиков\n\n"
            "Кітабың дайын! 😊"
        )


        with open(PDF_PATH, "rb") as pdf:

            await query.message.reply_document(

                document=pdf,

                caption="📖 Хранитель персиков"
            )


    # =========================
    # БАЙЛАНЫС
    # =========================

    elif query.data == "contact":

        keyboard = [

            [
                InlineKeyboardButton(
                    "🔙 Басты мәзір",
                    callback_data="home"
                )
            ]

        ]


        await query.edit_message_text(

            "📞 БАЙЛАНЫС\n\n"

            "Сұрақтарың болса, "
            "админге жаза аласың.",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # БАСТЫ МӘЗІР
    # =========================

    elif query.data == "home":

        await query.edit_message_text(

            "🏠 БАСТЫ МӘЗІР\n\n"
            "Қажетті бөлімді таңда:",

            reply_markup=main_menu()
        )


# =========================
# БОТТЫ ІСКЕ ҚОСУ
# =========================

app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CallbackQueryHandler(button)
)


print("Vireon бот іске қосылды! 🚀")


app.run_polling()                
