from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import FSInputFile, message
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os
import random
import sqlite3
import time
import asyncio

waiting_users = set()
leaderboard_selection_users = set()
CD = 900

base_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(base_dir, "data.env"))

token = os.getenv("BOT_TOKEN")
db_name = os.getenv("DATABASE_v0.1.1").strip()
dev_id = os.getenv("DEV_ID")

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML),)
dp = Dispatcher()

card_names = {
    1: "Водолаз Джо Байден",
    2: "Сикс Севен Джо Байден",
    3: "Праздничный Джо Байден",
    4: "Обычный Джо Байден",
}

db = sqlite3.connect(os.path.join(base_dir, db_name))
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    xp INTEGER DEFAULT 0,
    unlocked_cards INTEGER DEFAULT 0,
    total_cards INTEGER DEFAULT 0,
    last_card_time FLOAT DEFAULT 0
)
""")
db.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_cards (
    user_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, card_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS card_stats (
    card_id INTEGER PRIMARY KEY,
    total_count INTEGER NOT NULL DEFAULT 0,
    first_unlocked TEXT
)
""")

cursor.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cursor.fetchall()]
if "full_name" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
    db.commit()

cursor.execute("""
UPDATE users
SET full_name = 'Anon'
WHERE full_name IS NULL
""")
db.commit()
db.commit()


def add_card(user_id: int, card_id: int, xp_to_add: int, nickname: str):
    cursor.execute(
        """
        INSERT INTO user_cards (user_id, card_id, count)
        VALUES (?, ?, 1)
        ON CONFLICT(user_id, card_id) DO UPDATE SET count = count + 1
        """,
        (user_id, card_id),
    )

    cursor.execute(
        """
        UPDATE users
        SET xp = xp + ?, total_cards = total_cards + 1, last_card_time = ?
        WHERE user_id = ?
        """,
        (xp_to_add, time.time(), user_id,),
    )

    cursor.execute(
        """
        INSERT INTO card_stats (card_id, total_count)
        VALUES (?, 1)
        ON CONFLICT(card_id) DO UPDATE SET total_count = total_count + 1
        """,
        (card_id,),
    )

    cursor.execute(
        """
        UPDATE card_stats
        SET first_unlocked = ?
        WHERE card_id = ? AND first_unlocked IS NULL
        """,
        (nickname, card_id,),
    )
    db.commit()


def get_user_card_count(user_id: int, card_id: int) -> int:
    cursor.execute(
        """
        SELECT count
        FROM user_cards
        WHERE user_id = ? AND card_id = ?
        """,
        (user_id, card_id),
    )
    row = cursor.fetchone()
    return row[0] if row else 0


def get_world_card_count(card_id: int) -> int:
    cursor.execute(
        """
        SELECT total_count
        FROM card_stats
        WHERE card_id = ?
        """,
        (card_id,),
    )
    row = cursor.fetchone()
    return row[0] if row else 0


