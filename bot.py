from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import random
import os
from openai import OpenAI


# =========================
# BOT TOKEN
# =========================

TOKEN = "8834192376:AAGreKnNbvvSDMVDlgx0sqDy_Rcr7yMcP3c"


# =========================
# OPENAI API KEY
# =========================

OPENAI_API_KEY = "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"

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# =========================
# PDF ФАЙЛ
# =========================

PDF_PATH = "/storage/emulated/0/Download/Хранитель персиков.pdf"


# =========================
# ҚОЛДАНУШЫЛАР
# =========================

users = {}


# =========================
# CHATGPT РЕЖИМІНДЕГІ
# ҚОЛДАНУШЫЛАР
# =========================

ai_users = set()


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
                "🤖 ChatGPT",
                callback_data="ai_chat"
            )
        ],
        [
            InlineKeyboardButton(
                "📎 Тіл",
                callback_data="language"
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
            "points": 0,
            "language": "kk"
        }

    # ChatGPT режимінен шығару
    ai_users.discard(user.id)

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
            "points": 0,
            "language": "kk"
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

        if not os.path.isfile(PDF_PATH):

            await query.message.reply_text(

                "❌ PDF файл табылмады!\n\n"

                "Файл мына папкада болуы керек:\n"

                f"{PDF_PATH}\n\n"

                "Файлдың атауы дәл:\n"
                "Хранитель персиков.pdf"
            )

            return


        await query.message.reply_text(

            "📖 Хранитель персиков\n\n"
            "⏳ Кітап дайындалып жатыр...\n"
            "Бір сәт күте тұр."
        )


        try:

            with open(PDF_PATH, "rb") as pdf:

                await query.message.reply_document(

                    document=pdf,

                    filename="Хранитель персиков.pdf",

                    caption=(
                        "📖 Хранитель персиков\n\n"
                        "📚 Толық PDF кітап"
                    )
                )

        except Exception as e:

            await query.message.reply_text(

                "❌ PDF жіберу кезінде қате болды.\n\n"
                f"{e}"
            )


    # =========================
    # CHATGPT
    # =========================

    elif query.data == "ai_chat":

        ai_users.add(user.id)

        keyboard = [

            [
                InlineKeyboardButton(
                    "🔙 Басты мәзір",
                    callback_data="home"
                )
            ]

        ]

        await query.edit_message_text(

            "🤖 CHATGPT\n\n"

            "Сәлем! Мен ChatGPT-пін. 😊\n\n"

            "Маған кез келген сұрағыңды жаза бер.\n\n"

            "Мысалы:\n"
            "• Python туралы сұра\n"
            "• Математика есептерін сұра\n"
            "• Мәтін жаздыр\n"
            "• Бір нәрсені түсіндір\n\n"

            "💬 Сұрағыңды жаза бер:",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # ТІЛ МӘЗІРІ
    # =========================

    elif query.data == "language":

        keyboard = [

            [
                InlineKeyboardButton(
                    "🇰🇿 Қазақша",
                    callback_data="lang_kk"
                )
            ],

            [
                InlineKeyboardButton(
                    "🇷🇺 Русский",
                    callback_data="lang_ru"
                )
            ],

            [
                InlineKeyboardButton(
                    "🇬🇧 English",
                    callback_data="lang_en"
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

            "📎 ТІЛ ТАҢДАУ\n\n"
            "Қай тілді таңдайсың?",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # ҚАЗАҚША
    # =========================

    elif query.data == "lang_kk":

        users[user.id]["language"] = "kk"

        await query.edit_message_text(

            "🇰🇿 Қазақ тілі таңдалды!\n\n"
            "Тілді сәтті өзгерттің.",

            reply_markup=main_menu()
        )


    # =========================
    # РУССКИЙ
    # =========================

    elif query.data == "lang_ru":

        users[user.id]["language"] = "ru"

        keyboard = [

            [
                InlineKeyboardButton(
                    "👤 Мой профиль",
                    callback_data="profile"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎮 Игры",
                    callback_data="games"
                )
            ],

            [
                InlineKeyboardButton(
                    "📚 Библиотека",
                    callback_data="library"
                )
            ],

            [
                InlineKeyboardButton(
                    "🤖 ChatGPT",
                    callback_data="ai_chat"
                )
            ],

            [
                InlineKeyboardButton(
                    "📎 Язык",
                    callback_data="language"
                )
            ],

            [
                InlineKeyboardButton(
                    "📞 Контакты",
                    callback_data="contact"
                )
            ]

        ]

        await query.edit_message_text(

            "🇷🇺 Русский язык выбран!\n\n"
            "Язык успешно изменён.",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # =========================
    # ENGLISH
    # =========================

    elif query.data == "lang_en":

        users[user.id]["language"] = "en"

        keyboard = [

            [
                InlineKeyboardButton(
                    "👤 My Profile",
                    callback_data="profile"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎮 Games",
                    callback_data="games"
                )
            ],

            [
                InlineKeyboardButton(
                    "📚 Library",
                    callback_data="library"
                )
            ],

            [
                InlineKeyboardButton(
                    "🤖 ChatGPT",
                    callback_data="ai_chat"
                )
            ],

            [
                InlineKeyboardButton(
                    "📎 Language",
                    callback_data="language"
                )
            ],

            [
                InlineKeyboardButton(
                    "📞 Contact",
                    callback_data="contact"
                )
            ]

        ]

        await query.edit_message_text(

            "🇬🇧 English selected!\n\n"
            "Language successfully changed.",

            reply_markup=InlineKeyboardMarkup(keyboard)
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

        # ChatGPT режимінен шығу
        ai_users.discard(user.id)

        await query.edit_message_text(

            "🏠 БАСТЫ МӘЗІР\n\n"
            "Қажетті бөлімді таңда:",

            reply_markup=main_menu()
        )


# ==================================================
# CHATGPT-ТЕН ЖАУАП АЛУ
# ==================================================

async def ai_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    # Егер ChatGPT режимі қосылмаған болса,
    # қарапайым хабарламаларды елемейміз.

    if user.id not in ai_users:

        return


    text = update.message.text.strip()

    if not text:

        return


    # =========================
    # ОЙЛАНЫП ЖАТЫР
    # =========================

    thinking = await update.message.reply_text(
        "🤖 Ойланып жатырмын..."
    )


    try:

        response = client.responses.create(

            model="gpt-5",

            input=[
                {
                    "role": "system",
                    "content": (
                        "Сен Vireon Telegram ботындағы "
                        "ChatGPT көмекшісісің. "
                        "Пайдаланушы қай тілде жазса, "
                        "сол тілде жауап бер. "
                        "Жауапты түсінікті және пайдалы бер."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]

        )


        answer = response.output_text


        # Telegram хабарлама лимитінен асып кетсе,
        # бірнеше бөлікке бөлеміз.

        max_length = 4000

        if len(answer) <= max_length:

            await thinking.edit_text(
                "🤖 " + answer
            )

        else:

            await thinking.delete()

            for i in range(0, len(answer), max_length):

                part = answer[i:i + max_length]

                await update.message.reply_text(
                    "🤖 " + part
                )


    except Exception as e:

        await thinking.edit_text(

            "❌ ChatGPT жауап бере алмады.\n\n"

            "Мыналарды тексер:\n"
            "1️⃣ OpenAI API key дұрыс па?\n"
            "2️⃣ Интернет бар ма?\n"
            "3️⃣ API аккаунтыңда модельді қолдану мүмкіндігі бар ма?\n\n"

            f"Техникалық қате:\n{e}"
        )


# ==================================================
# БОТТЫ ІСКЕ ҚОСУ
# ==================================================

app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)


app.add_handler(
    CallbackQueryHandler(button)
)


# Қарапайым мәтіндерді ChatGPT-ке жіберу
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        ai_message
    )
)


print(
    "Vireon + ChatGPT бот іске қосылды! 🚀"
)


app.run_polling()
