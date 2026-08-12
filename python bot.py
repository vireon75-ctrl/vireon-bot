from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================================================
# 🔑 BOT TOKEN
# =========================================================
# BotFather берген токенді осы жерге қой:
TOKEN = "МҰНДА_BOTFATHER_ТОКЕНІН_ҚОЙ"

# =========================================================
# 🌐 USERS LANGUAGE
# =========================================================

user_languages = {}


# =========================================================
# 📝 TEXTS
# =========================================================

TEXTS = {

    "kk": {
        "welcome": (
            "👋 Сәлем!\n\n"
            "🌟 Vireon x Nexor ботына қош келдің!\n\n"
            "Төмендегі бөлімдердің бірін таңда:"
        ),
        "language": "🌐 Тіл",
        "admin": "👑 Админ",
        "back": "🔙 Артқа",

        "choose_language": (
            "🌐 Тілді таңдаңыз:\n\n"
            "Қажетті тілді төмендегі батырмадан таңдаңыз."
        ),

        "language_changed": "✅ Тіл қазақшаға ауыстырылды!"

        "admin_text": (
            "👑 <b>Админ</b>\n\n"
            "🌟 <b>Vireon x Nexor</b>\n\n"
            "📢 <b>Канал:</b> @sabinanizhaksykorem\n"
            "▶️ <b>YouTube:</b> @Vireon-127\n"
            "🎵 <b>TikTok:</b> Nexor🌟\n"
            "📩 <b>Байланыс:</b> @Sabinanizhansykorem\n\n"
            "✨ Барлық ресми парақшалар мен байланыс ақпараты осында."
        ),
    },

    "ru": {
        "welcome": (
            "👋 Привет!\n\n"
            "🌟 Добро пожаловать в бот Vireon x Nexor!\n\n"
            "Выбери нужный раздел:"
        ),
        "language": "🌐 Язык",
        "admin": "👑 Админ",
        "back": "🔙 Назад",

        "choose_language": (
            "🌐 Выберите язык:\n\n"
            "Выберите нужный язык с помощью кнопок ниже."
        ),

        "language_changed": "✅ Язык изменён на русский!",

        "admin_text": (
            "👑 <b>Админ</b>\n\n"
            "🌟 <b>Vireon x Nexor</b>\n\n"
            "📢 <b>Канал:</b> @sabinanizhaksykorem\n"
            "▶️ <b>YouTube:</b> @Vireon-127\n"
            "🎵 <b>TikTok:</b> Nexor🌟\n"
            "📩 <b>Контакт:</b> @Sabinanizhansykorem\n\n"
            "✨ Здесь находятся официальные страницы и контактная информация."
        ),
    },

    "en": {
        "welcome": (
            "👋 Hello!\n\n"
            "🌟 Welcome to the Vireon x Nexor bot!\n\n"
            "Choose a section below:"
        ),
        "language": "🌐 Language",
        "admin": "👑 Admin",
        "back": "🔙 Back",

        "choose_language": (
            "🌐 Choose your language:\n\n"
            "Select the language you want using the buttons below."
        ),

        "language_changed": "✅ Language changed to English!",

        "admin_text": (
            "👑 <b>Admin</b>\n\n"
            "🌟 <b>Vireon x Nexor</b>\n\n"
            "📢 <b>Channel:</b> @sabinanizhaksykorem\n"
            "▶️ <b>YouTube:</b> @Vireon-127\n"
            "🎵 <b>TikTok:</b> Nexor🌟\n"
            "📩 <b>Contact:</b> @Sabinanizhansykorem\n\n"
            "✨ Official pages and contact information."
        ),
    }
}


# =========================================================
# 🌐 LANGUAGE KEYBOARD
# =========================================================

def language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kk"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        ],
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ],
    ])


# =========================================================
# 🏠 MAIN MENU
# =========================================================

def main_keyboard(lang):
    t = TEXTS[lang]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["language"],
                callback_data="language"
            ),
            InlineKeyboardButton(
                t["admin"],
                callback_data="admin"
            )
        ]
    ])


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    # Егер бұрын тіл таңдамаған болса — қазақша
    if user_id not in user_languages:
        user_languages[user_id] = "kk"

    lang = user_languages[user_id]
    t = TEXTS[lang]

    await update.message.reply_text(
        t["welcome"],
        reply_markup=main_keyboard(lang),
        parse_mode="HTML"
    )


# =========================================================
# 🔘 BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_languages:
        user_languages[user_id] = "kk"

    lang = user_languages[user_id]
    t = TEXTS[lang]

    # =====================================================
    # 🌐 LANGUAGE
    # =====================================================

    if query.data == "language":

        await query.edit_message_text(
            t["choose_language"],
            reply_markup=language_keyboard(),
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 🇰🇿 KAZAKH
    # =====================================================

    if query.data == "lang_kk":

        user_languages[user_id] = "kk"

        await query.edit_message_text(
            TEXTS["kk"]["language_changed"],
            reply_markup=main_keyboard("kk"),
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 🇷🇺 RUSSIAN
    # =====================================================

    if query.data == "lang_ru":

        user_languages[user_id] = "ru"

        await query.edit_message_text(
            TEXTS["ru"]["language_changed"],
            reply_markup=main_keyboard("ru"),
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 🇬🇧 ENGLISH
    # =====================================================

    if query.data == "lang_en":

        user_languages[user_id] = "en"

        await query.edit_message_text(
            TEXTS["en"]["language_changed"],
            reply_markup=main_keyboard("en"),
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 👑 ADMIN
    # =====================================================

    if query.data == "admin":

        admin_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Channel",
                    url="https://t.me/sabinanizhaksykorem"
                )
            ],
            [
                InlineKeyboardButton(
                    "▶️ YouTube",
                    url="https://youtube.com/@Vireon-127"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎵 TikTok",
                    url="https://www.tiktok.com/@Nexor"
                )
            ],
            [
                InlineKeyboardButton(
                    "📩 Contact",
                    url="https://t.me/Sabinanizhansykorem"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="back"
                )
            ]
        ])

        await query.edit_message_text(
            t["admin_text"],
            reply_markup=admin_keyboard,
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 🔙 BACK
    # =====================================================

    if query.data == "back":

        await query.edit_message_text(
            t["welcome"],
            reply_markup=main_keyboard(lang),
            parse_mode="HTML"
        )

        return


# =========================================================
# 🚀 RUN BOT
# =========================================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Nexor2026_bot іске қосылды!")

    app.run_polling()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