@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id != dev_id:
        return

    if message.from_user.id == dev_id:
        text = (
         "<b>ОБНОВА v0.1.1 ВЫШЛА</b>\n\n"
         "Новое:\n"
         "<blockquote>- Изменение лидерборда: добавлена система опыта, полученное количество которой зависит от выбитой карточки, чем реже карточка - тем больше опыта. Сортировка лидерборда по трем категориям: по опыту, коллекции (сколько видов карт у вас открыто) и по первенству (игроки которые получили первыми определенные карточки.)\n"
         "- Напоминания о завершении КД и неактивности.\n"
         "- Уведомления при выполнении разных достижений, например получении первым конкретной карточки или открытии полной коллекции.\n"
         "- Уникальные описания для карточек.</blockquote>\n\n"
         "Баги:\n"
         "<blockquote>- Пофикшен баг при котором шансы распределялись неправильно. На Сикс Севен Джо Байдена шанс был больше чем на обычного и остальные карточки выпадали с высшим шансом чем должны были.\n"
         "- Пофикшены небольшие ошибки в тексте и форматировании.</blockquote>\n\n"
         "Баланс:\n"
         "<blockquote>- КД уменьшен до 15 минут (30m > 15m)\n"
         "- Изменения в редкости карточек (Водолаз 2% > 5%; Сикс Севен 20% > 10%; Праздничный 8% > 30%; Обычный 70% > 55%)</blockquote>\n\n"
         "QoL:\n"
         "<blockquote>- Изменен дизайн Водолаза Джо Байдена.\n"
         "- По многочисленным просьбам игроков Сикс Севен Джо Байден теперь имеет редкость которую раньше имел Праздничный Джо Байден.\n"
         "- В лидерборде теперь отображаются ники а не юзернеймы.</blockquote>\n\n"
         "Также в виде компенсации за обнуленное количество карточек и в честь триумфа голоса игроков всем доступен x1 Сикс Севен Джо Байден и x30 XP. Для получения введите команду /claim ."
        )
        await message.answer("🚀 Рассылка запущена..")

        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        count = 0

        for row in rows:
            user_id = row[0]
            try:
                await bot.send_message(chat_id=user_id, text=text)
                count += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Ошибка при отправке {user_id}: {e}")

        await message.answer(f"✅ Рассылка завершена! Сообщение получили {count} пользователей.")


@dp.message(Command("claim"))
async def gift_claiming(message: types.Message):
    user_id = message.from_user.id

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
        (user_id, message.from_user.full_name or "Anon"),
    )

    cursor.execute(
        "SELECT count FROM user_cards WHERE user_id = ? AND card_id = 2",
        (user_id,),
    )
    row = cursor.fetchone()

    if time.time() >= 1777280400:
        text = "⏱️ Срок получения подарка истек. Его действие закончилось 27 апреля в 12:00."
        await message.answer(text)
    else:
        if row is None:
            cursor.execute(
                "UPDATE users SET xp = xp + 30 WHERE user_id = ?",
                (user_id,),
            )
            cursor.execute(
                "UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?",
                (user_id,),
            )
            cursor.execute(
                "UPDATE users SET total_cards = total_cards + 1 WHERE user_id = ?",
                (user_id,),
            )
            cursor.execute(
                """
                INSERT INTO user_cards (user_id, card_id, count)
                SELECT user_id, 2, 1 FROM users WHERE user_id = ?
                """,
                (user_id,),
            )
            text = "🎁 Вы успешно получили <b>x30 опыта</b> и <b>x1 Сикс Севен Джо Байден</b> в честь обновления!"
            db.commit()
            await message.answer(text)
        else:
            text = "❗ Вы уже забрали данный подарок."
            await message.answer(text)


