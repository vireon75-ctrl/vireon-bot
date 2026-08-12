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
import json


# ==================================================
# BOT TOKEN
# ==================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN табылмады!")


# ==================================================
# USER DATA FILE
# ==================================================

DATA_FILE = "users.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


users = load_users()


def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            users,
            file,
            ensure_ascii=False,
            indent=4
        )


# ==================================================
# USER DATABASE
# ==================================================

def create_user(user_id):

    user_id = str(user_id)

    if user_id not in users:

        users[user_id] = {
            "profile_name": "",
            "coins": 0,
            "points": 0,
            "language": "kk"
        }

        save_users()


def get_user(user_id):

    user_id = str(user_id)

    create_user(user_id)

    return users[user_id]


def update_user(user_id, field, value):

    user_id = str(user_id)

    create_user(user_id)

    allowed_fields = [
        "profile_name",
        "coins",
        "points",
        "language"
    ]

    if field not in allowed_fields:
        return

    users[user_id][field] = value

    save_users()


def add_coins(user_id, amount):

    user_id = str(user_id)

    create_user(user_id)

    users[user_id]["coins"] += amount

    save_users()


def add_points(user_id, amount):

    user_id = str(user_id)

    create_user(user_id)

    users[user_id]["points"] += amount

    save_users()


# ==================================================
# ADMIN
# ==================================================

ADMIN_USERNAME = "Sabinanizhansykorem"


# ==================================================
# YOUTUBE / TIKTOK
# ==================================================

YOUTUBE_URL = "https://youtube.com/"
TIKTOK_URL = "https://tiktok.com/"


# ==================================================
# LANGUAGE TEXTS
# ==================================================

