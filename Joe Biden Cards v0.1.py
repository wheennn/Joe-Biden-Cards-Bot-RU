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
CD = 1800

base_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(base_dir, "data.env"))

token = os.getenv("BOT_TOKEN")
db_name = os.getenv("DATABASE_v0.1").strip()
dev_id = os.getenv("DEV_ID")

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

db = sqlite3.connect(os.path.join(base_dir, db_name))
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
 user_id INTEGER PRIMARY KEY,
 username TEXT,
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
 total_count INTEGER NOT NULL DEFAULT 0
)
""")
db.commit()
def add_card(user_id: int, card_id: int):
 cursor.execute("""
  INSERT INTO user_cards (user_id, card_id, count)
  VALUES (?, ?, 1)
  ON CONFLICT(user_id, card_id)
  DO UPDATE SET count = count + 1
  """, (user_id, card_id))
 cursor.execute("""
  INSERT INTO card_stats (card_id, total_count)
  VALUES (?, 1)
  ON CONFLICT(card_id)
  DO UPDATE SET total_count = total_count + 1
  """, (card_id,))
 cursor.execute("""
  UPDATE users
  SET total_cards = total_cards + 1, last_card_time = ?
  WHERE user_id = ?
  """, (time.time(), user_id,))
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


@dp.message(Command("leaderboard"))
async def show_leaderboard(message: types.Message):
 cursor.execute("SELECT username, total_cards FROM users ORDER BY total_cards DESC LIMIT 10")
 users = cursor.fetchall()
 results = "<b>🏆 ЛИДЕРБОРД</b>\n\n"
 for i, user in enumerate(users, 1):
  results += f"{i}. {user[0]} - {user[1]} карт\n"
 cursor.execute("SELECT SUM(total_count) FROM card_stats")
 row = cursor.fetchone()
 results += f"\n\nВсего карточек существует: {row[0] if row and row[0] else 0}"
 await message.answer(results) 

@dp.message(Command("start"))
async def start_handler(message: types.Message):
 text = "👋 Привет, ты попал в Joe Biden Cards.\nЗдесь ты можешь выбивать разные карточки с Джо Байденом, коллекционировать их и просто проводить время\n\nБот находится в начальной разработке, поэтому в нем могут присутствовать некоторые баги.\n\nСоздано @by_when ; весь материал в боте используется исключительно в шуточных целях\n\nЧтоб начать пользоваться ботом используйте команду /card"
 await message.answer(text)

@dp.message(Command("menu"))
async def handle_answer(message: types.Message):
 nickname = message.from_user.full_name
 user_id = message.from_user.id
 cursor.execute("SELECT total_cards, last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 text = (
 "<b>🏠 МЕНЮ</b>\n" 
 f"Ник: {nickname}\n\n"
 f"Водолаз Джо Байден - x{get_user_card_count(user_id, 1)}\n"
 f"Праздничный Джо Байден - x{get_user_card_count(user_id, 2)}\n"
 f"Сиксевен Джо Байден - x{get_user_card_count(user_id, 3)}\n"
 f"Обычный Джо Байден - x{get_user_card_count(user_id, 4)}\n"
 f"В общем: {row[0] if row else 0}\n\n"
 "Чтоб открыть карточку нажмите /card"
 )
 await message.answer(text)

@dp.message(Command("card"))
async def handle_answer(message: types.Message):
 user_id = message.from_user.id
 waiting_users.add(user_id)
 username = message.from_user.username or "Anon"
 cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
 db.commit() 
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 last_opening_time = cursor.fetchone()[0] 
 current_time = time.time()
 text = (
   "<b>🃏 Обычный набор карт с Джо Байденом</b>\n\n"
   "• Шансы:\n\n"
   "Водолаз Джо Байден - 3%\n"
   "Праздничный Джо Байден - 7%\n"
   "Сиксевен Джо Байден - 20%\n"
   "Обычный Джо Байден - 70%\n\n"
   "Напишите Y чтоб открыть или N чтоб отменить."
    )
 await message.answer(text)


@dp.message()
async def handle_all_messages(message: types.Message):
 user_id = message.from_user.id
 if user_id in waiting_users:
  if not message.text:
   return
  answer = message.text.lower()
  if answer == "y":
   cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
   row = cursor.fetchone()
   last_opening_time = row[0] if row else 0
   current_left = CD - int(time.time() - last_opening_time)
   if current_left <= 0:
    chance = random.randint(1, 100)
    if chance <= 3:
     add_card(message.from_user.id, 1)
     photo = FSInputFile(os.path.join(base_dir, "ВодолазДжоБайден.jpg"))
     text = (
     "Вам выпал..\n"
     "- <b>Водолаз Джо Байден - 3%!</b>\n\n"
     "Создано: 19.04.26\n"
     "Добавлено в бота: 22.04.26\n"
     f"Количество: {get_user_card_count(message.from_user.id, 1)}\n"
     f"Всего в мире: {get_world_card_count(1)}\n\n"
     "Для просмотра вашей обновленной коллекции нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     new_time = time.time()
     waiting_users.remove(user_id)
    elif chance <= 10:
     add_card(message.from_user.id, 2)
     photo = FSInputFile(os.path.join(base_dir, "ПраздничныйДжоБайден.jpg"))
     text = (
     "Вам выпал..\n" \
     "- <b>Праздничный Джо Байден - 7%!</b>\n\n"
     "Создано: 17.04.26\n"
     "Добавлено в бота: 22.04.26\n"
     f"Количество: {get_user_card_count(message.from_user.id, 2)}\n"
     f"Всего в мире: {get_world_card_count(2)}\n\n"
     "Для просмотра вашей обновленной коллекции нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     new_time = time.time()
     waiting_users.remove(user_id)
    elif chance <= 30:
     add_card(message.from_user.id, 3)
     photo = FSInputFile(os.path.join(base_dir, "67ДжоБайден.jpg"))
     text = (
     "Вам выпал..\n"
     "- <b>Сиксевен Джо Байден - 20%!</b>\n\n"
     "Создано: 14.03.26\n"
     "Добавлено в бота: 22.04.26\n"
     f"Количество: {get_user_card_count(message.from_user.id, 3)}\n"
     f"Всего в мире: {get_world_card_count(3)}\n\n"
     "Чтоб просмотреть твою обновленную коллекцию нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     new_time = time.time()
     waiting_users.remove(user_id)
    else:
     add_card(message.from_user.id, 4)
     photo = FSInputFile(os.path.join(base_dir, "ОбычныйДжоБайден.jpg"))
     text = (
      "Вам выпал..\n"
      "- <b>Обычный Джо Байден - 70%!</b>\n\n"
      "Создано: 13.03.26\n"
      "Добавлено в бота: 22.04.26\n"
      f"Количество: {get_user_card_count(message.from_user.id, 4)}\n"
      f"Всего в мире: {get_world_card_count(4)}\n\n"
      "Чтоб просмотреть твою обновленную коллекцию нажмите /menu"
     )
     await message.answer_photo(photo=photo, caption=text)
     new_time = time.time()
     waiting_users.remove(user_id)
   else: 
    minutes = current_left // 60
    seconds = current_left % 60
    text = f"⏱️ Сейчас данный набор находится в КД. Вы сможете открыть его через <b> {minutes}m {seconds}s</b>."
    await message.answer(text)
  elif answer == "n":
   waiting_users.remove(user_id)
   text = "Открытие отменено."
   await message.answer(text)
   return
   

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))