async def reminder():
    while True:
        await asyncio.sleep(3600)
        cursor.execute("SELECT user_id, last_card_time FROM users")
        rows = cursor.fetchall()

        for user_id, last_card_time in rows:
            diff = (time.time() - last_card_time)

            if last_card_time == 0:
                continue

            if user_id in waiting_users:
                continue
            else:
                if 86400 <= diff < 90000:
                    random_reminder = random.randint(1, 4)
                    if random_reminder == 1:
                        text = "С момента твоего последнего открытия прошло уже более дня! Ты собираешься играть, или просто дашь обогнать себя в лидерборде?!\n\nНажми /card чтоб открыть набор карточек."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 2:
                        text = "Другие игроки вот-вот обгонят тебя и твой опыт зарастет мхом! У тебя остался последний шанс прежде ты упадешь в лидерборде.\n\nНажми /card чтоб открыть набор карточек."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 3:
                        text = "Джо Байден соскучился по тебе.. Ты не открывал наборы с карточками уже почти 24 часа. У тебя что-то случилось?\n\n Если не хочешь расстроить Джо Байдена еще больше, нажми /card чтоб открыть набор карточек."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 4:
                        text = "Хочешь получить Водолаза? Так делай хоть что-то, а то с момента твоего последнего открытия прошел уже целый день!\n\nНе хочешь оказаться на дне как Водолаз? Заходи и открывай набор с карточками через /card ."
                        await bot.send_message(chat_id=user_id, text=text)

                elif 28800 <= diff < 32400:
                    random_reminder = random.randint(1, 4)
                    if random_reminder == 1:
                        text = "Я имел большие надежды на тебя, а ты просто взял и забил! Выбрал личную жизнь, а не меня!\n\nВдруг захочешь исправиться в моих глазах - команда /card тебе поможет."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 2:
                        text = "Хорошо. Я пытался заинтересовать тебя, дать шанс.. Но раз ты не открываешь карточки уже 8 часов, что ж поделаешь!\n\nВдруг захочешь исправиться - нажми команду /card."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 3:
                        text = "Ах ты проказник вот такой! Не заходишь в бота уже 8 часов, значит плакал за тобой Водолаз! Не быть тебе топ 1 мира с такой дисциплиной.\n\nНажми /card чтоб открыть набор карточек."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 4:
                        text = "Легенда гласит - если прямо сейчас откроешь набор, тебе выпадет твоя заветная карточка. Я ведь мудрец - а мудрецы не ошибаются.\n\nВдруг тебе и правда повезет? Просто нажми /card ."
                        await bot.send_message(chat_id=user_id, text=text)

                elif 7200 <= diff < 10800:
                    random_reminder = random.randint(1, 3)
                    if random_reminder == 1:
                        text = "С момента вашего последнего открытия прошло уже около 2 часов.\n\nНажмите /card для открытия."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 2:
                        text = "Твои конкуренты уже лутают опыт во всю, а ты что?\n\nНажми /card и компенсируй утерянное."
                        await bot.send_message(chat_id=user_id, text=text)
                    elif random_reminder == 3:
                        text = "Раз ты хочешь получить хотя-бы Праздничного Джо, лучше не забывай открывать карточки. А там, вдруг ты захочешь поохотиться за Водолазом и топ 1 мира.\n\nНажми /card чтоб открыть набор карточек."
                        await bot.send_message(chat_id=user_id, text=text)

                elif 0 <= diff < 3600:
                    text = "⏱️ КД обычного набора карточек закончился! Нажмите /card для открытия."
                    await bot.send_message(chat_id=user_id, text=text)


@dp.message(Command("leaderboard"))
async def show_leaderboard(message: types.Message):
    user_id = message.from_user.id
    leaderboard_selection_users.add(user_id)
    text = "Выберите режим лидерборда для его просмотра (по опыту/по коллекции/по первенству)"
    await message.answer(text)


@dp.message(lambda msg: msg.text and msg.text.lower() in ["по опыту", "по коллекции", "по первенству"])
async def change_of_leaderoard_mode(message: types.Message):
    user_id = message.from_user.id

    if user_id not in leaderboard_selection_users:
        return

    if user_id in leaderboard_selection_users:
        answer = message.text.strip().lower()

        if answer == "по первенству":
            cursor.execute("SELECT card_id, first_unlocked FROM card_stats WHERE first_unlocked IS NOT NULL ORDER BY card_id")
            users = cursor.fetchall()

            results = "<b>🏆 ЛИДЕРБОРД</b>\n"
            results += "Режим: По опыту | По коллекции | <b>По первенству</b>\n\n"

            for i, user in enumerate(users, 1):
                results += f" {user[1]} - открыл <b>{card_names[user[0]]}</b> первым в мире\n"

            cursor.execute("SELECT SUM(total_count) FROM card_stats")
            row = cursor.fetchone()
            results += f"\nВсего карточек существует: {row[0] if row and row[0] else 0}\n\n"

            await message.answer(results)

        elif answer == "по коллекции":
            cursor.execute("SELECT full_name, unlocked_cards FROM users ORDER BY unlocked_cards DESC LIMIT 10")
            users = cursor.fetchall()

            results = "<b>🏆 ЛИДЕРБОРД</b>\n"
            results += "Режим: По опыту | <b>По коллекции</b> | По первенству\n\n"

            for i, user in enumerate(users, 1):
                medal = "👑" if i == 1 else f"{i}."
                results += f"{medal} {user[0]} — {user[1]}/4 карт\n"

            cursor.execute("SELECT SUM(total_count) FROM card_stats")
            total_cards_count = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM users WHERE unlocked_cards = 4")
            users_with_full_coll = cursor.fetchone()[0] or 0

            results += f"\nВсего карточек существует: {total_cards_count} | Игроков с полной коллекцией: {users_with_full_coll}"
            await message.answer(results)

        elif answer == "по опыту":
            cursor.execute("SELECT full_name, xp FROM users ORDER BY xp DESC LIMIT 10")
            users = cursor.fetchall()

            results = "<b>🏆 ЛИДЕРБОРД</b>\n"
            results += "Режим: <b>По опыту</b> | По коллекции | По первенству\n\n"

            for i, user in enumerate(users, 1):
                medal = "👑" if i == 1 else f"{i}."
                results += f"{medal} {user[0]} — {user[1]} опыта\n"

            cursor.execute("SELECT SUM(total_count) FROM card_stats")
            row = cursor.fetchone()
            results += f"\nВсего карточек существует: {row[0] if row and row[0] else 0}\n\n"

            await message.answer(results)

        leaderboard_selection_users.discard(user_id)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        "👋 Привет, ты попал в Joe Biden Cards.\n"
        "Здесь ты можешь выбивать разные карточки с Джо Байденом, коллекционировать их и просто проводить время\n\n"
        "Бот находится в начальной разработке, поэтому в нем могут присутствовать некоторые баги.\n\n"
        "Создано @by_when ; весь материал в боте используется исключительно в шуточных целях\n\n"
        "Чтоб начать пользоваться ботом используйте команду /card\n\n"
        "Актуальная версия: v0.1.1"
    )
    await message.answer(text)


