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
import psycopg2


# ==================================================
# BOT TOKEN
# ==================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN табылмады!")


# ==================================================
# DATABASE
# ==================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL табылмады!")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            profile_name TEXT DEFAULT '',
            coins INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            language TEXT DEFAULT 'kk'
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# ==================================================
# USER DATABASE
# ==================================================

def create_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (user_id, profile_name, coins, points, language)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING
    """, (
        user_id,
        "",
        0,
        0,
        "kk"
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_user(user_id):

    create_user(user_id)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, profile_name, coins, points, language
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "user_id": row[0],
        "profile_name": row[1],
        "coins": row[2],
        "points": row[3],
        "language": row[4]
    }


def update_user(user_id, field, value):

    allowed_fields = [
        "profile_name",
        "coins",
        "points",
        "language"
    ]

    if field not in allowed_fields:
        return

    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        UPDATE users
        SET {field} = %s
        WHERE user_id = %s
    """

    cursor.execute(
        query,
        (value, user_id)
    )

    conn.commit()
    cursor.close()
    conn.close()


def add_coins(user_id, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET coins = coins + %s
        WHERE user_id = %s
    """, (amount, user_id))

    conn.commit()
    cursor.close()
    conn.close()


def add_points(user_id, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET points = points + %s
        WHERE user_id = %s
    """, (amount, user_id))

    conn.commit()
    cursor.close()
    conn.close()


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

        "profile_button":
            "👤 Сенің профилің",

        "games_button":
            "🎮 Ойындар",

        "language_button":
            "🌐 Тіл",

        "admin_button":
            "👑 Админ",

        "home":
            "🏠 БАСТЫ МӘЗІР\n\n"
            "Қажетті бөлімді таңда:",

        "profile":
            "👤 СЕНІҢ ПРОФИЛІҢ\n\n",

        "profile_name":
            "👤 Атың",

        "profile_name_none":
            "Қойылмаған",

        "profile_id":
            "🆔 ID",

        "points":
            "⭐ Ұпай",

        "coins":
            "🪙 Монета",

        "change_name":
            "✏️ Атымды өзгерту",

        "back":
            "🔙 Басты мәзір",

        "games":
            "🎮 ОЙЫНДАР МӘЗІРІ\n\n"
            "Ойын таңда:",

        "coin":
            "🪙 Монета лақтыру",

        "dice":
            "🎲 Кубик",

        "math":
            "🧮 Математика",

        "guess":
            "🎯 Болжам",

        "back_games":
            "🔙 Ойындарға қайту",

        "coin_result":
            "🪙 Монета лақтырылды!\n\n",

        "heads":
            "🟡 Аверс",

        "tails":
            "⚪ Реверс",

        "coin_count":
            "🪙 Монетаң",

        "again":
            "🔄 Қайта ойнау",

        "dice_result":
            "🎲 Кубик лақтырылды!\n\n",

        "dice_number":
            "Нәтиже",

        "points_count":
            "⭐ Ұпайың",

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

        "next_math":
            "🧮 Келесі есеп",

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

        "write_admin":
            "📩 Админге жазу",

        "youtube":
            "▶️ YouTube",

        "tiktok":
            "🎵 TikTok",

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

        "profile_button":
            "👤 Твой профиль",

        "games_button":
            "🎮 Игры",

        "language_button":
            "🌐 Язык",

        "admin_button":
            "👑 Админ",

        "home":
            "🏠 ГЛАВНОЕ МЕНЮ\n\n"
            "Выбери нужный раздел:",

        "profile":
            "👤 ТВОЙ ПРОФИЛЬ\n\n",

        "profile_name":
            "👤 Имя",

        "profile_name_none":
            "Не установлено",

        "profile_id":
            "🆔 ID",

        "points":
            "⭐ Очки",

        "coins":
            "🪙 Монеты",

        "change_name":
            "✏️ Изменить имя",

        "back":
            "🔙 Главное меню",

        "games":
            "🎮 МЕНЮ ИГР\n\n"
            "Выбери игру:",

        "coin":
            "🪙 Подбросить монету",

        "dice":
            "🎲 Кубик",

        "math":
            "🧮 Математика",

        "guess":
            "🎯 Угадай число",

        "back_games":
            "🔙 Назад к играм",

        "coin_result":
            "🪙 Монета подброшена!\n\n",

        "heads":
            "🟡 Орёл",

        "tails":
            "⚪ Решка",

        "coin_count":
            "🪙 Твои монеты",

        "again":
            "🔄 Играть снова",

        "dice_result":
            "🎲 Кубик брошен!\n\n",

        "dice_number":
            "Результат",

        "points_count":
            "⭐ Твои очки",

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

        "next_math":
            "🧮 Следующий пример",

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

        "write_admin":
            "📩 Написать админу",

        "youtube":
            "▶️ YouTube",

        "tiktok":
            "🎵 TikTok",

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

        "profile_button":
            "👤 Your Profile",

        "games_button":
            "🎮 Games",

        "language_button":
            "🌐 Language",

        "admin_button":
            "👑 Admin",

        "home":
            "🏠 MAIN MENU\n\n"
            "Choose a section:",

        "profile":
            "👤 YOUR PROFILE\n\n",

        "profile_name":
            "👤 Name",

        "profile_name_none":
            "Not set",

        "profile_id":
            "🆔 ID",

        "points":
            "⭐ Points",

        "coins":
            "🪙 Coins",

        "change_name":
            "✏️ Change Name",

        "back":
            "🔙 Main Menu",

        "games":
            "🎮 GAMES MENU\n\n"
            "Choose a game:",

        "coin":
            "🪙 Flip Coin",

        "dice":
            "🎲 Dice",

        "math":
            "🧮 Math",

        "guess":
            "🎯 Guess the Number",

        "back_games":
            "🔙 Back to Games",

        "coin_result":
            "🪙 Coin flipped!\n\n",

        "heads":
            "🟡 Heads",

        "tails":
            "⚪ Tails",

        "coin_count":
            "🪙 Your coins",

        "again":
            "🔄 Play Again",

        "dice_result":
            "🎲 Dice rolled!\n\n",

        "dice_number":
            "Result",

        "points_count":
            "⭐ Your points",

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

        "next_math":
            "🧮 Next Problem",

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

        "write_admin":
            "📩 Contact Admin",

        "youtube":
            "▶️ YouTube",

        "tiktok":
            "🎵 TikTok",

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
# PROFILE
# ==================================================