TEXTS = {

    "kk": {

        "welcome":
            "🤖 Vireon ботына қош келдің!\n\n"
            "Қажетті бөлімді таңда:",

        "profile_button": "👤 Сенің профилің",
        "games_button": "🎮 Ойындар",
        "language_button": "🌐 Тіл",
        "admin_button": "👑 Админ",

        "home":
            "🏠 БАСТЫ МӘЗІР\n\n"
            "Қажетті бөлімді таңда:",

        "profile":
            "👤 СЕНІҢ ПРОФИЛІҢ\n\n",

        "profile_name": "👤 Атың",
        "profile_name_none": "Қойылмаған",
        "profile_id": "🆔 ID",
        "points": "⭐ Ұпай",
        "coins": "🪙 Монета",

        "change_name": "✏️ Атымды өзгерту",
        "back": "🔙 Басты мәзір",

        "games":
            "🎮 ОЙЫНДАР МӘЗІРІ\n\n"
            "Ойын таңда:",

        "coin": "🪙 Монета лақтыру",
        "dice": "🎲 Кубик",
        "math": "🧮 Математика",
        "guess": "🎯 Болжам",

        "back_games": "🔙 Ойындарға қайту",

        "coin_result":
            "🪙 Монета лақтырылды!\n\n",

        "heads": "🟡 Аверс",
        "tails": "⚪ Реверс",
        "coin_count": "🪙 Монетаң",

        "again": "🔄 Қайта ойнау",

        "dice_result":
            "🎲 Кубик лақтырылды!\n\n",

        "dice_number": "Нәтиже",
        "points_count": "⭐ Ұпайың",

        "math_instruction":
            "🧮 МАТЕМАТИКА\n\n"
            "Есепті шығар:\n\n",

        "math_answer":
            "✍️ Жауабыңды кәдімгі клавиатурамен жаз.",

        "math_correct":
            "✅ Дұрыс!\n\n"
            "⭐ +1 ұпай",

        "math_wrong":
            "❌ Қате!\n\n"
            "Дұрыс жауап",

        "next_math": "🧮 Келесі есеп",

        "guess_instruction":
            "🎯 БОЛЖАМ ОЙЫНЫ\n\n"
            "Мен 1 мен 10 аралығында бір сан ойладым.\n"
            "Санды жазыңыз:",

        "guess_higher":
            "⬆️ Үлкенірек сан таңда!",

        "guess_lower":
            "⬇️ Кішірек сан таңда!",

        "guess_correct":
            "🎉 Дұрыс таптың!\n\n"
            "⭐ +1 ұпай\n"
            "🪙 +2 монета",

        "language_title":
            "🌐 ТІЛ ТАҢДАУ\n\n"
            "Қай тілді таңдайсың?",

        "kk_selected":
            "🇰🇿 Қазақ тілі таңдалды!",

        "ru_selected":
            "🇷🇺 Русский язык выбран!",

        "en_selected":
            "🇬🇧 English selected!",

        "admin":
            "👑 АДМИН\n\n"
            "🤖 Vireon жобасының әкімшісі\n\n"
            "Төмендегі батырмалар арқылы байланыса аласың.",

        "write_admin": "📩 Админге жазу",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok",

        "enter_name":
            "✏️ Жаңа атыңды жаз:\n\n"
            "Бұл Vireon ішіндегі профиліңнің аты болады.",

        "name_saved":
            "✅ Атың сәтті өзгертілді!",

        "invalid_number":
            "❌ Өтінемін, тек сан жаз.",

        "guess_wait":
            "🎯 Алдымен 1 мен 10 аралығындағы сан жаз."
    },


    "ru": {

        "welcome":
            "🤖 Добро пожаловать в Vireon!\n\n"
            "Выбери нужный раздел:",

        "profile_button": "👤 Твой профиль",
        "games_button": "🎮 Игры",
        "language_button": "🌐 Язык",
        "admin_button": "👑 Админ",

        "home":
            "🏠 ГЛАВНОЕ МЕНЮ\n\n"
            "Выбери нужный раздел:",

        "profile":
            "👤 ТВОЙ ПРОФИЛЬ\n\n",

        "profile_name": "👤 Имя",
        "profile_name_none": "Не установлено",
        "profile_id": "🆔 ID",
        "points": "⭐ Очки",
        "coins": "🪙 Монеты",

        "change_name": "✏️ Изменить имя",
        "back": "🔙 Главное меню",

        "games":
            "🎮 МЕНЮ ИГР\n\n"
            "Выбери игру:",

        "coin": "🪙 Подбросить монету",
        "dice": "🎲 Кубик",
        "math": "🧮 Математика",
        "guess": "🎯 Угадай число",

        "back_games": "🔙 Назад к играм",

        "coin_result":
            "🪙 Монета подброшена!\n\n",

        "heads": "🟡 Орёл",
        "tails": "⚪ Решка",
        "coin_count": "🪙 Твои монеты",

        "again": "🔄 Играть снова",

        "dice_result":
            "🎲 Кубик брошен!\n\n",

        "dice_number": "Результат",
        "points_count": "⭐ Твои очки",

        "math_instruction":
            "🧮 МАТЕМАТИКА\n\n"
            "Реши пример:\n\n",

        "math_answer":
            "✍️ Напиши ответ с обычной клавиатуры.",

        "math_correct":
            "✅ Правильно!\n\n"
            "⭐ +1 очко",

        "math_wrong":
            "❌ Неправильно!\n\n"
            "Правильный ответ",

        "next_math": "🧮 Следующий пример",

        "guess_instruction":
            "🎯 ИГРА «УГАДАЙ ЧИСЛО»\n\n"
            "Я загадал число от 1 до 10.\n"
            "Напиши число:",

        "guess_higher":
            "⬆️ Возьми число побольше!",

        "guess_lower":
            "⬇️ Возьми число поменьше!",

        "guess_correct":
            "🎉 Правильно!\n\n"
            "⭐ +1 очко\n"
            "🪙 +2 монеты",

        "language_title":
            "🌐 ВЫБОР ЯЗЫКА\n\n"
            "Какой язык выбрать?",

        "kk_selected":
            "🇰🇿 Выбран казахский язык!",

        "ru_selected":
            "🇷🇺 Выбран русский язык!",

        "en_selected":
            "🇬🇧 Выбран английский язык!",

        "admin":
            "👑 АДМИН\n\n"
            "🤖 Администратор проекта Vireon\n\n"
            "Ты можешь связаться с администратором:",

        "write_admin": "📩 Написать админу",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok",

        "enter_name":
            "✏️ Напиши новое имя:\n\n"
            "Это будет имя твоего профиля внутри Vireon.",

        "name_saved":
            "✅ Имя успешно изменено!",

        "invalid_number":
            "❌ Пожалуйста, напиши только число.",

        "guess_wait":
            "🎯 Сначала напиши число от 1 до 10."
    },


    "en": {

        "welcome":
            "🤖 Welcome to Vireon!\n\n"
            "Choose a section:",

        "profile_button": "👤 Your Profile",
        "games_button": "🎮 Games",
        "language_button": "🌐 Language",
        "admin_button": "👑 Admin",

        "home":
            "🏠 MAIN MENU\n\n"
            "Choose a section:",

        "profile":
            "👤 YOUR PROFILE\n\n",

        "profile_name": "👤 Name",
        "profile_name_none": "Not set",
        "profile_id": "🆔 ID",
        "points": "⭐ Points",
        "coins": "🪙 Coins",

        "change_name": "✏️ Change Name",
        "back": "🔙 Main Menu",

        "games":
            "🎮 GAMES MENU\n\n"
            "Choose a game:",

        "coin": "🪙 Flip Coin",
        "dice": "🎲 Dice",
        "math": "🧮 Math",
        "guess": "🎯 Guess the Number",

        "back_games": "🔙 Back to Games",

        "coin_result":
            "🪙 Coin flipped!\n\n",

        "heads": "🟡 Heads",
        "tails": "⚪ Tails",
        "coin_count": "🪙 Your coins",

        "again": "🔄 Play Again",

        "dice_result":
            "🎲 Dice rolled!\n\n",

        "dice_number": "Result",
        "points_count": "⭐ Your points",

        "math_instruction":
            "🧮 MATH\n\n"
            "Solve this problem:\n\n",

        "math_answer":
            "✍️ Type your answer using the normal keyboard.",

        "math_correct":
            "✅ Correct!\n\n"
            "⭐ +1 point",

        "math_wrong":
            "❌ Wrong!\n\n"
            "Correct answer",

        "next_math": "🧮 Next Problem",

        "guess_instruction":
            "🎯 GUESS THE NUMBER\n\n"
            "I chose a number from 1 to 10.\n"
            "Type your guess:",

        "guess_higher":
            "⬆️ Choose a higher number!",

        "guess_lower":
            "⬇️ Choose a lower number!",

        "guess_correct":
            "🎉 Correct!\n\n"
            "⭐ +1 point\n"
            "🪙 +2 coins",

        "language_title":
            "🌐 LANGUAGE SELECTION\n\n"
            "Which language do you choose?",

        "kk_selected":
            "🇰🇿 Kazakh selected!",

        "ru_selected":
            "🇷🇺 Russian selected!",

        "en_selected":
            "🇬🇧 English selected!",

        "admin":
            "👑 ADMIN\n\n"
            "🤖 Vireon project administrator\n\n"
            "You can contact the administrator:",

        "write_admin": "📩 Contact Admin",
        "youtube": "▶️ YouTube",
        "tiktok": "🎵 TikTok",

        "enter_name":
            "✏️ Enter your new name:\n\n"
            "This will be your profile name inside Vireon.",

        "name_saved":
            "✅ Name successfully changed!",

        "invalid_number":
            "❌ Please enter a number only.",

        "guess_wait":
            "🎯 First, enter a number from 1 to 10."
    }
}