@dp.message(Command("menu"))
async def handle_answer(message: types.Message):
    nickname = message.from_user.full_name
    user_id = message.from_user.id

    cursor.execute(
        "SELECT total_cards, last_card_time FROM users WHERE user_id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    total_cards = row[0] if row else 0

    cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
    info = cursor.fetchone()
    xp = info[0] if info else 0

    cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
    one_more_info = cursor.fetchone()
    collected = one_more_info[0] if one_more_info else 0

    text = (
        "<b>🏠 МЕНЮ</b>\n"
        f"Ник: {nickname} | {xp} XP\n\n"
        f"Водолаз Джо Байден - x{get_user_card_count(user_id, 1)}\n"
        f"Сикс Севен Джо Байден - x{get_user_card_count(user_id, 2)}\n"
        f"Праздничный Джо Байден - x{get_user_card_count(user_id, 3)}\n"
        f"Обычный Джо Байден - x{get_user_card_count(user_id, 4)}\n"
        f"В общем: {total_cards}; Собрано: {collected}/4\n\n"
        "Чтоб открыть карточку нажмите /card"
    )
    await message.answer(text)


@dp.message(Command("card"))
async def handle_answer(message: types.Message):
    user_id = message.from_user.id

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
        (user_id, message.from_user.full_name),
    )
    db.commit()

    username = message.from_user.username or "Anon"

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
        (user_id, message.from_user.full_name or "Anon"),
    )
    cursor.execute(
        "UPDATE users SET full_name = ? WHERE user_id = ?",
        (message.from_user.full_name or "Anon", user_id),
    )
    db.commit()

    cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
    last_opening_time = cursor.fetchone()[0]
    current_time = time.time()

    waiting_users.add(user_id)

    text = (
        "<b>🃏 Обычный набор карт с Джо Байденом</b>\n\n"
        "• Шансы:\n\n"
        "???\n"
        "Водолаз Джо Байден - 5%\n"
        "Сикс Севен Джо Байден - 10%\n"
        "Праздничный Джо Байден - 30%\n"
        "Обычный Джо Байден - 55%\n\n"
        "Напишите Y чтоб открыть или N чтоб отменить."
    )
    await message.answer(text)


