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
ver_selection_users = set()
leaderboard_selection_users = set()
CD = 900

base_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(base_dir, "data.env"))

token = os.getenv("BOT_TOKEN")
db_name = os.getenv("DATABASE_v0.1.1.1").strip()
dev_id = int(os.getenv("DEV_ID"))

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML),)
dp = Dispatcher()
card_names = {
 1: "Водолаз Джо Байден",
 2: "Сикс Севен Джо Байден",
 3: "Праздничный Джо Байден",
 4: "Обычный Джо Байден"
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


def add_card(user_id: int, card_id: int, xp_to_add: int, nickname: str):
 cursor.execute("""
  INSERT INTO user_cards (user_id, card_id, count)
  VALUES (?, ?, 1)
  ON CONFLICT(user_id, card_id)
  DO UPDATE SET count = count + 1
  """, (user_id, card_id))
 cursor.execute("""
  UPDATE users
  SET xp = xp + ?, total_cards = total_cards + 1, last_card_time = ?
  WHERE user_id = ?       
 """, (xp_to_add, time.time(), user_id,))
 cursor.execute("""
  INSERT INTO card_stats (card_id, total_count)
  VALUES (?, 1)
  ON CONFLICT(card_id)
  DO UPDATE SET total_count = total_count + 1
  """, (card_id,))
 cursor.execute("""
  UPDATE card_stats
  SET first_unlocked = ?
  WHERE card_id = ? AND first_unlocked IS NULL
  """, (nickname, card_id,))
 db.commit()
def get_user_card_count(user_id: int, card_id: int) -> int:
    cursor.execute("""
        SELECT count FROM user_cards
        WHERE user_id = ? AND card_id = ?
    """, (user_id, card_id))
    row = cursor.fetchone()
    return row[0] if row else 0
def get_world_card_count(card_id: int) -> int:
    cursor.execute("""
        SELECT total_count FROM card_stats
        WHERE card_id = ?
    """, (card_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

@dp.message(Command("all_info"))  # АДМИН КОМАНДА v0.1.1.3+
async def showing_db_info(message: types.Message):
 if message.from_user.id not in [dev_id, 6776823399]:
  text = "У вас недостаточно прав для использования команды /all_info."
  await message.answer(text)
  return
 cursor.execute("SELECT user_id FROM users")
 ids = [rows[0] for rows in cursor.fetchall()]
 text = "<b>ВСЯ ИНФОРМАЦИЯ</b>\n"
 for id in ids:
  cursor.execute("SELECT full_name, xp,  total_cards, unlocked_cards FROM users WHERE user_id = ?", (id,))
  row = cursor.fetchone()
  full_name, xp, total_cards, unlocked_cards = row if row else ("Anon", 0, 0, 0)
  text += f"\n<b>{full_name} – {id} | {xp} XP</b>\n"
  cursor.execute("SELECT card_id, count FROM user_cards WHERE user_id = ?", (id,))
  user_cards = cursor.fetchall()
  for card_id, count in user_cards:
   card_name = card_names.get(card_id, f"Карта не найдена")
   text += f"{card_name} — x{count}\n"
  text += f"В общем: {total_cards} карт | Открыто: {unlocked_cards}/4 карт\n"
  if id == 2041528836:
   text += (
    "\nПервый в мире <b>Водолаз Джо Байден</b>\n"
    "Первый в мире <b>Сикс Севен Джо Байден</b>\n"
    "Первый в мире <b>Праздничный Джо Байден</b>\n"
    "Первый в мире <b>Обычный Джо Байден</b>\n\n"
   )
 cursor.execute("SELECT SUM(total_count) FROM card_stats")
 row = cursor.fetchone()
 total_count = row[0] if row and row[0] is not None else 0
 cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id IN (7020510390, 7481475946)")
 row = cursor.fetchone()
 when_total_count = row[0] if row and row[0] is not None else 0
 cursor.execute("SELECT SUM(xp) FROM users")
 row = cursor.fetchone()
 total_xp = row[0] if row and row[0] is not None else 0
 cursor.execute("SELECT SUM(xp) FROM users WHERE user_id IN (7020510390, 7481475946)")
 row = cursor.fetchone()
 when_total_xp = row[0] if row and row[0] is not None else 0
 text += f"\n<b>В общем: {total_count - when_total_count} ({total_count}) карт | {total_xp - when_total_xp} ({total_xp}) XP</b>"
 if len(text) >= 4096:
  part1 = text[:4096].replace("<b>", "").replace("</b>", "")
  part2 = text[4096:].replace("<b>", "").replace("</b>", "")
  await message.answer(part1)
  await asyncio.sleep(2)
  await message.answer(part2)
 else:
  await message.answer(text)

if int(time.time()) in range(1780577400, 1780578600):
 cursor.execute("DELETE FROM user_cards WHERE user_id = 6776823399")
 cursor.execute("DELETE FROM users WHERE user_id = 6776823399")
 db.commit()
 time.sleep(5)
 cursor.execute("""
  INSERT INTO users (user_id, full_name, xp, total_cards, unlocked_cards) 
  VALUES (6776823399, '𔓕 ⊹ ◜⛩️◞  ꩜ すばらしい ꩜ ◜🪽◞ `⌁', 402, 37, 4)
 """)
 cursor.execute("INSERT INTO user_cards (user_id, card_id, count) VALUES (6776823399, 1, 3)")
 cursor.execute("INSERT INTO user_cards (user_id, card_id, count) VALUES (6776823399, 2, 2)")
 cursor.execute("INSERT INTO user_cards (user_id, card_id, count) VALUES (6776823399, 3, 12)")
 cursor.execute("INSERT INTO user_cards (user_id, card_id, count) VALUES (6776823399, 4, 20)")
 db.commit()

@dp.message(Command("broadcast"))  # АДМИН КОМАНДА v0.1.1+
async def broadcast(message: types.Message):
 if message.from_user.id != dev_id:
  text = "У вас недостаточно прав для использованя команды /broadcast."
  await message.answer(text)
  return
 text = ( 
  "<b>Бот стал доступен на GitHub</b>!\n\n"
  "https://github.com/wheennn/Joe-Biden-Cards-Bot-RU\n\n"
  "Также теперь работа бота <b>возобновлена</b> благодаря тому, что с этого момента он находится на сервере @Subarash_ii "
 )
 cursor.execute("SELECT user_id FROM users")
 rows = cursor.fetchall()
 count = 0
 await message.answer("🚀 Рассылка запущена..")
 for row in rows:
  user_id = row[0]
  try:
   await message.bot.send_message(chat_id=user_id, text=text)
   count += 1
   await asyncio.sleep(0.1) 
  except Exception as e:
   print(f"Ошибка при отправке {user_id}: {e}")
 await message.answer(f"✅ Рассылка завершена! Сообщение получили {count} пользователей.")
   
cursor.execute("PRAGMA table_info(users)") # ВРЕМЕННАЯ ЗАЧИСТКА ДАТАБАЗЫ v0.1.1.3
columns = cursor.fetchall()
column_names = [col[1] for col in columns]
columns_to_drop = ["first_event_reward", "second_event_reward", "third_event_reward"]
for col in columns_to_drop:
 if col in column_names:
  cursor.execute(f"ALTER TABLE users DROP COLUMN {col}")
  print(f"Столбец '{col}' успешно удален.")
 else:
  print(f"Столбец '{col}' отсутствует. Пропущено.")
db.commit()

@dp.message(Command("claim")) # КОМАНДА ДЛЯ ПОЛУЧЕНИЯ ПОДАРКОВ v0.1.1+
async def gift_claiming(message: types.Message):
 user_id = message.from_user.id
 cursor.execute(
    "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
    (user_id, message.from_user.full_name or "Anon")
 )
 cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = 2", (user_id,))
 row = cursor.fetchone()
 if time.time() >= 1780318800:
  text = "⏱️ Срок получения подарка истек. Его действие закончилось 2 мая в 00:00."
  await message.answer(text)
 else:
  if row is None:
   cursor.execute("UPDATE users SET xp = xp + 30 WHERE user_id = ?", (user_id,))
   cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
   cursor.execute("UPDATE users SET total_cards = total_cards + 1 WHERE user_id = ?", (user_id,))
   cursor.execute("""
    INSERT INTO user_cards (user_id, card_id, count)
    SELECT user_id, 2, 1 FROM users WHERE user_id = ?
   """, (user_id,))
   text = "🎁 Вы успешно получили <b>x30 опыта</b> и <b>x1 Сикс Севен Джо Байден</b> в честь выхода v0.1.1.1!"
   db.commit()
   await message.answer(text)
  else:
   text = "❗ Вы уже забрали данный подарок."
   await message.answer(text)


async def reminder(): # СИСТЕМА НАПОМИНАНИЙ v0.1.1+
 while True:
  cursor.execute("SELECT user_id, last_card_time FROM users")
  rows = cursor.fetchall()
  for user_id, last_card_time in rows:
   if last_card_time == 0: 
    continue
   if user_id in waiting_users:
    continue
   diff = (time.time() - last_card_time)
   try:
    if 84600 <= diff < 90000: # ОДИН ДЕНЬ НЕАКТИВА (1ч. окно)
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
    elif 26000 <= diff < 31400: # ВОСЕМЬ ЧАСОВ НЕАКТИВА (1ч. окно)
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
    elif 5400 <= diff < 10800: # ДВА ЧАСА НЕАКТИВА (1ч. окно)
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
    elif 1800 <= diff < 7200: # ПЯТНАДЦАТЬ МИНУТ НЕАКТИВА (1ч. окно)
     text = "⏱️ КД обычного набора карточек закончился! Нажмите /card для открытия."
     await bot.send_message(chat_id=user_id, text=text)
   except Exception as e:
    print(f"Не удалось отправить уведомление для {user_id}: {e}")
  unique_time_check = random.randint(1800, 3600)
  await asyncio.sleep(unique_time_check)



@dp.message(Command("leaderboard")) # СПИСОК ЛИДЕРОВ v0.1+
async def show_leaderboard(message: types.Message):
 user_id = message.from_user.id
 leaderboard_selection_users.add(user_id)
 text = "Выберите режим лидерборда для его просмотра (по опыту/по коллекции/по первенству)"
 await message.answer(text)

@dp.message(lambda msg: msg.text and msg.text.lower() in ["по опыту", "по", "xp", "по коллекции", "пк", "по первенству", "пп"])
async def change_of_leaderoard_mode(message: types.Message):
 user_id = message.from_user.id
 if user_id not in leaderboard_selection_users:
  return
 if user_id in leaderboard_selection_users:
  answer = message.text.strip().lower()
  if answer in ["по первенству", "пп"]:
   results = "<b>🏆 ЛИДЕРБОРД</b>\n"
   results += "Режим: По опыту | По коллекции | <b>По первенству</b>\n\n"
   results += (
    "cwendyzz - открыл <b>Водолаз Джо Байден</b> первым в мире\n"
    "cwendyzz - открыл <b>Сикс Севен Джо Байден</b> первым в мире\n"
    "cwendyzz - открыл <b>Праздничный Джо Байден</b> первым в мире\n"
    "cwendyzz - открыл <b>Обычный Джо Байден</b> первым в мире\n\n"
   )
   cursor.execute("SELECT SUM(total_count) FROM card_stats")
   row = cursor.fetchone()
   total_cards = row[0] if row and row[0] else 0
   cursor.execute("SELECT total_cards FROM users WHERE user_id = 7020510390")
   devs_cards = 0
   row = cursor.fetchone()
   devs_cards += int(row[0] if row else 0)
   cursor.execute("SELECT total_cards FROM users WHERE user_id = 7481475946")
   row = cursor.fetchone()
   devs_cards += int(row[0] if row else 0)
   results += f"Всего карточек существует: {total_cards - devs_cards}\n\n"
   await message.answer(results)

  elif answer in ["по коллекции", "пк"]:
   cursor.execute("SELECT full_name, unlocked_cards FROM users ORDER BY unlocked_cards DESC LIMIT 10")
   users = cursor.fetchall()
   results = "<b>🏆 ЛИДЕРБОРД</b>\n"
   results += "Режим: По опыту | <b>По коллекции</b> | По первенству\n\n"
   rank = 1
   for user in users:
    if user[0] == "Wheen17":
     continue
    if user[0] == "whenn?🍂":
     continue
    medal = "👑" if rank == 1 else f"{rank}"
    results += f"{medal}. {user[0]} - открыто {user[1]}/4 карт\n"
    rank += 1
   cursor.execute("SELECT SUM(total_count) FROM card_stats")
   row = cursor.fetchone()
   total_cards = row[0] if row and row[0] else 0
   cursor.execute("SELECT total_cards FROM users WHERE user_id = 7020510390")
   devs_cards = 0
   row = cursor.fetchone()
   devs_cards += int(row[0] if row else 0)
   cursor.execute("SELECT total_cards FROM users WHERE user_id = 7481475946")
   row = cursor.fetchone()
   devs_cards += int(row[0] if row else 0)
   cursor.execute("SELECT COUNT(*) FROM users WHERE unlocked_cards = 4")
   users_with_full_coll = cursor.fetchone()[0] or 0
   results += f"\nВсего карточек существует: {total_cards - devs_cards} | Игроков с полной коллекцией: {users_with_full_coll - 2}"
   await message.answer(results)

  elif answer in ["по опыту", "по", "xp"]:
   cursor.execute("SELECT full_name, xp FROM users ORDER BY xp DESC LIMIT 10")
   users = cursor.fetchall()
   results = "<b>🏆 ЛИДЕРБОРД</b>\n"
   results += "Режим: <b>По опыту</b> | По коллекции | По первенству\n\n"
   rank = 1
   for user in users:
    if user[0] == "Wheen17":
     continue
    if user[0] == "whenn?🍂":
     continue
    medal = "👑" if rank == 1 else f"{rank}"
    results += f"{medal}. {user[0]} - {user[1]} XP\n"
    rank += 1
   cursor.execute("SELECT SUM(total_count) FROM card_stats")
   row = cursor.fetchone()
   total_cards = row[0] if row and row[0] else 0
   cursor.execute("SELECT total_cards FROM users WHERE user_id = 7020510390")
   devs_cards = 0
   row = cursor.fetchone()
   devs_cards += int(row[0] if row else 0)
   cursor.execute("SELECT total_cards FROM users WHERE user_id = 7481475946")
   row = cursor.fetchone()
   devs_cards += int(row[0] if row else 0)
   results += f"\nВсего карточек существует: {total_cards - devs_cards}\n\n"
   await message.answer(results) 
  leaderboard_selection_users.discard(user_id)


@dp.message(Command("start")) # КОМАНДА ДЛЯ СТАРТА v0.1+
async def start_handler(message: types.Message):
 text = (
 "👋 Привет, ты попал в Joe Biden Cards.\n"
 "Здесь ты можешь выбивать разные карточки с Джо Байденом, коллекционировать их и просто проводить время\n\n"
 "Бот находится в начальной разработке, поэтому в нем могут присутствовать некоторые баги.\n\n"
 "Создано @by_when ; весь материал в боте используется исключительно в шуточных целях\n\n"
 "Чтоб начать пользоваться ботом используйте команду /card\n\n"
 "Актуальная версия: v0.1.1.3 [02.06.2026]"
 )
 await message.answer(text)

@dp.message(Command("menu")) # КОМАНДА МЕНЮ v0.1+
async def handle_answer(message: types.Message):
 nickname = message.from_user.full_name
 user_id = message.from_user.id
 cursor.execute("SELECT total_cards, last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 total_cards = row[0] if row else 0
 cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
 info = cursor.fetchone()
 xp = info[0] if info else 0
 cursor.execute("SELECT unlocked_cards FROM users  WHERE user_id = ?", (user_id,))
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

@dp.message(Command("card")) # КОМАНДА ДЛЯ ОТКРЫТИЯ КАРТЫ v0.1+
async def handle_answer(message: types.Message):
 user_id = message.from_user.id
 cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)", (user_id, message.from_user.full_name))
 db.commit() 
 cursor.execute(
    "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
    (user_id, message.from_user.full_name or "Anon")
 )
 cursor.execute(
    "UPDATE users SET full_name = ? WHERE user_id = ?",
    (message.from_user.full_name or "Anon", user_id)
 )
 db.commit()
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 last_opening_time = cursor.fetchone()[0] 
 waiting_users.add(user_id)
 text = (
   "<b>🃏 Обычный набор карт с Джо Байденом</b>\n\n"
   "• Шансы:\n\n"
   "???\n"
   "Водолаз Джо Байден - 5%\n"
   "Сикс Севен Джо Байден - 10%\n"
   "Праздничный Джо Байден - 30%\n"
   "Обычный Джо Байден - 55%\n\n"
   "Напишите y чтоб открыть или n чтоб отменить."
    )
 await message.answer(text)


@dp.message() # ПРОВЕРКА ПОДТВЕРЖДЕНИЯ ОТКРЫТИЯ КАРТЫ v0.1+
async def handle_all_messages(message: types.Message):
 nickname = message.from_user.full_name
 user_id = message.from_user.id
 if user_id in waiting_users:
  if not message.text:
   return
  answer = message.text.lower()
  if answer in ["ｙ", "y", "у"]:
   cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
   count_before = cursor.fetchone()[0]
   cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
   row = cursor.fetchone()
   last_opening_time = row[0] if row else 0
   current_left = CD - int(time.time() - last_opening_time)
   if current_left <= 0:
    chance = random.randint(1, 100)
    devs_cards = 0
    if chance <= 5: # 1, 2, 3, 4, 5
     xp_to_add = 40
     add_card(user_id, 1, xp_to_add, nickname)
     cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (7020510390, 7481475946) AND card_id = 1")
     row = cursor.fetchone()
     devs_cards = row[0] if row and row[0] is not None else 0
     if get_user_card_count(user_id, 1) == 1:
      cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
      db.commit()
     photo = FSInputFile(os.path.join(base_dir, "images", "ВодолазДжоБайден.jpg"))
     text = (
     "Вам выпал..\n"
     "- <b>Водолаз Джо Байден - 5%!</b>\n"
     "+40 XP\n\n"
     "<blockquote>— нырнул в разговор и не вынырнул. Говорит много, звучит умно, смысл утонул где-то на глубине.</blockquote>\n\n"
     f"Количество: {get_user_card_count(message.from_user.id, 1)}\n"
     f"Всего в мире: {get_world_card_count(1) - devs_cards}\n\n"
     "Для просмотра вашей обновленной коллекции нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
     count_after = cursor.fetchone()[0]
     if get_world_card_count(1) == 1:
      text = "Вы первыми в мире открыли <b>Водолаза Джо Байдена</b>!\n+40 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
      await message.answer(text)
      xp_to_add = 40
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
     if count_after == 4 and count_before == 3:
      text = "Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал Водолаз Джо Байден.\n +125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
      xp_to_add = 125
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
      await message.answer(text)
     waiting_users.remove(user_id)
    elif chance <= 15: # 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
     xp_to_add = 15
     add_card(user_id, 2, xp_to_add, nickname)
     cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (7020510390, 7481475946) AND card_id = 2")
     row = cursor.fetchone()
     devs_cards = row[0] if row and row[0] is not None else 0
     if get_user_card_count(user_id, 2) == 1:
      cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
      db.commit()
     photo = FSInputFile(os.path.join(base_dir, "images", "67ДжоБайден.jpg"))
     text = (
     "Вам выпал..\n" \
     "- <b>Сикс Севен Джо Байден - 10%!</b>\n"
     "+15 XP\n\n"
     "<blockquote>— 67 67 67. Никто не знает что это значит, но если не уважаешь 67 — ты вне цивилизации.</blockquote>\n\n"
     f"Количество: {get_user_card_count(message.from_user.id, 2)}\n"
     f"Всего в мире: {get_world_card_count(2) - devs_cards}\n\n"
     "Для просмотра вашей обновленной коллекции нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
     count_after = cursor.fetchone()[0]
     if get_world_card_count(2) == 1:
      text = "Вы первыми в мире открыли <b>Сикс Севен Джо Байдена</b>!\n+15 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
      await message.answer(text)
      xp_to_add = 15
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
     if count_after == 4 and count_before == 3:
      text = "Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал Сикс Севен Джо Байден.\n +125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
      xp_to_add = 125
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
      await message.answer(text)
     waiting_users.remove(user_id)
    elif chance <= 45: # 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45
     xp_to_add = 6
     add_card(user_id, 3, xp_to_add, nickname)
     cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (7020510390, 7481475946) AND card_id = 3")
     row = cursor.fetchone()
     devs_cards = row[0] if row and row[0] is not None else 0
     if get_user_card_count(user_id, 3) == 1:
      cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
      db.commit()
     photo = FSInputFile(os.path.join(base_dir, "images", "ПраздничныйДжоБайден.jpg"))
     text = (
     "Вам выпал..\n"
     "- <b>Праздничный Джо Байден - 30%!</b>\n"
     "+6 XP\n\n"
     "<blockquote>— это когда торт уже не торт, а государственное событие.</blockquote>\n\n"
     f"Количество: {get_user_card_count(message.from_user.id, 3)}\n"
     f"Всего в мире: {get_world_card_count(3) - devs_cards}\n\n"
     "Для просмотра вашей обновленной коллекции нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
     count_after = cursor.fetchone()[0]
     if get_world_card_count(3) == 1:
      text = "Вы первыми в мире открыли <b>Праздничного Джо Байдена</b>!\n+6 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
      await message.answer(text)
      xp_to_add = 6
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
     if count_after == 4 and count_before == 3:
      text = "Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал Праздничный Джо Байден.\n +125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
      xp_to_add = 125
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
      await message.answer(text)
     waiting_users.remove(user_id)
    else: # 55-100
     xp_to_add = 2
     add_card(user_id, 4, xp_to_add, nickname)
     cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (7020510390, 7481475946) AND card_id = 4")
     row = cursor.fetchone()
     devs_cards = row[0] if row and row[0] is not None else 0
     if get_user_card_count(user_id, 4) == 1:
      cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
      db.commit()
     photo = FSInputFile(os.path.join(base_dir, "images", "ОбычныйДжоБайден.jpg"))
     text = (
      "Вам выпал..\n"
      "- <b>Обычный Джо Байден - 55%!</b>\n"
      "+2 XP\n\n"
      "<blockquote>— literally дефолт скин. Ничего не делает, просто стоит, но почему-то уже происходит лор. Если выпал — значит игра сказала “ну держи хоть что-то”.</blockquote>\n\n"
      f"Количество: {get_user_card_count(message.from_user.id, 4)}\n"
      f"Всего в мире: {get_world_card_count(4) - devs_cards}\n\n"
      "Для просмотра вашей обновленной коллекции нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
     count_after = cursor.fetchone()[0]
     if get_world_card_count(4) == 1:
      text = "Вы первыми в мире открыли <b>Обычного Джо Байдена</b>!\n+2 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
      await message.answer(text)
      xp_to_add = 2
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
     if count_after == 4 and count_before == 3:
      text = "Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал Обычный Джо Байден.\n +125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard ."
      xp_to_add = 125
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
      db.commit()
      await message.answer(text)
    waiting_users.remove(user_id)
   else: 
    minutes = current_left // 60
    seconds = current_left % 60
    text = f"⏱️ Сейчас данный набор находится в КД. Вы сможете открыть его через <b> {minutes}m {seconds}s</b>."
    await message.answer(text)
    waiting_users.discard(user_id)
  elif answer in ["n", "ん", "н"]:
   text = "Открытие отменено."
   await message.answer(text)
   waiting_users.discard(user_id)
   return
  else:
   text = "Открытие отменено."
   await message.answer(text)
   waiting_users.discard(user_id)
   return
   

async def main():
 asyncio.create_task(reminder())
 await dp.start_polling(bot)

if __name__ == "__main__":
 try:
  asyncio.run(main())
 except KeyboardInterrupt:
  print("Бот выключен")