# ==================================================
# USER STATES
# ==================================================

waiting_for_name = set()
math_questions = {}
guess_questions = {}


# ==================================================
# TRANSLATION
# ==================================================

def t(user_id, key):

    data = get_user(user_id)

    language = data["language"]

    return TEXTS[language][key]


# ==================================================
# MAIN MENU
# ==================================================

def main_menu(user_id):

    keyboard = [

        [
            InlineKeyboardButton(
                t(user_id, "profile_button"),
                callback_data="profile"
            )
        ],

        [
            InlineKeyboardButton(
                t(user_id, "games_button"),
                callback_data="games"
            )
        ],

        [
            InlineKeyboardButton(
                t(user_id, "language_button"),
                callback_data="language"
            )
        ],

        [
            InlineKeyboardButton(
                t(user_id, "admin_button"),
                callback_data="admin"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# ==================================================
# PROFILE MENU
# ==================================================

def profile_menu(user_id):

    keyboard = [

        [
            InlineKeyboardButton(
                t(user_id, "change_name"),
                callback_data="change_name"
            )
        ],

        [
            InlineKeyboardButton(
                t(user_id, "back"),
                callback_data="home"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


# ==================================================
# GAMES MENU
# ==================================================

def games_menu(user_id):

    keyboard = [

        [
            InlineKeyboardButton(
                t(user_id, "coin"),
                callback_data="coin"
            )
        ],

        [
            InlineKeyboardButton(
                t(user_id, "dice"),
                callback_data="dice"
            )
        ],

        [
            InlineKeyboardButton(
                t(user_id, "math"),
                callback_data="math"
            )
        ],

        [
            InlineKeyboardButton(
                t(user_id, "guess"),
                callback_data="guess"