@dp.message()
async def handle_all_messages(message: types.Message):
    nickname = message.from_user.full_name
    user_id = message.from_user.id

    if user_id in waiting_users:
        if not message.text:
            return

        answer = message.text.lower()

        if answer == "y":
            cursor.execute(
                "SELECT unlocked_cards FROM users WHERE user_id = ?",
                (user_id,),
            )
            count_before = cursor.fetchone()[0]

            cursor.execute(
                "SELECT last_card_time FROM users WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            last_opening_time = row[0] if row else 0

            current_left = CD - int(time.time() - last_opening_time)

            if current_left <= 0:
                chance = random.randint(1, 100)

                if chance <= 5:  # 1, 2, 3, 4, 5
                    xp_to_add = 40
                    add_card(user_id, 1, xp_to_add, nickname)

                    if get_user_card_count(user_id, 1) == 1:
                        cursor.execute(
                            "UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?",
                            (user_id,),
                        )
                        db.commit()

                    photo = FSInputFile(os.path.join(base_dir, "images", "ВодолазДжоБайден.jpg"))
                    text = (
                        "Вам выпал..\n"
                        "- <b>Водолаз Джо Байден - 5%!</b>\n"
                        "+40 XP\n\n"
                        "<blockquote>— нырнул в разговор и не вынырнул. Говорит много, звучит умно, смысл утонул где-то на глубине.</blockquote>\n\n"
                        f"Количество: {get_user_card_count(message.from_user.id, 1)}\n"
                        f"Всего в мире: {get_world_card_count(1)}\n\n"
                        "Для просмотра вашей обновленной коллекции нажмите /menu"
                    )
                    await message.answer_photo(photo=photo, caption=text)

                    cursor.execute(
                        "SELECT unlocked_cards FROM users WHERE user_id = ?",
                        (user_id,),
                    )
                    count_after = cursor.fetchone()[0]

                    if get_world_card_count(1) == 1:
                        text = (
                            "Вы первыми в мире открыли <b>Водолаза Джо Байдена</b>!\n+40 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
                        )
                        await message.answer(text)
                        xp_to_add = 40
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()
                    if count_after == 4 and count_before == 3:
                        text = (
                            "Вы собрали полную коллекцию Джо Байденов!\n"
                            "Последней нужной картой стал Водолаз Джо Байден.\n"
                            " +125 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
                        )
                        xp_to_add = 125
                        await message.answer(text)
                        xp_to_add = 125
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()
                elif chance <= 15:  # 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
                    xp_to_add = 15
                    add_card(user_id, 2, xp_to_add, nickname)

                    if get_user_card_count(user_id, 2) == 1:
                        cursor.execute(
                            "UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?",
                            (user_id,),
                        )
                        db.commit()

                    photo = FSInputFile(os.path.join(base_dir, "images", "67ДжоБайден.jpg"))
                    text = (
                        "Вам выпал..\n"
                        "- <b>Сикс Севен Джо Байден - 10%!</b>\n"
                        "+15 XP\n\n"
                        "<blockquote>— 67 67 67. Никто не знает что это значит, но если не уважаешь 67 — ты вне цивилизации.</blockquote>\n\n"
                        f"Количество: {get_user_card_count(message.from_user.id, 2)}\n"
                        f"Всего в мире: {get_world_card_count(2)}\n\n"
                        "Для просмотра вашей обновленной коллекции нажмите /menu"
                    )
                    await message.answer_photo(photo=photo, caption=text)

                    cursor.execute(
                        "SELECT unlocked_cards FROM users WHERE user_id = ?",
                        (user_id,),
                    )
                    count_after = cursor.fetchone()[0]

                    if get_world_card_count(2) == 1:
                        text = (
                            "Вы первыми в мире открыли <b>Сикс Севен Джо Байдена</b>!\n+15 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
                        )
                        await message.answer(text)
                        xp_to_add = 15
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()
                    if count_after == 4 and count_before == 3:
                        text = (
                            "Вы собрали полную коллекцию Джо Байденов!\n"
                            "Последней нужной картой стал Сикс Севен Джо Байден.\n"
                            " +125 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
                        )
                        xp_to_add = 125
                        await message.answer(text)
                        xp_to_add = 125
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()

                elif chance <= 45:  # 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45
                    xp_to_add = 6
                    add_card(user_id, 3, xp_to_add, nickname)

                    if get_user_card_count(user_id, 3) == 1:
                        cursor.execute(
                            "UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?",
                            (user_id,),
                        )
                        db.commit()

                    photo = FSInputFile(os.path.join(base_dir, "images", "ПраздничныйДжоБайден.jpg"))
                    text = (
                        "Вам выпал..\n"
                        "- <b>Праздничный Джо Байден - 30%!</b>\n"
                        "+6 XP\n\n"
                        "<blockquote>— это когда торт уже не торт, а государственное событие.</blockquote>\n\n"
                        f"Количество: {get_user_card_count(message.from_user.id, 3)}\n"
                        f"Всего в мире: {get_world_card_count(3)}\n\n"
                        "Для просмотра вашей обновленной коллекции нажмите /menu"
                    )
                    await message.answer_photo(photo=photo, caption=text)

                    cursor.execute(
                        "SELECT unlocked_cards FROM users WHERE user_id = ?",
                        (user_id,),
                    )
                    count_after = cursor.fetchone()[0]

                    if get_world_card_count(3) == 1:
                        text = (
                            "Вы первыми в мире открыли <b>Праздничного Джо Байдена</b>!\n+6 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
                        )
                        await message.answer(text)
                        xp_to_add = 6
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()
                    if count_after == 4 and count_before == 3:
                        text = (
                            "Вы собрали полную коллекцию Джо Байденов!\n"
                            "Последней нужной картой стал Праздничный Джо Байден.\n"
                            " +125 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
                        )
                        await message.answer(text)
                        xp_to_add = 125
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()

                else:  # 55-100
                    xp_to_add = 2
                    add_card(user_id, 4, xp_to_add, nickname)

                    if get_user_card_count(user_id, 4) == 1:
                        cursor.execute(
                            "UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?",
                            (user_id,),
                        )
                        db.commit()

                    photo = FSInputFile(os.path.join(base_dir, "images", "ОбычныйДжоБайден.jpg"))
                    text = (
                        "Вам выпал..\n"
                        "- <b>Обычный Джо Байден - 55%!</b>\n"
                        "+2 XP\n\n"
                        "<blockquote>— literally дефолт скин. Ничего не делает, просто стоит, но почему-то уже происходит лор. Если выпал — значит игра сказала “ну держи хоть что-то”.</blockquote>\n\n"
                        f"Количество: {get_user_card_count(message.from_user.id, 4)}\n"
                        f"Всего в мире: {get_world_card_count(4)}\n\n"
                        "Для просмотра вашей обновленной коллекции нажмите /menu"
                    )
                    await message.answer_photo(photo=photo, caption=text)

                    cursor.execute(
                        "SELECT unlocked_cards FROM users WHERE user_id = ?",
                        (user_id,),
                    )
                    count_after = cursor.fetchone()[0]

                    if get_world_card_count(4) == 1:
                        text = (
                            "Вы первыми в мире открыли <b>Обычного Джо Байдена</b>!\n+2 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
                        )
                        await message.answer(text)
                        xp_to_add = 2
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()
                    if count_after == 4 and count_before == 3:
                        text = (
                            "Вы собрали полную коллекцию Джо Байденов!\n"
                            "Последней нужной картой стал Обычный Джо Байден.\n"
                            " +125 XP\n\n"
                            "Вы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
                        )
                        await message.answer(text)
                        xp_to_add = 125
                        cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
                        db.commit()

                new_time = time.time()
                waiting_users.discard(user_id)
            else:
                minutes = current_left // 60
                seconds = current_left % 60
                text = f"⏱️ Сейчас данный набор находится в КД. Вы сможете открыть его через <b> {minutes}m {seconds}s</b>."
                await message.answer(text)

                waiting_users.discard(user_id)

        elif answer == "n":
            text = "Открытие отменено."
            await message.answer(text)
            waiting_users.discard(user_id)
            return
        else:
            waiting_users.discard(user_id)


async def main():
    asyncio.create_task(reminder())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")