async def show_profile(query):

    user = query.from_user

    data = get_user(user.id)

    profile_name = data["profile_name"]

    if not profile_name:

        profile_name = t(
            user.id,
            "profile_name_none"
        )

    text = (

        t(user.id, "profile")

        + f"{t(user.id, 'profile_name')}: "
        + f"{profile_name}\n"

        + f"{t(user.id, 'profile_id')}: "
        + f"{data['user_id']}\n"

        + f"{t(user.id, 'points')}: "
        + f"{data['points']}\n"

        + f"{t(user.id, 'coins')}: "
        + f"{data['coins']}\n"

    )

    await query.edit_message_text(
        text,
        reply_markup=profile_menu(user.id)
    )


# ==================================================
# START
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user.id)

    waiting_for_name.discard(user.id)
    math_questions.pop(user.id, None)
    guess_questions.pop(user.id, None)

    await update.message.reply_text(
        t(user.id, "welcome"),
        reply_markup=main_menu(user.id)
    )


# ==================================================
# BUTTONS
# ==================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    create_user(user.id)

    # ==================================================
    # PROFILE
    # ==================================================

    if query.data == "profile":

        await show_profile(query)

    # ==================================================
    # CHANGE NAME
    # ==================================================

    elif query.data == "change_name":

        waiting_for_name.add(user.id)

        await query.edit_message_text(
            t(user.id, "enter_name")
        )

    # ==================================================
    # GAMES
    # ==================================================

    elif query.data == "games":

        math_questions.pop(user.id, None)
        guess_questions.pop(user.id, None)

        await query.edit_message_text(
            t(user.id, "games"),
            reply_markup=games_menu(user.id)
        )

    # ==================================================
    # COIN
    # ==================================================

    elif query.data == "coin":

        result = random.choice(["heads", "tails"])

        if result == "heads":

            add_coins(user.id, 1)

            result_text = t(
                user.id,
                "heads"
            )

        else:

            result_text = t(
                user.id,
                "tails"
            )

        data = get_user(user.id)

        keyboard = [

            [
                InlineKeyboardButton(
                    t(user.id, "again"),
                    callback_data="coin"
                )
            ],

            [
                InlineKeyboardButton(
                    t(user.id, "back_games"),
                    callback_data="games"
                )
            ]

        ]

        await query.edit_message_text(

            t(user.id, "coin_result")
            + f"🎯 {result_text}\n\n"
            + f"{t(user.id, 'coin_count')}: "
            + f"{data['coins']}",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ==================================================
    # DICE
    # ==================================================

    elif query.data == "dice":

        number = random.randint(1, 6)

        if number >= 4:

            add_points(
                user.id,
                1
            )

        data = get_user(user.id)

        keyboard = [

            [
                InlineKeyboardButton(
                    t(user.id, "again"),
                    callback_data="dice"
                )
            ],

            [
                InlineKeyboardButton(
                    t(user.id, "back_games"),
                    callback_data="games"
                )
            ]

        ]

        await query.edit_message_text(

            t(user.id, "dice_result")
            + f"🎯 {t(user.id, 'dice_number')}: "
            + f"{number}\n"
            + f"{t(user.id, 'points_count')}: "
            + f"{data['points']}",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ==================================================
    # MATH
    # ==================================================

    elif query.data == "math":

        create_math_question(user.id)

        question = math_questions[user.id]

        await query.edit_message_text(

            t(user.id, "math_instruction")
            + f"👉 {question['text']}\n\n"
            + t(user.id, "math_answer"),

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        t(user.id, "back_games"),
                        callback_data="games"
                    )
                ]

            ])
        )

    # ==================================================
    # NEXT MATH
    # ==================================================

    elif query.data == "next_math":

        create_math_question(user.id)

        question = math_questions[user.id]

        await query.edit_message_text(

            t(user.id, "math_instruction")
            + f"👉 {question['text']}\n\n"
            + t(user.id, "math_answer"),

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        t(user.id, "back_games"),
                        callback_data="games"
                    )
                ]

            ])
        )

    # ==================================================
    # GUESS
    # ==================================================

    elif query.data == "guess":

        secret = random.randint(1, 10)

        guess_questions[user.id] = secret

        await query.edit_message_text(

            t(user.id, "guess_instruction"),

            reply_markup=InlineKeyboardMarkup([

                [
                    InlineKeyboardButton(
                        t(user.id, "back_games"),
                        callback_data="games"
                    )
                ]

            ])
        )

    # ==================================================
    # LANGUAGE
    # ==================================================

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
                    t(user.id, "back"),
                    callback_data="home"
                )
            ]

        ]

        await query.edit_message_text(
            t(user.id, "language_title"),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ==================================================
    # LANG KK
    # ==================================================

    elif query.data == "lang_kk":

        update_user(
            user.id,
            "language",
            "kk"
        )

        await query.edit_message_text(
            t(user.id, "kk_selected"),
            reply_markup=main_menu(user.id)
        )

    # ==================================================
    # LANG RU
    # ==================================================

    elif query.data == "lang_ru":

        update_user(
            user.id,
            "language",
            "ru"
        )

        await query.edit_message_text(
            t(user.id, "ru_selected"),
            reply_markup=main_menu(user.id)
        )

    # ==================================================
    # LANG EN
    # ==================================================

    elif query.data == "lang_en":

        update_user(
            user.id,
            "language",
            "en"
        )

        await query.edit_message_text(
            t(user.id, "en_selected"),
            reply_markup=main_menu(user.id)
        )

    # ==================================================
    # ADMIN
    # ==================================================

    elif query.data == "admin":

        keyboard = [

            [
                InlineKeyboardButton(
                    t(user.id, "write_admin"),
                    url=f"https://t.me/{ADMIN_USERNAME}"
                )
            ],

            [
                InlineKeyboardButton(
                    t(user.id, "youtube"),
                    url=YOUTUBE_URL
                )
            ],

            [
                InlineKeyboardButton(
                    t(user.id, "tiktok"),
                    url=TIKTOK_URL
                )
            ],

            [
                InlineKeyboardButton(
                    t(user.id, "back"),
                    callback_data="home"
                )
            ]

        ]

        await query.edit_message_text(
            t(user.id, "admin"),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ==================================================
    # HOME
    # ==================================================

    elif query.data == "home":

        waiting_for_name.discard(user.id)
        math_questions.pop(user.id, None)
        guess_questions.pop(user.id, None)

        await query.edit_message_text(
            t(user.id, "home"),
            reply_markup=main_menu(user.id)
        )


# ==================================================
# CREATE MATH QUESTION
# ==================================================

def create_math_question(user_id):

    operation = random.choice([
        "+",
        "-",
        "*",
        "/"
    ])

    if operation == "+":

        a = random.randint(1, 100)
        b = random.randint(1, 100)

        answer = a + b

        text = f"{a} + {b} = ?"

    elif operation == "-":

        a = random.randint(1, 100)
        b = random.randint(1, 100)

        if b > a:
            a, b = b, a

        answer = a - b

        text = f"{a} - {b} = ?"

    elif operation == "*":

        a = random.randint(2, 20)
        b = random.randint(2, 20)

        answer = a * b

        text = f"{a} × {b} = ?"

    else:

        b = random.randint(2, 12)
        answer = random.randint(1, 12)

        a = b * answer

        text = f"{a} ÷ {b} = ?"

    math_questions[user_id] = {
        "text": text,
        "answer": answer
    }


# ==================================================
# TEXT MESSAGES
# ==================================================

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user.id)

    text = update.message.text.strip()

    # ==================================================
    # CHANGE PROFILE NAME
    # ==================================================

    if user.id in waiting_for_name:

        if len(text) > 30:

            await update.message.reply_text(
                "❌ Атың 30 таңбадан аспауы керек."
            )

            return

        update_user(
            user.id,
            "profile_name",
            text
        )

        waiting_for_name.discard(user.id)

        await update.message.reply_text(
            t(user.id, "name_saved"),
            reply_markup=main_menu(user.id)
        )

        return

    # ==================================================
    # MATH ANSWER
    # ==================================================

    if user.id in math_questions:

        try:

            answer = int(text)

        except ValueError:

            await update.message.reply_text(
                t(user.id, "invalid_number")
            )

            return

        question = math_questions[user.id]

        if answer == question["answer"]:

            add_points(
                user.id,
                1
            )

            keyboard = [

                [
                    InlineKeyboardButton(
                        t(user.id, "next_math"),
                        callback_data="next_math"
                    )
                ],

                [
                    InlineKeyboardButton(
                        t(user.id, "back_games"),
                        callback_data="games"
                    )
                ]

            ]

            await update.message.reply_text(
                t(user.id, "math_correct"),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            math_questions.pop(
                user.id,
                None
            )

        else:

            await update.message.reply_text(

                t(user.id, "math_wrong")
                + f": {question['answer']}",

                reply_markup=InlineKeyboardMarkup([

                    [
                        InlineKeyboardButton(
                            t(user.id, "next_math"),
                            callback_data="next_math"
                        )
                    ],

                    [
                        InlineKeyboardButton(
                            t(user.id, "back_games"),
                            callback_data="games"
                        )
                    ]

                ])
            )

            math_questions.pop(
                user.id,
                None
            )

        return

    # ==================================================
    # GUESS ANSWER
    # ==================================================

    if user.id in guess_questions:

        try:

            number = int(text)

        except ValueError:

            await update.message.reply_text(
                t(user.id, "invalid_number")
            )

            return

        if number < 1 or number > 10:

            await update.message.reply_text(
                t(user.id, "guess_wait")
            )

            return

        secret = guess_questions[user.id]

        if number == secret:

            add_points(
                user.id,
                1
            )

            add_coins(
                user.id,
                2
            )

            keyboard = [

                [
                    InlineKeyboardButton(
                        t(user.id, "guess"),
                        callback_data="guess"
                    )
                ],

                [
                    InlineKeyboardButton(
                        t(user.id, "back_games"),
                        callback_data="games"
                    )
                ]

            ]

            await update.message.reply_text(
                t(user.id, "guess_correct"),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            guess_questions.pop(
                user.id,
                None
            )

        elif number < secret:

            await update.message.reply_text(
                t(user.id, "guess_higher")
            )

        else:

            await update.message.reply_text(
                t(user.id, "guess_lower")
            )

        return


# ==================================================
# DATABASE START
# ==================================================

init_db()


# ==================================================
# APPLICATION
# ==================================================

app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    CallbackQueryHandler(
        button
    )
)


app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_message
    )
)


# ==================================================
# RUN
# ==================================================

print("Vireon бот іске қосылды! 🚀")

app.run_polling()                                 
