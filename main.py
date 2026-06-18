# Joe Biden Cards — v0.1.3
# Est. 23.04.2026
# by wheen

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import html_decoration as hd
from aiogram.types import FSInputFile, message, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from html import escape
from datetime import datetime
import inspect
import os
import random
import sqlite3
import time
import asyncio

waiting_users = set()
fpack_CD = 900
spack_CD = 1800

base_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(base_dir, "data.env"))

token = os.getenv("BOT_TOKEN")
db_name = os.getenv("DATABASE").strip()
users_env = os.getenv("USERS_WITH_FULL_COLLECTION")
full_coll_users = [int(x) for x in users_env.split(",")]
dev_id = int(os.getenv("DEV_ID"))
dev2_id = int(os.getenv("DEV2_ID"))
dev_mini_id = int(os.getenv("DEV_MINI_ID"))
t1_season0 = int(os.getenv("TOP1_SEASON0"))
comp_user1 = int(os.getenv("COMPENSATION1"))
comp_user2 = int(os.getenv("COMPENSATION2"))
comp_user3 = int(os.getenv("COMPENSATION3"))
comp_user4 = int(os.getenv("COMPENSATION4"))
comp_user5 = int(os.getenv("COMPENSATION5"))
comp_user6 = int(os.getenv("COMPENSATION6"))

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

card_names = {
 1: "Водолаз Джо Байден",
 2: "Сикс Севен Джо Байден",
 3: "Праздничный Джо Байден",
 4: "Обычный Джо Байден",
 5: "Сигма Джо Байден",
 6: "Пожизненный Водолаз Джо Байден",
 7: "Джо Байден в Разрешении 9:38",
 8: "Джо Байден в Разрешении 38:9",
 9: "Джо Байден.exe",
 10: "Троллфейс Джо Байден"
}
card_descriptions = {
 1: "Потно пахающий водолаз, выполняющий всю грязную работу. Одет в неплохое оборудование, но не сравнится с Пожизненным Водолазом. Как можно заметить, его труд был оценен поэтому он стал довольно редкой картой.",
 2: "Стереотипный ребенок, смеющийся с молодежного «67». Надел пропеллерную кепку, чтобы его не сдул ветер, и показывает свой мем. Лучшая версия нас.",
 3: "Приодетый в колпак, готов праздновать свой день рождения в любой момент, организовывая специальное государственное событие.",
 4: "Ничем не отличающийся от других Джо Байден, является простым человеком, а не ярким образом.",
 5: "В крутых и стильных очках, не боится толпы и ее мнения, ведь как раз таки он — местный авторитет с миллионами фанаток по всему миру.",
 6: "Более опытный и глубоководный водолаз. Оснащен профессиональным оборудованием и готов бороться за трон Joe Biden Cards. Эксклюзивен за топ 1 мира в течение сезонов.",
 7: "Жертва жесткого сжатия и растяжения, застрявшая в непривычном для людей разрешении. Настолько узкий и вытянутый, как кое-что другое, что может протиснуться сквозь текстуры игры и следить за балансом.",
 8: "Абсолютная противоположность его дружка, раздувшаяся до невероятных горизонталей. Стал настолько жирным, что теперь в одиночку занимает половину экрана и блокирует подводный проход для водолазов.",
 9: "Настоящий псевдо-хакер, которого нужно бояться в случае обнаружения вирусов. Попытался наложить на себя глитч-эффекты, чтобы быть более ужасающим, так ещё и PNG-шки ошибок достал сразу.",
 10: "Очень могущественный и непобедимый Джо Байден. Натапал хомячка в 2024 году и ушёл на пенсию, ведь заработал на три поколения вперёд. Одет в стильную маску троллфейса, чтобы демонстрировать всем, что с ним лучше не шутить."
}
card_drop_diapazones = {
 11: 0,
 10: 5,
 9: 15,
 8: 45,
 7: 100,
 5: 1,
 1: 5,
 2: 15,
 3: 45,
 4: 100,
}
card_chances = {
 1: 4,
 2: 10,
 3: 30,
 4: 55,
 5: 1,
 6: 0,
 7: 55,
 8: 30,
 9: 10,
 10: 5,
 11: 0
}
card_xps = {
 1: 40,
 2: 15,
 3: 6,
 4: 2,
 5: 100,
 6: 0,
 7: 4,
 8: 10,
 9: 24,
 10: 60,
 11: 0
}
first_unlocked_date = {
 1: "26.04",
 2: "23.04",
 3: "23.04",
 4: "26.04",
 5: "07.06",
 6: "08.06",
 7: "16.06",
 8: "16.06",
 9: "16.06",
 10: "???"
}
first_unlocked_rewards = {
 1: 4,
 2: 3,
 3: 2,
 4: 1,
 5: 5,
 6: 0,
 7: 1,
 8: 2,
 9: 3,
 10: 4,
 11: 5
}
global_rewards_indicators = {
 "total_cards_st1": 100,
 "total_cards_st2": 300,
 "total_cards_st3": 500,
 "sigma_cards_st1": 5,
 "sigma_cards_st2": 10,
 "diver_cards_st1": 10,
 "diver_cards_st2": 25,
 "diver_cards_st3": 50,
 "sixseven_cards_st1": 25,
 "sixseven_cards_st2": 50,
 "sixseven_cards_st3": 100
}
global_rewards = {
 "total_cards_st1": 50,
 "total_cards_st2": 150,
 "total_cards_st3": 250,
 "sigma_cards_st1": 200,
 "sigma_cards_st2": 400,
 "diver_cards_st1": 100,
 "diver_cards_st2": 250,
 "diver_cards_st3": 500,
 "sixseven_cards_st1": 50,
 "sixseven_cards_st2": 100,
 "sixseven_cards_st3": 200
}
global_rewards_names = {
 "total_cards_st1": "Общий Тираж — Уровень 1",
 "total_cards_st2": "Общий Тираж — Уровень 2",
 "total_cards_st3": "Общий Тираж — Уровень 3",
 "sigma_cards_st1": "Тираж Сигм — Уровень 1",
 "sigma_cards_st2": "Тираж Сигм — Уровень 2",
 "diver_cards_st1": "Тираж Водолазов — Уровень 1",
 "diver_cards_st2": "Тираж Водолазов — Уровень 2",
 "diver_cards_st3": "Тираж Водолазов — Уровень 3",
 "sixseven_cards_st1": "Тираж Сикс Севенов — Уровень 1",
 "sixseven_cards_st2": "Тираж Сикс Севенов — Уровень 2",
 "sixseven_cards_st3": "Тираж Сикс Севенов — Уровень 3"
}

leaderboard_mode_selection = InlineKeyboardBuilder() # Выбор фильтра лидерборда
leaderboard_mode_selection.button(text="Сезонный лидерборд", callback_data="season_leaderboard")
leaderboard_mode_selection.button(text="Лидерборд достижений", callback_data="records_leaderboard")
leaderboard_mode_selection.button(text="Глобальные достижения", callback_data="global_achievements")
leaderboard_mode_selection.adjust(1)

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
cursor.execute("""
CREATE TABLE IF NOT EXISTS reminder_spam (
 user_id INTEGER PRIMARY KEY,
 reminder_cd INTEGER DEFAULT 0,
 reminder_2 INTEGER DEFAULT 0,
 reminder_8 INTEGER DEFAULT 0,
 reminder_24 INTEGER DEFAULT 0
)
""")
db.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS season_info (
 current_season INTEGER DEFAULT 1,
 rewards TEXT,
 winner_s0 TEXT,
 winner_s1 TEXT
)
""")
db.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS global_rewards (
 total_cards_st1 INTEGER DEFAULT 1,
 total_cards_st2 INTEGER DEFAULT 0,
 total_cards_st3 INTEGER DEFAULT 0,
 sigma_cards_st1 INTEGER DEFAULT 0,
 sigma_cards_st2 INTEGER DEFAULT 0,
 diver_cards_st1 INTGER DEFAULT 1,
 diver_cards_st2 INTEGER DEFAULT 0,
 diver_cards_st3 INTEGER DEFAULT 0,
 sixseven_cards_st1 INTEGER DEFAULT 1,
 sixseven_cards_st2 INTEGER DEFAULT 0,
 sixseven_cards_st3 INTEGER DEFAULT 0
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
 openings_per_time INTEGER DEFAULT 1,
 showing_prefixes INTEGER DEFAULT 1,
 user_id INTEGER PRIMARY KEY
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
  cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
  row = cursor.fetchone()
  return row[0] if row else 0
def get_world_card_count(card_id: int) -> int:
 cursor.execute("SELECT total_count FROM card_stats WHERE card_id = ?", (card_id,))
 row = cursor.fetchone()
 return row[0] if row else 0
async def card_pack_opening(callback: CallbackQuery, pack_name: str, type: str):
 user_id = callback.from_user.id
 nickname = callback.from_user.full_name
 if type == "accumulations":
  cursor.execute("SELECT openings_per_time FROM settings WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  openings_per_time = row[0] if row else 0
 elif type == "cd":
  openings_per_time = 1
 for i in range(openings_per_time):
  cursor.execute("SELECT fpacks, spacks FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  if pack_name == "fpack":
   cursor.execute("SELECT fpack_unlocked_cards FROM users WHERE user_id = ?", (user_id,))
  elif pack_name == "spack":
   cursor.execute("SELECT spack_unlocked_cards FROM users WHERE user_id = ?", (user_id,))
  count_before = cursor.fetchone()[0]
  fpacks, spacks = row if row else (0, 0)
  accums = fpacks if pack_name == "fpack" else spacks
  cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  last_opening_time = row[0] if row else 0
  if type == "cd":
   if pack_name == "fpack":
    current_left = fpack_CD - int(time.time() - last_opening_time)
   else:
    current_left = spack_CD - int(time.time() - last_opening_time)
 
   if current_left > 0:
    minutes = current_left // 60
    seconds = current_left % 60
    if accums == 0:
     text = f"⏱️ Сейчас данный набор находится в КД. Вы сможете открыть его через <b>{minutes}m {seconds}s</b>."
    elif accums >= 1:
     text = f"⏱️ Сейчас данный набор находится в КД. Вы сможете открыть его через <b>{minutes}m {seconds}s</b>. Вы также можете открыть набор <b>прямо сейчас</b> потратив свои накопленные запасы."
    await callback.message.answer(text)
    await callback.answer()
    return
 
  elif type == "accumulations":
   if accums < 1:
    text = "Недостаточно наборов карт. Попробуйте позже."
    await callback.message.answer(text)
    await callback.answer()
    return
   if pack_name == "fpack":
    cursor.execute("UPDATE users SET fpacks = fpacks - 1 WHERE user_id = ?", (user_id,))
   elif pack_name == "spack":
    cursor.execute("UPDATE users SET spacks = spacks - 1 WHERE user_id = ?", (user_id,))
   db.commit()
   
  chance = random.randint(1, 100)
  if pack_name == "fpack":
   pack_identification = {1, 2, 3, 4, 5}
  elif pack_name == "spack":
   pack_identification = {7, 8, 9, 10, 11}
  for i in card_drop_diapazones.keys():
   if chance <= card_drop_diapazones.get(i) and i in pack_identification:
    cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    total_before = row[0] if row else 0
    cursor.execute("SELECT fpack_progress, spack_progress FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    fp_prog, sp_prog = row if row else (0, 0)
    xp_to_add = card_xps.get(i, 0)
    text = "Вам выпал..\n<b>"
    if pack_name == "fpack":
     if fp_prog == 100:
      xp_to_add = xp_to_add / 2
    elif pack_name == "spack":
     if sp_prog == 100:
      xp_to_add = xp_to_add / 2
    if str(xp_to_add).count(".0") == 1:
     xp_to_add = int(xp_to_add)
    add_card(user_id, i, xp_to_add, nickname)
    if get_user_card_count(user_id, i) == 1:
     text += f"[NEW] "
     if pack_name == "fpack":
      cursor.execute("UPDATE users SET fpack_unlocked_cards = fpack_unlocked_cards + 1 WHERE user_id = ?", (user_id,))
      cursor.execute("UPDATE users SET fpack_progress = fpack_progress + 20 WHERE user_id = ?", (user_id,))
     elif pack_name == "spack":
      cursor.execute("UPDATE users SET spack_unlocked_cards = spack_unlocked_cards + 1 WHERE user_id = ?", (user_id,))
      cursor.execute("UPDATE users SET spack_progress = spack_progress + 25 WHERE user_id = ?", (user_id,))
     cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
     cursor.execute("UPDATE users SET total_progress = total_progress + 11 WHERE user_id = ?", (user_id,))
     db.commit()
    if card_names.get(i, "") == "Джо Байден в Разрешении 9:38":
     actual_card_name = "ДжоБайденВРазрешении9к38.jpg"
    elif card_names.get(i, "") == "Джо Байден в Разрешении 38:9":
     actual_card_name = "ДжоБайденВРазрешении38к9.jpg"
    else:
     actual_card_name = card_names.get(i, "").replace(" ", "")
     actual_card_name += ".jpg"
    cursor.execute("SELECT SUM(count) FROM user_cards WHERE card_id = ? AND user_id NOT IN (?, ?)", (i, dev_id, dev_mini_id))
    row = cursor.fetchone()
    total = row[0] if row else 0
    cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    total_after = row[0] if row else 0
    photo = FSInputFile(os.path.join(base_dir, "images", actual_card_name))
    text += (
     f"{card_names.get(i, "")} — {card_chances.get(i, "")}%!</b>\n"
     f"+{xp_to_add} XP\n\n"
     f"<blockquote>{card_descriptions.get(i, "")}</blockquote>\n\n"
     f"Количество: {get_user_card_count(user_id, i)}\n"
     f"Всего в мире: {total}\n\n"
    )
    if get_user_card_count(user_id, i) == 1:
     text += "Вы открыли новую карту! Ваш прогресс прохождения бота был обновлён!\n\n"
    if type == "accumulations":
     text += "Для открытия ещё одного набора из запасов нажмите /card либо /menu для просмотра вашего текущего прогресса и обновлённой коллекции"
    else:
     text += "Для просмотра вашей обновлённой коллекции нажмите /menu"
    await callback.message.answer_photo(photo=photo, caption=text)
    if pack_name == "fpack":
     cursor.execute("SELECT fpack_unlocked_cards FROM users WHERE user_id = ?", (user_id,))
    elif pack_name == "spack":
     cursor.execute("SELECT spack_unlocked_cards FROM users WHERE user_id = ?", (user_id,))
    count_after = cursor.fetchone()[0]
    if total == 1:
     if first_unlocked_rewards.get(i, 0) == 1:
      mini_text = "обычный набор карт" if pack_name == "fpack" else "расширенный набор карт"
     elif first_unlocked_rewards.get(i, 0) == 5:
      mini_text = "обычных наборов карт" if pack_name == "fpack" else "расширенных наборов карт"
     else:
      mini_text = "обычных набора карт" if pack_name == "fpack" else "расширенных наборов карт"
     text = f"Вы первыми в мире открыли карту <b>{card_names.get(i, "")}</b>!\n+{first_unlocked_rewards.get(i, "")} {mini_text}\n\nВы можете просмотреть обновлённый лидерборд с вашим ником используя /leaderboard"
     await callback.message.answer(text)
     if pack_name == "fpack":
      cursor.execute("UPDATE users SET fpacks = fpacks + ? WHERE user_id = ?", (first_unlocked_rewards.get(i, 0), user_id))
     elif pack_name == "spack":
      cursor.execute("UPDATE users SET spacks = spacks + ? WHERE user_id = ?", (first_unlocked_rewards.get(i, 0), user_id))
     db.commit()
    if count_after == 5 and count_before == 4:
     if pack_name == "fpack":
      text = (
       f"Вы собрали <b>полную коллекцию Джо Байденов</b> из <b>Обычного Набора Карт</b> и завершили прохождение <b>Первой стадии</b>! Последней нужной картой стал <b>{card_names.get(i, "")}</b>. В честь этого вы получаете награду в виде <b>50 XP</b> и <b>3 расширенных набора карт</b>.\n"
       "Теперь вы разблокировали <b>Расширенный Набор Карт</b> и начали прохождение <b>Второй стадии</b>, а также с этого момента при открытии обычного набора вы будете получать в два раза меньше опыта.\n\n"
       "<b>Ваши показатели на момент достижения:</b>\n"
       f"<blockquote>Сигма Джо Байден — x{get_user_card_count(user_id, 6)}\n"
       f"Водолаз Джо Байден — x{get_user_card_count(user_id, 1)}\n"
       f"Сикс Севен Джо Байден — x{get_user_card_count(user_id, 2)}\n"
       f"Праздничный Джо Байден — x{get_user_card_count(user_id, 3)}\n"
       f"Обычный Джо Байден — x{get_user_card_count(user_id, 4)}\n"
       f"В сумме: {sum(get_user_card_count(user_id, cid) for cid in (1, 2, 3, 4, 5))}</blockquote>\n"
       "Вы можете поделиться или померяться данными счетчиками с вашими друзьями, пересылая это сообщение.\n\n"
       "Для открытия и просмотра нового набора нажмите /card, или /menu для просмотра вашей уникальной коллекции"
      )
      xp_to_add = 50
      spacks_to_add = 3
      cursor.execute("UPDATE users SET xp = xp + 50 WHERE user_id = ?", (user_id,))
      cursor.execute("UPDATE users SET spacks = spacks + 3 WHERE user_id = ?", (user_id,))
      cursor.execute("UPDATE users SET pack_stage = 2 WHERE user_id = ?", (user_id,))
      db.commit()
      await callback.message.answer(text)
    if total_before == 8 and total_after == 9: 
     text = (
      f"<b>{escape(nickname)}</b>, вы собрали <b>полную коллекцию Джо Байденов</b> из <b>9 карт</b>! Теперь вы официально прошли <b>Joe Biden Cards</b> и ваш общий достигнутый <b>прогресс равен 100%</b>!\n\n"
      "Поскольку бот активно обновляется и выходят новые карты, с целью баланса мы не можем выдать вам какую-либо награду, но знайте, <b>ваше имя</b> уже записано в <b>истории проекта!</b>\n\n"
      "Продолжайте играть, дожидаться новых обновлений и соревноваться за топ-1 мира, ведь теперь перед вами полностью открыта сфера соревнований за эксклюзивные награды!"
     )
     cursor.execute("UPDATE users SET total_progress = 100 WHERE user_id = ?", (user_id,))
     db.commit()
     await callback.message.answer(text)
    elif total_before == 9 and total_after == 10:
     text = (
      f"<b>{escape(nickname)}</b>, вы собрали <b>абсолютно полную коллекцию Джо Байденов</b> из <b>10 карт</b>! Теперь вы официально прошли <b>Joe Biden Cards и ваш общий достигнутый <b>прогресс равен 100%</b>!\n\n"
      "Поскольку бот активно обновляется и выходят новые карты, с целью баланса мы не можем выдать вам какую-либо награду, но знайте, <b>ваше имя</b> уже записано в <b>истории проекта!</b>\n\n"
      "Продолжайте играть, дожидаться новых обновлений и соревноваться за топ-1 мира!"
     )
     await callback.message.answer(text)
    if type == "accumulations":
     cursor.execute("UPDATE users SET last_card_time = ? WHERE user_id = ?", (last_opening_time, user_id))
     db.commit()
    await callback.answer()
    break

cursor.execute("INSERT OR IGNORE INTO season_info (current_season, winner_s0, winner_s1) VALUES (1, NULL, NULL)")
db.commit()

cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (comp_user4,))
row = cursor.fetchone()[0]
if row == 1:
 cursor.execute("UPDATE users SET pack_stage = 2 WHERE user_id = ?", (comp_user4,))
 cursor.execute("UPDATE users SET total_progress = 50 WHERE user_id = ?", (comp_user4,))
 db.commit()

async def global_rewards_dispatcher(): # ДИСПЕТЧЕР ОБЩИХ ДОСТИЖЕНИЙ И НАГРАД v0.1.3+
 while True:
  cursor.execute("INSERT OR IGNORE INTO global_rewards (id) VALUES (1)")
  db.commit()
  cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
  row = cursor.fetchone()
  total_count = row[0] if row else 0
  xs = [5, 1, 2]
  for x in xs:
   cursor.execute("SELECT SUM(count) FROM user_cards WHERE card_id = ? AND user_id NOT IN (?, ?)", (x, dev_id, dev_mini_id))
   row = cursor.fetchone()
   if x == 5:
    sigma_count = row[0] if row else 0
   elif x == 1:
    diver_count = row[0] if row else 0
   elif x == 2:
    sixseven_count = row[0] if row else 0
  for i in range(1, 12):
   if i == 1:
    what_to_find = "total_cards_st1"
    goal_name = "Общий Тираж — Уровень 1"
    count = total_count
   elif i == 2:
    what_to_find = "total_cards_st2"
    goal_name = "Общий Тираж — Уровень 2"
    count = total_count
   elif i == 3:
    what_to_find = "total_cards_st3"
    goal_name = "Общий Тираж — Уровень 3"
    count = total_count
   elif i == 4:
    what_to_find = "sigma_cards_st1"
    goal_name = "Тираж Сигм — Уровень 1"
    count = sigma_count
   elif i == 5:
    what_to_find = "sigma_cards_st2"
    goal_name = "Тираж Сигм — Уровень 2"
    count = sigma_count
   elif i == 6:
    what_to_find = "diver_cards_st1"
    goal_name = "Тираж Водолазов — Уровень 1"
    count = diver_count
   elif i == 7:
    what_to_find = "diver_cards_st2"
    goal_name = "Тираж Водолазов — Уровень 2"
    count = diver_count
   elif i == 8:
    what_to_find = "diver_cards_st3"
    goal_name = "Тираж Водолазов — Уровень 3"
    count = diver_count
   elif i == 9:
    what_to_find = "sixseven_cards_st1"
    goal_name = "Тираж Сикс Севенов — Уровень 1"
    count = sixseven_count
   elif i == 10:
    what_to_find = "sixseven_cards_st2"
    goal_name = "Тираж Сикс Севенов — Уровень 2"
    count = sixseven_count
   elif i == 11:
    what_to_find = "sixseven_cards_st3"
    goal_name = "Тираж Сикс Севенов — Уровень 3"
    count = sixseven_count
   cursor.execute(f"SELECT {what_to_find} FROM global_rewards WHERE id = 1")
   row = cursor.fetchone()
   achieved = row[0] if row else 0
   if count is not None and count >= global_rewards_indicators.get(what_to_find, 0) and achieved == 0:
    cursor.execute(f"UPDATE global_rewards SET {what_to_find} = 1 WHERE {what_to_find} = 0 AND id = 1")
    if cursor.rowcount == 0:
     continue
    db.commit()
    cursor.execute("SELECT user_id FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
    user_rows = cursor.fetchall()
    for row_user in user_rows:
     user_id = row_user[0]
     cursor.execute("SELECT full_name FROM users WHERE user_id = ?", (user_id,))
     row = cursor.fetchone()
     nickname = row[0] if row else 0
     if i in (1, 2, 3):
      cursor.execute("SELECT total_cards FROM users WHERE user_id = ?", (user_id,))
      row = cursor.fetchone()
      player_count = row[0] if row else 0
     else:
      if i in (4, 5):
       cursor.execute("SELECT count FROM user_cards WHERE card_id = 5 AND user_id = ?", (user_id,))
      elif i in (6, 7, 8):
       cursor.execute("SELECT count FROM user_cards WHERE card_id = 1 AND user_id = ?", (user_id,))
      elif i in (9, 10, 11):
       cursor.execute("SELECT count FROM user_cards WHERE card_id = 2 AND user_id = ?", (user_id,))
      info = cursor.fetchone()
      if info:
       player_count = info[0] if info else 0
      else:
       player_count = 0
     try:
      goal_percentage = min(1, (player_count / count))
     except (ZeroDivisionError, TypeError):
      goal_percentage = 0
     earned_xp = min(global_rewards.get(what_to_find), int(global_rewards.get(what_to_find) * goal_percentage))
     text = (
      f"{escape(nickname)}, в честь достижения цели <b>{goal_name}</b> Вы получили <b>{earned_xp} XP</b>, достигнув <b>{int(goal_percentage * 100)}%</b> всей цели с получёнными <b>{player_count} требованными картами!</b>"
     )
     cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (earned_xp, user_id))
     try:
      await bot.send_message(chat_id=user_id, text=text)
     except TelegramAPIError as e:
      print(f"Не удалось отправить награду пользователю {user_id}: {e}")
     await asyncio.sleep(0.1)
    db.commit()
  await asyncio.sleep(5)

async def season_dispatcher(): # ДИСПЕТЧЕР СЕЗОНОВ v0.1.2+
 global season_start, season_end, season_desc, season_duration
 while True:
  cursor.execute("SELECT current_season FROM season_info")
  row = cursor.fetchone()
  season = row[0] if row else 0
  if 1777203780 <= int(time.time()) <= 1780912800 and season == 0: # ДОСЕЗОННЫЙ ПЕРИОД
   season_start = 1777203780
   season_end = 1780912800
   season_desc = "Затишье перед бурей — попытайтесь достигнуть топ 1 мира чтобы получить эксклюзивную карту <b>Пожизненного Водолаза Джо Байдена</b> и забронировать место в разделе архивированных достижений списка лидеров, прежде чем начнётся полноценная система сезонов!"
   season_duration = (season_end - season_start) // 86400
  else: # СЕЗОНЫ 1+
   season_start = 1779703200 + (1209600 * season)
   season_end = 1780912800 + (1209600  * season)
   season_desc = "Открывайте наборы карточек и получайте XP чтобы побороться за топ 1 мира и эксклюзивного <b>Пожизненного Водолаза Джо Байдена!</b>"
   season_duration = (season_end - season_start) // 86400
  if (season_end - int(time.time())) in range(86398, 86402):
   cursor.execute("SELECT user_id FROM users")
   users = cursor.fetchall()
   for user in users:
    try:
     text = "🛍 Остался 1 день до окончания сезона, поэтому <b>временный маркет возвращается</b>!\n\nИспользуя команду /market вы можете просмотреть текущие акции и закупиться перед началом следующего сезона."
     await bot.send_message(chat_id=user[0], text=text)
     await asyncio.sleep(0.1)
    except Exception as e:
     print(f"Не удалось отправить уведомление для {user[0]}: {e}")
   await asyncio.sleep(6)
  if int(time.time()) in range(season_end - 2, season_end + 2):
   cursor.execute("SELECT full_name, user_id, xp FROM users WHERE user_id NOT IN (?, ?) ORDER BY xp DESC LIMIT 1", (dev_id, dev_mini_id)) # ВЫДАЧА НАГРАД ЗА ТОП 1 МИРА
   user = cursor.fetchone()
   if user:
    cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user[1],))
    count_before = cursor.fetchone()[0]
    cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user[1],))
    prev_time = cursor.fetchone()[0]
    cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (user[1],))
    pack_stage = cursor.fetchone()[0]
    if pack_stage == 1:
     pack_type = "Обычных Наборов Карт"
     cursor.execute("UPDATE users SET fpacks = fpacks + 5 WHERE user_id = ?", (user[1],))
    elif pack_stage == 2:
     pack_type = "Расширенных Наборов Карт"
     cursor.execute("UPDATE users SET spacks = spacks + 5 WHERE user_id = ?", (user[1],))
    db.commit()
    text = f"{user[0]}, за {season_duration} дней вы смогли набрать {user[2]} XP, заняв при этом топ 1 мира! В честь этого вы получили эксклюзивного <b>x1 Пожизненного Водолаза Джо Байдена</b> и <b>x5 {pack_type}</b>.\n\nТакже теперь вы появились в разделе архивированных достижений списка лидеров!\n\n"
    await bot.send_message(chat_id=user[1], text=text)
    add_card(user[1], 6, 0, user[0]) # ВЫПАДЕНИЕ ПОЖИЗНЕННОГО ВОДОЛАЗА
    cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (?, ?)", (dev_id, dev_mini_id))
    row = cursor.fetchone()
    if row:
     devs_cards = row[0] if row and row[0] is not None else 0
     if get_user_card_count(user[1], 6) == 1:
      cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user[1],))
      db.commit()
     photo = FSInputFile(os.path.join(base_dir, "images", "ПожизненныйВодолазДжоБайден.jpg"))
     text = (
      "Вам выпал..\n"
      "- <b>Пожизненный Джо Байден — Эксклюзивный!</b>\n"
      "+0 XP\n\n"
      f"<blockquote>{card_descriptions.get(6)}</blockquote>\n\n"
      f"Количество: {get_user_card_count(user[1], 6) - devs_cards}\n"
      f"Всего в мире: {get_world_card_count(6) - devs_cards}\n\n"
      "Для просмотра вашей обновлённой коллекции нажмите /menu"
     )
     await bot.send_photo(chat_id=user[1], photo=photo, caption=text)
     cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user[1],))
     count_after = cursor.fetchone()[0]
     cursor.execute("UPDATE users SET last_card_time = ? WHERE user_id = ?", (prev_time, user[1]))
     db.commit()
     cursor.execute("UPDATE season_info SET winner_s1 = ?", (user[0],))
     db.commit()
     if count_after == 10 and count_before == 9:
      text = "Вы собрали абсолютно полную коллекцию Джо Байденов, включая эксклюзивы!\nПоследней нужной картой стал <b>Пожизненный Водолаз Джо Байден</b>.\n\nВы можете просмотреть обновлённый лидерборд с вашим ником используя /leaderboard."
      await bot.send_message(chat_id=user[1], text=text)
   cursor.execute("SELECT full_name, user_id, xp, pack_stage FROM users WHERE user_id NOT IN (?, ?) ORDER BY xp DESC LIMIT 1 OFFSET 1", (dev_id, dev_mini_id)) # ВЫДАЧА НАГРАДЫ ТОП 2 МИРА
   row = cursor.fetchone()
   if row:
    if row[3] == 1:
     pack_type = "Обычных Наборов Карт"
     cursor.execute("UPDATE users SET fpacks = fpacks + 5 WHERE user_id = ?", (row[1],))
    elif row[3] == 2:
     pack_type = "Расширенных Наборов Карт"
     cursor.execute("UPDATE users SET spacks = spacks + 5 WHERE user_id = ?", (row[1],))
    db.commit()
    text = f"{row[0]}, за {season_duration} дней вы смогли набрать {row[2]} XP, заняв при этом топ 2 мира! В честь этого вы получили <b>x5 {pack_type}</b>."
    await bot.send_message(chat_id=row[1], text=text)
   cursor.execute("SELECT full_name, user_id, xp, pack_stage FROM users WHERE user_id NOT IN (?, ?) ORDER BY xp DESC LIMIT 1 OFFSET 2", (dev_id, dev_mini_id)) # ВЫДАЧА НАГРАДЫ ТОП 3 МИРА
   row = cursor.fetchone()
   if row:
    if row[3] == 1:
     pack_type = "Обычных Наборов Карт"
     cursor.execute("UPDATE users SET fpacks = fpacks + 3 WHERE user_id = ?", (row[1],))
    elif row[3] == 2:
     pack_type = "Расширенных Наборов Карт"
     cursor.execute("UPDATE users SET spacks = spacks + 3 WHERE user_id = ?", (row[1],))
    db.commit()
    text = f"{row[0]}, за {season_duration} дней вы смогли набрать {row[2]} XP, заняв при этом топ 3 мира! В честь этого вы получили <b>x3 {pack_type}</b>."
    await bot.send_message(chat_id=row[1], text=text)
   cursor.execute("SELECT full_name, user_id, xp, pack_stage FROM users ORDER BY xp DESC LIMIT 15 OFFSET 3") # ВЫДАЧА БОНУСА В ЧЕСТЬ НАЧАЛА СЕЗОНА
   members = cursor.fetchall()
   if members:
    for member in members:
     try:
      if member[3] == 1:
       pack_type = "Обычный Набор Карт"
      elif member[3] == 2:
       pack_type = "Расширенный Набор Карт"
      text = f"Новый сезон начался! Соревнуйтесь за топ 1 мира, чтобы получить эксклюзивного <b>Пожизненного Водолаза Джо Байдена</b>!\n\nВаш опыт был обнулён, а также вы получили <b>x1 {pack_type}</b> в честь окончания сезона."
      if member[3] == 1:
       cursor.execute("UPDATE users SET fpacks = fpacks + 1 WHERE user_id = ?", (member[1],))
      elif member[3] == 2:
       cursor.execute("UPDATE users SET spacks = spacks + 1 WHERE user_id = ?", (member[1],))
      await bot.send_message(chat_id=member[1], text=text)
      await asyncio.sleep(0.1)
     except Exception as e:
      print(f"Не удалось отправить уведомление для {member[1]}: {e}")
   cursor.execute("UPDATE users SET xp = 0")
   cursor.execute("UPDATE season_info SET current_season = current_season + 1")
   db.commit()
   await asyncio.sleep(6)
  await asyncio.sleep(1)

@dp.message(Command("all_info"))  # АДМИН КОМАНДА v0.1.1.3+
async def showing_db_info(message: types.Message):
 if message.from_user.id not in [dev_id, dev2_id, dev_mini_id]:
  text = "У вас недостаточно прав для использования команды /all_info."
  await message.answer(text)
  return
 cursor.execute("SELECT user_id FROM users")
 ids = [row[0] for row in cursor.fetchall()]
 text = "<b>ВСЯ ИНФОРМАЦИЯ</b>\n"
 for id in ids:
  cursor.execute("SELECT full_name, xp, total_cards, unlocked_cards, fpacks, last_card_time FROM users WHERE user_id = ?", (id,))
  row = cursor.fetchone()
  full_name, xp, total_cards, unlocked_cards, fpacks, last_card_time = row if row else ("Anon", 0, 0, 0, 0, 0)
  text += f"\n<b>{escape(full_name)} — {id} | {xp} XP</b>\n"
  for i in card_drop_diapazones.keys():
   card_name = card_names.get(i, f"Карта не найдена")
   if get_user_card_count(id, i) > 0:
    text += f"{card_name} — x{get_user_card_count(id, i)}\n"
  if unlocked_cards <= 5 and get_user_card_count(id, 6) == 0:
   text += f"Всего: {total_cards} карт | Открыто: {unlocked_cards}/5"
  elif unlocked_cards <= 5 and get_user_card_count(id, 6) >= 1:
   text += f"Всего: {total_cards} карт | Открыто: {unlocked_cards}/6"
  elif unlocked_cards == 6:
   text += f"Всего: {total_cards} карт | Открыто: {unlocked_cards}/6"
  text += f"\nНаборы карт: {fpacks}"
  text += f"\nПоследнее открытие: {datetime.fromtimestamp(last_card_time).date()}\n"
 cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 row = cursor.fetchone()
 total_count = row[0] if row and row[0] is not None else 0
 cursor.execute("SELECT SUM(xp) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 row = cursor.fetchone()
 total_xp = row[0] if row and row[0] is not None else 0
 text += f"\n<b>Всего: {total_count} карт | {total_xp} XP</b>"
 if len(text) >= 4096:
  part1 = text[:4096].replace("<b>", "").replace("</b>", "")
  part2 = text[4096:].replace("<b>", "").replace("</b>", "")
  await message.answer(part1)
  await asyncio.sleep(2)
  await message.answer(part2)
 else:
  await message.answer(text)  

@dp.message(Command("broadcast"))  # АДМИН КОМАНДА v0.1.1+
async def broadcast(message: types.Message):
 if message.from_user.id != dev_id:
  text = "У вас недостаточно прав для использованя команды /broadcast."
  await message.answer(text)
  return
 text = (
  "<b>⚡️ ОБНОВЛЕНИЕ v0.1.3 ВЫШЛО!</b>\n\n"
  "Новое:\n"
  "<blockquote>— Добавлен расширенный набор карт с 4 видами карт внутри.\n"
  "— Внедрена система стадий прохождения игры. Прогресс теперь дозируется: на первой стадии доступны только <b>Обычные Наборы</b>, после завершения открывается вторая стадия с доступом к <b>Расширенному Набору</b>.\n"
  "— Добавлен общий счётчик прохождения игры.\n"
  "— Запущена система глобальных достижений. Игроки набирают определённый тираж конкретных карт, после чего все получают награды в зависимости от личного вклада. На данный момент доступно 4 вида достижений с <b>самыми редкими картами в игре</b>, а также по общему тиражу. Все глобальные достижения можно посмотреть через инлайн-кнопку в лидерборде.\n"
  "— Полностью переработана команда /profile. Теперь она работает как RP-команда (требует аргумент при вводе) и поддерживает как <b>Telegram-ID</b>, так и <b>юзернеймы</b>.\n"
  "— Добавлена команда /settings с тремя настройками: <b>количество одновременно открываемых наборов</b>, <b>отображение префиксов</b> и <b>раздел контрибьюторов</b>.</blockquote>\n\n"
  "QoL:\n"
  "<blockquote>— Добавлены префиксы <b>[NEW]</b> для карт, которые игрок выбил впервые.\n"
  "— Добавлены уникальные префиксы для игроков: <b>[DEV]</b>, <b>[🥇]</b>, <b>[🥈]</b>, <b>[🥉]</b>.</blockquote>\n\n"
  "Изменения баланса:\n"
  "<blockquote>— Уменьшено количество опыта за <b>собрание полной коллекции карт обычного набора</b>: 250 XP → 50 XP.\n"
  "— Изменены награды за <b>открытие карт первыми в мире</b>: теперь вместо опыта игроки получают наборы соответствующей стадии в количестве от 1 до 5 (в зависимости от редкости карты).\n"
  "— После прохождения стадии опыт за <b>открытие карт из уже завершённой стадии</b> уменьшен в два раза.\n"
  "— Улучшены награды за итоговые места в сезоне: <b>1 место</b> — x1 Пожизненный Водолаз Джо Байден + 5 текущих наборов карт; <b>2 место</b> — 5 текущих наборов карт; <b>3 место</b> — 3 текущих набора карт; <b>остальные места</b> — 1 текущий набор карт.\n"
  "— Увеличена базовая стоимость <b>Обычных Наборов Карт</b> в магазине: 10 XP → 15 XP.</blockquote>\n\n"
  "Техническое:\n"
  "<blockquote>— Значительная оптимизация кода и рефакторинг базы данных.</blockquote>\n\n"
  "В честь выхода обновления команда /claim была возвращена. Теперь по ней можно забрать <b>x5 Обычных Наборов Карт</b> или <b>x3 Расширенных Наборов Карт</b> в зависимости от текущей стадии."
 )
 cursor.execute("SELECT user_id FROM users")
 rows = cursor.fetchall()
 count = 0
 if int(time.time()) < 1781631002:
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
 else:
  await message.answer("Слишком поздно для рассылки. Ограничение по времени активизировано.")
 
@dp.message(Command("claim")) # КОМАНДА ДЛЯ ПОЛУЧЕНИЯ ПОДАРКОВ v0.1.1+
async def gift_claiming(message: types.Message):
 try:
  cursor.execute("ALTER TABLE users ADD COLUMN collected_gift INTEGER DEFAULT 0")
  db.commit()
 except sqlite3.OperationalError:
  print("Столбец id уже существует.")
 user_id = message.from_user.id
 cursor.execute(
    "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
    (user_id, message.from_user.full_name or "Anon")
 )
 cursor.execute("SELECT pack_stage, collected_gift FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 stage = (row[0] if row[0] is not None else 0) if row else 0
 did_collect = (row[1] if row[1] is not None else 0) if row else 0
 if time.time() >= 1781870400:
  text = "⏱️ Срок получения подарка истек. Его действие закончилось 19 июня в 15:00."
  await message.answer(text)
 else:
  if did_collect == 0:
   if stage == 1:
    cursor.execute("UPDATE users SET fpacks = fpacks + 5 WHERE user_id = ?", (user_id,))
    text = "🎁 Вы успешно получили <b>x5 Обычных Наборов Карт</b> в честь выхода v0.1.3!"
   elif stage == 2:
    cursor.execute("UPDATE users SET spacks = spacks + 3 WHERE user_id = ?", (user_id,))
    text = "🎁 Вы успешно получили <b>x3 Расширенных Наборов Карт</b> в честь выхода v0.1.3!"
   else:
    text = "На данный момент для вашего аккаунта не доступны никакие подарки."
    await message.answer(text)
    return
   cursor.execute("UPDATE users SET collected_gift = 1 WHERE user_id = ?", (user_id,))
   db.commit()
   await message.answer(text)
  elif did_collect == 1:
   text = "❗ Вы уже забрали данный подарок."
   await message.answer(text)

@dp.message(Command("market")) # КОМАНДА ВРЕМЕННОГО МАРКЕТА v0.1.2+
async def showing_market(message: types.Message):
 global season, season_start, season_end, season_desc, season_duration
 user_id = message.from_user.id
 cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 pack_stage = row[0] if row else 0
 market_action_chance = random.randint(0, 1000)
 left_before_s_end = season_end - time.time()
 if 86400 >= left_before_s_end > 0:
  h = int(left_before_s_end // 3600)
  m = int((left_before_s_end % 3600) // 60)
  text = (
   f"<b>🛍 ВРЕМЕННЫЙ МАРКЕТ</b> — до закрытия {h}ч {m}м\n\n"
   "<blockquote>Здесь вы можете обменять ваш опыт в конце сезона на наборы карт, чтобы поохотиться за новыми добавленными редкими картами или получить фору в начале следующего сезона.</blockquote>\n\n"
   "Доступные акции:\n"
   "<blockquote>🃏 <b>x1 Обычный Набор Карт</b> — 15 XP\n"
   "🃏 <b>x10 Обычных Наборов Карт</b> — <s>150</s> 130 XP (-10%)"
  )
  if pack_stage > 1:
   text += (
    "\n🃏 <b>x1 Расширенный Набор Карт</b> — <s>25</s> 22 XP"
    "\n🃏 <b>x10 Расширенных Наборов Карт</b> — <s>250</s> 200 XP (-20%)"
   )
  if pack_stage > 1 and market_action_chance <= 67:
   text += "\n🃏 <b>6 Обычных Наборов Карт</b> + <b>7 Обычных Наборов Карт</b> — <s>265</s> 67 XP (-75%)\n\n"
  text += "\n\nВыберите акцию для покупки"
  market_purchase_selection = InlineKeyboardBuilder() # Выбор покупки во временном маркете
  market_purchase_selection.button(text="x1 Обычный Набор Карт — 15 XP", callback_data="one_fpack_purchase")
  market_purchase_selection.button(text="x10 Обычных Наборов Карт — 130 XP", callback_data="ten_fpacks_purchase")
  if pack_stage > 1:
   market_purchase_selection.button(text="x1 Расширенный Набор Карт — 23 XP", callback_data="one_spack_purchse")
   market_purchase_selection.button(text="x10 Расширенных Наборов Карт — 200 XP", callback_data="ten_spack_purchase")
  if pack_stage > 1 and market_action_chance <= 67:
   market_purchase_selection.button(text="x6 Обычных Наборов Карт + x7 Расширенных Наборов Карт — 67 XP", callback_data="action_67_purchase")
  market_purchase_selection.adjust(1)
  await message.answer(text, reply_markup=market_purchase_selection.as_markup())
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await message.answer(text)

@dp.callback_query(F.data == "one_fpack_purchase")
async def processing_one_fpack_purchase(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 left_before_s_end = season_end - time.time()
 if 86400 >= left_before_s_end > 0:
  user_id = callback.from_user.id
  cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  xp = row[0] if row else 0
  if xp >= 15:
   cursor.execute("UPDATE users SET xp = xp - 15, fpacks = fpacks + 1 WHERE user_id = ?", (user_id,))
   db.commit()
   text = "Вы успешно приобрели <b>x1 Обычный Набор Карт</b> за 15 XP"
   await callback.message.answer(text)
  else:
   text = "Недостаточно XP для покупки. Попробуйте позже."
   await callback.message.answer(text)
  await callback.answer()
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await callback.message.answer(text)
  await callback.answer()

@dp.callback_query(F.data == "ten_fpacks_purchase")
async def processing_ten_fpacks_purchase(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 left_before_s_end = season_end - time.time()
 if 86400 >= left_before_s_end > 0:
  user_id = callback.from_user.id
  cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  xp = row[0] if row else 0
  if xp >= 130:
   cursor.execute("UPDATE users SET xp = xp - 130, fpacks = fpacks + 10 WHERE user_id = ?", (user_id,))
   db.commit()
   text = "Вы успешно приобрели <b>x10 Обычных Наборов Карт</b> за 130 XP"
   await callback.message.answer(text)
  else:
   text = "Недостаточно XP для покупки. Попробуйте позже."
   await callback.message.answer(text)
  await callback.answer()
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await callback.message.answer(text)
  await callback.answer()

@dp.callback_query(F.data == "one_spack_purchase")
async def processing_one_spack_purchase(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 left_before_s_end = season_end - time.time()
 if 86400 >= left_before_s_end > 0:
  user_id = callback.from_user.id
  cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  xp = row[0] if row else 0
  if xp >= 22:
   cursor.execute("UPDATE users SET xp = xp - 22, spacks = spacks + 1 WHERE user_id = ?", (user_id,))
   db.commit()
   text = "Вы успешно приобрели <b>x1 Расширенный Набор Карт</b> за 22 XP"
   await callback.message.answer(text)
  else:
   text = "Недостаточно XP для покупки. Попробуйте позже."
   await callback.message.answer(text)
  await callback.answer()
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await callback.message.answer(text)
  await callback.answer()

@dp.callback_query(F.data == "ten_spacks_purchase")
async def processing_ten_spacks_purchase(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 left_before_s_end = season_end - time.time()
 if 86400 >= left_before_s_end > 0:
  user_id = callback.from_user.id
  cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  xp = row[0] if row else 0
  if xp >= 200:
   cursor.execute("UPDATE users SET xp = xp - 200, spacks = spacks + 10 WHERE user_id = ?", (user_id,))
   db.commit()
   text = "Вы успешно приобрели <b>x10 Расширенных Наборов Карт</b> за 200 XP"
   await callback.message.answer(text)
  else:
   text = "Недостаточно XP для покупки. Попробуйте позже."
   await callback.message.answer(text)
  await callback.answer()
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await callback.message.answer(text)
  await callback.answer()

@dp.callback_query(F.data == "action_67_purchase")
async def processing_67action_purchase(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 left_before_s_end = season_end - time.time()
 cursor.execute("SELECT purchased_special_action, pack_stage FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 did_buy_or_no, pack_stage = row if row else (0, 0)
 if 86400 >= left_before_s_end > 0 and did_buy_or_no == 0:
  user_id = callback.from_user.id
  cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  xp = row[0] if row else 0
  if xp >= 67:
   cursor.execute("UPDATE users SET xp = xp - 67, fpacks = fpacks + 6, spacks = spacks + 7 WHERE user_id = ?", (user_id,))
   db.commit()
   text = "Вы успешно приобрели <b>x6 Обычных Наборов Карт</b> и <b>x7 Расширенных Наборов Карт</b> за 67 XP"
   await callback.message.answer(text)
  else:
   text = "Недостаточно XP для покупки. Попробуйте позже."
   await callback.message.answer(text)
  await callback.answer()
 elif 86400 >= left_before_s_end > 0 and did_buy_or_no == 1:
  text = f"Вы уже приобрели эту одноразовую акцию."
  await callback.message.answer(text)
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await callback.message.answer(text)
  await callback.answer()

@dp.message(Command("leaderboard")) # СПИСОК ЛИДЕРОВ v0.1+
async def show_leaderboard(message: types.Message):
 text = "Выберите режим лидерборда для его просмотра:"
 await message.answer(text, reply_markup=leaderboard_mode_selection.as_markup())

@dp.callback_query(F.data == "season_leaderboard") # Сезонный лидерборд
async def handle_season_leaderboard(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 cursor.execute("SELECT full_name, xp FROM users WHERE user_id NOT IN (?, ?) ORDER BY XP DESC LIMIT 5", (dev_id, dev_mini_id))
 users = cursor.fetchall()
 results = "<b>🏆 СЕЗОННЫЙ ЛИДЕРБОРД</b>\n"
 left_before_s_end = max(0, int(season_end - time.time()))
 d = int(left_before_s_end // 86400)
 h = int((left_before_s_end % 86400) // 3600)
 if time.time() < 1780912800:
  results += (
   f"Досезонный период — {d}д {h}ч\n\n"
   f"<blockquote>{season_desc}</blockquote>\n\n"
  )
 else:
  results += (
   f"Активный сезон — {d}д {h}ч\n\n"
   f"<blockquote>{season_desc}</blockquote>\n\n"
  )
 results += (
  "Награды сезона:\n"
  "<blockquote>Топ-1 — <b>x1 Пожизненный Водолаз Джо Байден</b> + <b>x5 текущих наборов карт</b>\n"
  "Топ-2 — <b>x5 текущих наборов карт</b>\n"
  "Топ-3 — <b>x3 текущих наборов карт</b>\n"
  "Остальные — <b>x1 текущий набор карт</b></blockquote>\n\n"
 )
 rank = 1
 for user in users:
  medal = "👑" if rank == 1 else f"{rank}"
  dot = "" if rank == 1 else "."
  results += f"{medal}{dot} {escape(user[0])} — {user[1]} XP\n"
  rank += 1
 cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 row = cursor.fetchone()
 total_cards = row[0] if row and row[0] else 0
 results += f"\nВсего карточек существует: {total_cards}\n\n"
 await callback.message.answer(results) 
 await callback.answer()

@dp.callback_query(F.data == "records_leaderboard") # Лидерборд достижений
async def handle_records_leaderboard(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 cursor.execute("SELECT full_name FROM users WHERE unlocked_cards = 9 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with9 = cursor.fetchall()
 cursor.execute("SELECT full_name FROM users WHERE unlocked_cards = 10 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with10 = cursor.fetchall()
 cursor.execute("SELECT COUNT(*) FROM users WHERE unlocked_cards = 9 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with_full_coll9 = cursor.fetchone()[0] or 0
 cursor.execute("SELECT COUNT(*) FROM users WHERE unlocked_cards = 10 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with_full_coll10 = cursor.fetchone()[0] or 0
 results = "<b>🏆 ЛИДЕРБОРД ДОСТИЖЕНИЙ</b>"
 if users_with9:
  names_9 = [escape(u[0]) for u in users_with9]
  results += "\n\nПолная коллекция (9/9):\n" + ", ".join(names_9)
  results += f"\nВсего игроков: {users_with_full_coll9}"
 if users_with10:
  names_10 = [escape(u[0]) for u in users_with10]
  results += "\n\nПолная коллекция (10/10):\n" + ", ".join(names_10)
  results += f"\nВсего игроков: {users_with_full_coll10}"
 cursor.execute("SELECT winner_s0 FROM season_info")
 row = cursor.fetchone()
 the_winner_s0 = row[0] if row and row[0] is not None else "None"
 if the_winner_s0:
  results += (
   "\n\nПобедители сезонов:"
   f"\n<blockquote>{escape(the_winner_s0)} — топ-1 мира в досезонном периоде</blockquote>"
  ) 
 results += (
  "\n\n<b>АРХИВИРОВАННЫЕ ДОСТИЖЕНИЯ</b>"
  "\n\nПервооткрыватели:"
  "\n<blockquote>Victony Universal — первый в мире <b>Открытый Набор</b> (23.04)"
 )
 for i in card_drop_diapazones.keys():
  cursor.execute("SELECT first_unlocked FROM card_stats WHERE card_id = ?", (i,))
  row = cursor.fetchone()
  first = row[0] if row else None
  cursor.execute("SELECT full_name FROM users WHERE user_id = ?", (dev_id,))
  row = cursor.fetchone()
  dev_name = row[0] if row else 0
  cursor.execute("SELECT full_name FROM users WHERE user_id = ?", (dev_mini_id,))
  row = cursor.fetchone()
  dev_mini_name = row[0] if row else 0
  if first in (dev_name, dev_mini_name):
   first = None
  if i in (1, 2, 3, 4, 5, 6):
   results += f"\n{escape(first)} — первый в мире <b>{card_names.get(i)}</b> ({first_unlocked_date.get(i)})"
  elif i in (7, 8, 9, 10):
   try: 
    results += f"\n{escape(first)} — первый в мире <b>{card_names.get(i)} ({first_unlocked_date.get(i)}</b>"
   except AttributeError:
    continue
 results += "\ncwendyzz — первая в мире <b>Полная Коллекция 4/4</b> (26.04)"
 results += "\nMᴇ Cʀᴀꜰᴛ♡ — первая в мире <b>Полная Коллекция 5/5</b> (08.06)</blockquote>"
 await callback.message.answer(results)
 await callback.answer()

@dp.callback_query(F.data == "global_achievements") # Глобальные достижения
async def handle_global_achievements(callback: CallbackQuery):
 try:
  cursor.execute("ALTER TABLE global_rewards ADD COLUMN id INTEGER DEFAULT 1")
  db.commit()
 except sqlite3.OperationalError:
  print("Столбец id уже существует.")
 results = "<b>ГЛОБАЛЬНЫЕ ДОСТИЖЕНИЯ</b>\n\n"
 cursor.execute("SELECT total_cards_st1, total_cards_st2, total_cards_st3, sigma_cards_st1, sigma_cards_st2, diver_cards_st1, diver_cards_st2, diver_cards_st3, sixseven_cards_st1, sixseven_cards_st2, sixseven_cards_st3 FROM global_rewards WHERE id = 1")
 rows = cursor.fetchall()
 if rows:
  row_data = rows[0]
  columns = ["total_cards_st1", "total_cards_st2", "total_cards_st3", "sigma_cards_st1", "sigma_cards_st2", "diver_cards_st1", "diver_cards_st2", "diver_cards_st3", "sixseven_cards_st1", "sixseven_cards_st2", "sixseven_cards_st3"]
  for i, reward_name in enumerate(columns):
   target = row_data[i]
   if reward_name in ("total_cards_st1", "total_cards_st2", "total_cards_st3"):
    cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
   elif reward_name in ("sigma_cards_st1", "sigma_cards_st2"):
    cursor.execute("SELECT SUM(count) FROM user_cards WHERE card_id = 5 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
   elif reward_name in ("diver_cards_st1", "diver_cards_st2", "diver_cards_st3"):
    cursor.execute("SELECT SUM(count) FROM user_cards WHERE card_id = 1 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
   elif reward_name in ("sixseven_cards_st1", "sixseven_cards_st2", "sixseven_cards_st3"):
    cursor.execute("SELECT SUM(count) FROM user_cards WHERE card_id = 2 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
   info = cursor.fetchone()
   count = info[0] if info else 0
   if target == 1:
    results += (
     f"<blockquote><b>🏆 {global_rewards_names.get(reward_name)} — {global_rewards_indicators.get(reward_name)}/{global_rewards_indicators.get(reward_name)}</b>\n"
     f"Полная награда: {global_rewards.get(reward_name)} XP (получена)</blockquote>\n\n"
    )
   else:
    results += (
     f"<blockquote><b>{global_rewards_names.get(reward_name)} — {count}/{global_rewards_indicators.get(reward_name)}</b>\n"
     f"Полная награда: {global_rewards.get(reward_name)} XP</blockquote>\n\n"
    )
  await callback.message.answer(results)
  await callback.answer()

@dp.message(Command("start")) # КОМАНДА ДЛЯ СТАРТА v0.1+
async def showing_welcome_message(message: types.Message):
 nickname = message.from_user.full_name
 user_id = message.from_user.id
 username = message.from_user.username
 cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)", (user_id, nickname or "Anon", username or "None"))
 cursor.execute("UPDATE users SET full_name = ?, username = ? WHERE user_id = ?", (nickname or "Anon", username or "Anon", user_id))
 db.commit()
 text = (
 "<b>👋 Привет, ты попал в Joe Biden Cards.</b>\n\n"
 "Здесь ты можешь выбивать разные карточки с <b>Джо Байденом</b>, коллекционировать их и просто проводить время.\n\n"
 "Проект находится в <b>начальной разработке</b>, поэтому в нём могут присутствовать некоторые баги.\n\n"
 "Создано @by_when\n\n"
 "<b>GitHub</b> — https://github.com/wheennn/Joe-Biden-Cards-Bot-RU\n\n"
 "Весь материал используется исключительно в <b>шуточных целях</b>.\n\n"
 "Чтобы начать игру, используйте команду /card\n\n"
 "Актуальная версия: v0.1.3"
 )
 await message.answer(text)

@dp.message(Command("menu")) # КОМАНДА МЕНЮ v0.1+
async def handle_answer(message: types.Message):
 nickname = message.from_user.full_name
 user_id = message.from_user.id
 username = message.from_user.username
 user_id = message.from_user.id
 cursor.execute(
    "INSERT OR IGNORE INTO settings (user_id, openings_per_time, showing_prefixes) VALUES (?, 1, 1)",
    (user_id,)
 )
 cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)", (user_id, nickname or "Anon", username or "None"))
 cursor.execute("UPDATE users SET full_name = ?, username = ? WHERE user_id = ?", (nickname or "Anon", username or "Anon", user_id))
 db.commit()
 cursor.execute("SELECT full_name, xp, unlocked_cards, total_cards, fpacks, spacks, total_progress, pack_stage, fpack_unlocked_cards, spack_unlocked_cards, fpack_progress, spack_progress FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone() 
 info = row if row else ("Неизвестный пользователь", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
 if info[0] == "Неизвестный пользователь":
  text = "Вас не найдено в базе данных. Попробуйте ещё раз после открытия набора карт."
  await message.answer(text)
  waiting_users.discard(user_id)
  return
 cursor.execute("SELECT showing_prefixes FROM settings WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 showing_prefixes = row[0] if row else 0
 cursor.execute("SELECT user_id FROM users WHERE user_id NOT IN (?, ?) ORDER BY xp DESC LIMIT 3",(dev_id, dev_mini_id))
 rows = cursor.fetchall()
 top_ids = [r[0] for r in rows]
 while len(top_ids) < 3:
  top_ids.append(0)
 if showing_prefixes == 1:
  if user_id in (dev_id, dev_mini_id):
   status = "[DEV] "
  elif user_id == top_ids[0]:
   status = "[🥇] "
  elif user_id == top_ids[1]:
   status = "[🥈] "
  elif user_id == top_ids[2]:
   status = "[🥉] "
  else:
   status = ""
 else:
  status = ""
 stage_progress = info[10] if info[7] == 1 else info[11] 
 text = (
  f"<b>{status}{escape(info[0])} | {info[1]} XP</b>\n"
  f"Стадия прохождения: {info[7]} [{stage_progress}%]"
 )
 if get_user_card_count(user_id, 6) > 0:
  text += (
   "\n\nЭксклюзивные:"
   f"\n<blockquote>Пожизненный Водолаз Джо Байден — x{get_user_card_count(user_id, 6)}</blockquote>"
  )
 cursor.execute("SELECT total_cards FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 total_cards = row[0] if row else 0
 if total_cards > 0:
  text += "\n\nОбычные:\n<blockquote>"
 for i in card_drop_diapazones.keys():
  if get_user_card_count(user_id, i) > 0:
   text += f"{card_names.get(i, "")} — x{get_user_card_count(user_id, i)}\n"
 if info[2] <= 9 and get_user_card_count(user_id, 6) == 0:
  text += (
   f"</blockquote>\nВсего: {info[3]} | {info[2]}/9 открыто\n"
   f"Обычные наборы карт: {info[4]} | Расширенные наборы карт: {info[5]}"
  )
 elif info[2] <= 9 and get_user_card_count(user_id, 6) > 0:
  text += (
   f"</blockquote>\nВсего: {info[3]} | {info[2]}/10 открыто\n"
   f"Обычные наборы карт: {info[4]} | Расширенные наборы карт: {info[5]}"
 )
 elif info[2] == 10 and get_user_card_count(user_id, 6) > 0:
  text += (
   f"</blockquote>\nВсего: {info[3]} | {info[2]}/10 открыто \n"
   f"Обычные наборы карт: {info[4]} | Расширенные наборы карт: {info[5]}"
  )
 text += f"\nПроцент прохождения: {info[6]}%"
 await message.answer(text)

@dp.message(Command("card")) # КОМАНДА ДЛЯ ОТКРЫТИЯ КАРТЫ v0.1+
async def handling_fpack_info(event: types.Message | types.CallbackQuery):
 user_id = event.from_user.id
 nickname = event.from_user.full_name
 username = event.from_user.username
 user_id = event.from_user.id
 cursor.execute(
    "INSERT OR IGNORE INTO settings (user_id, openings_per_time, showing_prefixes) VALUES (?, 1, 1)",
    (user_id,)
 )
 cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)", (user_id, nickname or "Anon", username or "None")
 )
 cursor.execute("UPDATE users SET full_name = ?, username = ? WHERE user_id = ?", (nickname or "Anon", username or "Anon", user_id)
 )
 db.commit()
 text = (
  "<b>Обычный Набор Карт с Джо Байденом</b>\n\n"
  "• Шансы:\n\n"
  "Сигма Джо Байден — 1%\n"
  "Водолаз Джо Байден — 4%\n"
  "Сикс Севен Джо Байден — 10%\n"
  "Праздничный Джо Байден — 30%\n"
  "Обычный Джо Байден — 55%"
 )
 card_pack_selection = InlineKeyboardBuilder() # Выбор действия при просмотре информации набора карт
 card_pack_selection.button(text="Открыть", callback_data="opening_fpack_method")
 card_pack_selection.button(text="Следующий набор", callback_data="next_pack")
 card_pack_selection.adjust(1)
 if isinstance(event, types.Message):
  await event.answer(text, reply_markup=card_pack_selection.as_markup())
 elif isinstance(event, types.CallbackQuery):
  await event.message.edit_text(text=text, reply_markup=card_pack_selection.as_markup())
  await event.answer()

@dp.callback_query(F.data == "opening_fpack_method")
async def opening_fpack(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 last_opening_time = row[0] if row else 0
 current_left = fpack_CD - int(time.time() - last_opening_time)
 cursor.execute("SELECT fpacks FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 fpacks = row[0] if row else 0
 card_pack_opening_selection = InlineKeyboardBuilder() # Выбор способа открытия набора карт
 if current_left > 0:
  minutes = current_left // 60
  seconds = current_left % 60
  card_pack_opening_selection.button(text=f"Бесплатно ({minutes}m {seconds}s)", callback_data="opening_fpack_through_cd")
 elif current_left <= 0:
  card_pack_opening_selection.button(text="Бесплатно", callback_data="opening_fpack_through_cd")
 if fpacks > 0:
  card_pack_opening_selection.button(text=f"Открыть из запасов ({fpacks} шт.)", callback_data="opening_fpack_through_accums")
 card_pack_opening_selection.adjust(1)
 await callback.message.edit_text(text=f"Выберите способ открытия:",reply_markup=card_pack_opening_selection.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "opening_spack_method")
async def opening_fpack(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 last_opening_time = row[0] if row else 0
 current_left = spack_CD - int(time.time() - last_opening_time)
 cursor.execute("SELECT spacks FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 spacks = row[0] if row else 0
 card_pack_opening_selection = InlineKeyboardBuilder() # Выбор способа открытия набора карт
 if current_left > 0:
  minutes = current_left // 60
  seconds = current_left % 60
  card_pack_opening_selection.button(text=f"Бесплатно ({minutes}m {seconds}s)", callback_data="opening_spack_through_cd")
 elif current_left <= 0:
  card_pack_opening_selection.button(text="Бесплатно", callback_data="opening_spack_through_cd")
 if spacks > 0:
  card_pack_opening_selection.button(text=f"Открыть из запасов ({spacks} шт.)", callback_data="opening_spack_through_accums")
 card_pack_opening_selection.adjust(1)
 await callback.message.edit_text(text=f"Выберите способ открытия:",reply_markup=card_pack_opening_selection.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "opening_fpack_through_cd")
async def opening_fpack_through_cd(callback: CallbackQuery):
 await card_pack_opening(callback, "fpack", "cd")
 await callback.answer()
  
@dp.callback_query(F.data == "opening_fpack_through_accums")
async def opening_fpack_through_accumulations(callback: CallbackQuery):
 await card_pack_opening(callback, "fpack", "accumulations")
 await callback.answer()

@dp.callback_query(F.data == "opening_spack_through_cd")
async def opening_spack_through_cd(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (user_id,))
 stg = cursor.fetchone()[0]
 if stg >= 2:
  await card_pack_opening(callback, "spack", "cd")
  await callback.answer()
 else:
  text = "Вам не доступен данный набор."
  await callback.message.answer(text)
  await callback.answer()
  
@dp.callback_query(F.data == "opening_spack_through_accums")
async def opening_spack_through_accumulations(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (user_id,))
 stg = cursor.fetchone()[0]
 if stg >= 2:
  await card_pack_opening(callback, "spack", "accumulations")
  await callback.answer()
 else:
  text = "Вам не доступен данный набор."
  await callback.message.answer(text)
  await callback.answer()

@dp.callback_query(F.data == "next_pack")
async def handling_spack_info(callback: CallbackQuery):
 user_id = callback.from_user.id
 nickname = callback.from_user.full_name
 username = callback.from_user.username
 cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)", (user_id, nickname or "Anon", username or "None")
 )
 cursor.execute("UPDATE users SET full_name = ?, username = ? WHERE user_id = ?", (nickname or "Anon", username or "Anon", user_id)
 )
 db.commit()
 cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (user_id,))
 stg = cursor.fetchone()[0]
 is_blocked = "🔒 " if stg < 2 else ""
 text = (
  f"<b>{is_blocked}Расширенный Набор Карт с Джо Байденом</b>\n\n"
  "• Шансы:\n\n"
  "Троллфейс Джо Байден — 5%\n"
  "Джо Байден.exe — 10%\n"
  "Джо Байден в Разрешении 38:9 — 30%\n"
  "Джо Байден в Разрешении 9:38 — 55%"
 )
 card_pack_selection = InlineKeyboardBuilder() # Выбор действия при просмотре информации набора карт
 if stg >= 2:
  card_pack_selection.button(text="Открыть", callback_data="opening_spack_method")
 card_pack_selection.button(text="Предыдущий набор", callback_data="prev_pack")
 card_pack_selection.adjust(1)
 await callback.message.edit_text(text=text, reply_markup=card_pack_selection.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "prev_pack")
async def previous_pack(callback: CallbackQuery):
 await handling_fpack_info(callback)

async def reminder(): # СИСТЕМА НАПОМИНАНИЙ v0.1.1+
 while True:
  cursor.execute("SELECT user_id, last_card_time FROM users")
  rows = cursor.fetchall()
  for user_id, last_card_time in rows:
   if last_card_time == 0: 
    continue
   diff = (time.time() - last_card_time)
   cursor.execute("INSERT OR IGNORE INTO reminder_spam (user_id, reminder_cd, reminder_2, reminder_8, reminder_24) VALUES (?, 0, 0, 0, 0)", (user_id,))
   db.commit()
   cursor.execute("SELECT reminder_cd, reminder_2, reminder_8, reminder_24 FROM reminder_spam WHERE user_id = ?", (user_id,))
   row = cursor.fetchone()
   if not row:
    continue
   await asyncio.sleep(0.1) 
   reminder_cd, reminder_2, reminder_8, reminder_24 = row
   if diff < 1800:
    if reminder_cd != 0 or reminder_2 != 0 or reminder_8 != 0 or reminder_24 != 0:
      cursor.execute("UPDATE reminder_spam SET reminder_cd = 0, reminder_2 = 0, reminder_8 = 0, reminder_24 = 0 WHERE user_id = ?", (user_id,))
      db.commit()
    continue
   try:
    if diff >= 84600 and reminder_24 == 0:
     random_reminder = random.randint(1, 5)
     if random_reminder == 1:
      text = "С момента твоего последнего открытия прошло уже более дня! <b>Ты собираешься играть</b>, или <b>просто дашь обогнать себя в лидерборде</b>?!\n\nНажми /card чтобы открыть набор карточек"
     elif random_reminder == 2:
      text = "😔 Другие игроки вот-вот обгонят тебя и <b>твой опыт зарастёт мхом</b>! У тебя остался <b>последний шанс прежде ты упадёшь в лидерборде</b>.\n\nНажми /card чтобы открыть набор карточек"
     elif random_reminder == 3:
      text = "😢 <b>Джо Байден соскучился по тебе</b>.. Ты не открывал наборы с карточками уже почти 24 часа. У тебя что-то случилось?\n\nЕсли не хочешь расстроить Джо Байдена еще больше, нажми /card чтобы открыть набор карточек"
     elif random_reminder == 4:
      text = "Хочешь получить хотя-бы <b>Водолаза</b> или даже <b>Сигму</b>? Так делай хоть что-то, а то с момента твоего последнего открытия прошёл уже целый день!\n\n<b>Не хочешь оказаться на дне как Водолаз</b>? Заходи и открывай набор с карточками через /card"
     elif random_reminder == 5:
      text = "Знаешь, <b>Сигма Джо Байден</b> ведь тоже не сразу стал таким крутым, <b>он достиг этого самостоятельно</b>. А вот ты — лентяй! Иди и открывай карточку, если хочешь достичь хоть чего-то!\n\nНажми /card для открытия"
     await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_24 = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
    elif 28800 <= diff < 84600 and reminder_8 == 0:
     random_reminder = random.randint(1, 5)
     if random_reminder == 1:
      text = "🙄 Я имел большие надежды на тебя, а <b>ты просто взял и забил</b>! <b>Выбрал личную жизнь, а не меня</b>!\n\nВдруг захочешь исправиться в моих глазах - команда /card тебе поможет"
     elif random_reminder == 2:
      text = "🙄 Хорошо. Я <b>пытался заинтересовать тебя</b>, дать шанс.. Но раз ты не открываешь карточки уже 8 часов, что ж поделаешь!\n\nВдруг захочешь исправиться - нажми команду /card"
     elif random_reminder == 3:
      text = "😡 Ах ты проказник вот такой! Не заходишь в бота уже 8 часов, значит <b>плакал за тобой Сигма</b>! Не быть тебе топ 1 мира с такой дисциплиной.\n\nНажми /card чтобы открыть набор карточек"
     elif random_reminder == 4:
      text = "Легенда гласит — <b>если прямо сейчас откроешь набор, тебе выпадет твоя заветная карточка</b>. Я ведь мудрец — а мудрецы не ошибаются.\n\nВдруг тебе и правда повезет? Просто нажми /card"
     elif random_reminder == 5:
      text = "♾️ Восьмёрка — символ нового начала, возрождения и рая. Именно столько часов ты не открывал карточку, так пойди и открой, и достигнешь своего дзена!\n\nНажми /card чтобы открыть набор карточек"
     await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_8 = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
    elif 7200 <= diff < 28800 and reminder_2 == 0:
     random_reminder = random.randint(1, 4)
     if random_reminder == 1:
      text = "С момента вашего последнего открытия <b>прошло уже около 2 часов</b>.\n\nНажмите /card для открытия"
     elif random_reminder == 2:
      text = "📈 Твои <b>конкуренты уже лутают опыт во всю</b>, а ты что?\n\nНажми /card и компенсируй утерянное"
     elif random_reminder == 3:
      text = "😉 Раз ты хочешь получить хотя бы <b>Сикс Севен Джо</b>, лучше не забывай открывать карточки. А там, вдруг ты захочешь <b>поохотиться за Сигмой и топ 1 мира</b>.\n\nНажми /card чтобы открыть набор карточек"
     elif random_reminder == 4:
      text = "⌛ Часики тикают, а <b>твои шансы достичь топа всё уменьшаются</b>!\n\nНажми /card и компенсируй утерянное"
     await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_2 = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
    elif 1800 <= diff < 7200 and reminder_cd == 0:
     random_reminder = random.randint(1, 2)
     if random_reminder == 1:
      text = "⏱️ КД обычного набора карточек закончился! Нажмите /card для открытия"
     elif random_reminder == 2:
      text = "⏱️ Пришло время выбивать новых Джо Байденов — КД обычного набора карточек закончился! Используй /card для открытия"
     await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_cd = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
   except Exception as e:
    print(f"Не удалось отправить уведомление для {user_id}: {e}")
  unique_time_check = random.randint(1800, 3600)
  await asyncio.sleep(unique_time_check)

@dp.message(Command("settings")) # КОМАНДА НАСТРОЕК v0.1.3+
async def showing_and_setting_up_settings(message: types.Message):
 user_id = message.from_user.id 
 cursor.execute("INSERT OR IGNORE INTO settings (user_id) VALUES (?)", (user_id,))
 db.commit()
 cursor.execute("SELECT openings_per_time, showing_prefixes FROM settings WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 opening_per_time = row[0]
 showing_prefixes = row[1]
 showing_prefixes = "On" if showing_prefixes == 1 else "Off"
 text = (
  "⚙️ <b>НАСТРОЙКИ</b>\n\n"
  f"Открытие карт за раз — {opening_per_time}\n"
  "<blockquote>Количество карт которые открываются за одно нажатие при распаковке из запасов</blockquote>\n\n"
  f"Отображение префиксов — {showing_prefixes}\n"
  "<blockquote>Отображение уникальных префиксов в вашем или чужом профиле</blockquote>\n\n"
  "Контрибьюторы\n"
  "<blockquote>Люди, сделавшие вклад в развитие проекта</blockquote>\n\n"
  "В течение будущих обновлений кастомные функции и настройки будут добавлятся."
 )
 settings = InlineKeyboardBuilder() # Выбор действия в настройках
 settings.button(text="Открытие карт за раз", callback_data="opening_per_time")
 settings.button(text="Отображение префиксов", callback_data="showing_prefixes")
 settings.button(text="Контрибьюторы", callback_data="contributors")
 settings.adjust(1)
 await message.answer(text=text, reply_markup=settings.as_markup())

@dp.callback_query(F.data == "opening_per_time")
async def opening_per_time_setting(callback: CallbackQuery):
 text = "Выберите количество наборов карт которое вы хотите открывать за раз"
 opening_per_time = InlineKeyboardBuilder() # Выбор желанного количества наборов карт которые будут открыты за раз
 opening_per_time.button(text="1", callback_data="opening_one_per_time")
 opening_per_time.button(text="2", callback_data="opening_two_per_time")
 opening_per_time.button(text="3", callback_data="opening_three_per_time")
 await callback.message.edit_text(text=text, reply_markup=opening_per_time.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "opening_one_per_time")
async def opening_one_per_time(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("UPDATE settings SET openings_per_time = 1 WHERE user_id = ?", (user_id,))
 db.commit()
 text = "Вы успешно изменили эту настройку. Теперь при открытии наборов из запасов вы всегда будете открывать по 1 карте за раз."
 await callback.message.answer(text)
 await callback.answer()
 
@dp.callback_query(F.data == "opening_two_per_time")
async def opening_two_per_time(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("UPDATE settings SET openings_per_time = 2 WHERE user_id = ?", (user_id,))
 db.commit()
 text = "Вы успешно изменили эту настройку. Теперь при открытии наборов из запасов вы всегда будете открывать по 2 карты за раз."
 await callback.message.answer(text)
 await callback.answer()

@dp.callback_query(F.data == "opening_three_per_time")
async def opening_three_per_time(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("UPDATE settings SET openings_per_time = 3 WHERE user_id = ?", (user_id,))
 db.commit()
 text = "Вы успешно изменили эту настройку. Теперь при открытии наборов из запасов вы всегда будете открывать по 3 карты за раз."
 await callback.message.answer(text)
 await callback.answer()

@dp.callback_query(F.data == "showing_prefixes")
async def showing_prefixes_setting(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT showing_prefixes FROM settings WHERE user_id = ?", (user_id,))
 showing_prefixes = cursor.fetchone()[0]
 if showing_prefixes == 1:
  cursor.execute("UPDATE settings SET showing_prefixes = 0 WHERE user_id = ?", (user_id,))
  text = "Вы успешно изменили эту настройку. Теперь вам не будут видны особые префиксы перед никами игроков."
 elif showing_prefixes == 0:
  cursor.execute("UPDATE settings SET showing_prefixes = 1 WHERE user_id = ?", (user_id,))
  text = "Вы успешно изменили эту настройку. Теперь вам будут видны особые префиксы перед никами игроков."
 await callback.message.answer(text)
 await callback.answer()
 db.commit()

@dp.callback_query(F.data == "contributors")
async def showing_contributors(callback: CallbackQuery):
 text = (
  "<b>Контрибьюторы\n\n</b>"
  "@take_me_back_to_august — дизайн для Обычного и Праздничного Джо Байденов\n"
  "@Subarash_ii — хостинг бота и поддержка работы сервера"
 )
 await callback.message.answer(text)
 await callback.answer()

@dp.message(Command("profile")) # КОМАНДА ДЛЯ ПРОСМОТРА ЧУЖОГО ПРОФИЛЯ v0.1.2+
async def showing_someones_profile(message: types.Message):
 user_id = message.from_user.id
 text = "Введите ID игрока в телеграме, чей профиль вы хотите просмотреть."
 if message.text != "/profile":
  waiting_users.add(user_id)
 elif message.text == "/profile":
  text = "Команда поддерживается только с вставкой агрумента. Укажите <b>username</b> или <b>Telegram-ID</b> после написания названия команды."
  await message.answer(text)
  return
 if user_id in waiting_users:
  try:
   by_username = False
   given_id = int(message.text.replace("/profile ", ""))
   cursor.execute("SELECT full_name, xp, unlocked_cards, total_cards, fpacks, spacks, total_progress, pack_stage, fpack_unlocked_cards, spack_unlocked_cards, fpack_progress, spack_progress FROM users WHERE user_id = ?", (given_id,))
   row = cursor.fetchone() 
   info = row if row else ("Неизвестный пользователь", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  except ValueError:
   by_username = True
   username = str(message.text.replace("/profile ", "").replace("@", ""))
   cursor.execute("SELECT full_name, xp, unlocked_cards, total_cards, fpacks, spacks, total_progress, pack_stage, fpack_unlocked_cards, spack_unlocked_cards, fpack_progress, spack_progress FROM users WHERE username = ?", (username,))
   row = cursor.fetchone() 
   info = row if row else ("Неизвестный пользователь", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  if info[0] == "Неизвестный пользователь":
   text = "Данного пользователя не найдено в базе данных. Попробуйте ещё раз."
   await message.answer(text)
   waiting_users.discard(user_id)
   return
  arg = given_id if by_username == False else username
  cursor.execute("SELECT user_id FROM users WHERE user_id NOT IN (?, ?) ORDER BY xp DESC LIMIT 3",(dev_id, dev_mini_id))
  rows = cursor.fetchall()
  top_ids = [r[0] for r in rows]
  while len(top_ids) < 3:
   top_ids.append(0)
  if by_username:
   cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
   row = cursor.fetchone()
   arg_id = row[0] if row else 0
  else:
   arg_id = given_id
  cursor.execute("SELECT showing_prefixes FROM settings WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  showing_prefixes = row[0] if row else 0
  if showing_prefixes == 1:
   if arg_id in (dev_id, dev_mini_id):
    status = "[DEV] "
   elif arg_id == top_ids[0]:
    status = "[🥇] "
   elif arg_id == top_ids[1]:
    status = "[🥈] "
   elif arg_id == top_ids[2]:
    status = "[🥉] "
   else:
    status = ""
  else:
   status = ""
  stage_progress = info[10] if info[7] == 1 else info[11] 
  text = (
   f"<b>{status}{escape(info[0])} | {info[1]} XP</b>\n"
   f"Стадия прохождения: {info[7]} [{stage_progress}%]"
  )
  if get_user_card_count(arg_id, 6) > 0:
   text += (
    "\n\nЭксклюзивные:"
    f"\n<blockquote>Пожизненный Водолаз Джо Байден — x{get_user_card_count(arg_id, 6)}</blockquote>"
   )
  cursor.execute("SELECT total_cards FROM users WHERE user_id = ?", (arg_id,))
  row = cursor.fetchone()
  total_cards = row[0] if row else 0
  if total_cards > 0:
   text += "\n\nОбычные:\n<blockquote>"
  for i in card_drop_diapazones.keys():
   if get_user_card_count(arg_id, i) > 0:
    text += f"{card_names.get(i, "")} — x{get_user_card_count(arg_id, i)}\n"
  if info[2] <= 9 and get_user_card_count(arg_id, 6) == 0:
   text += (
    f"</blockquote>\nВсего: {info[3]} | {info[2]}/9 открыто\n"
    f"Обычные наборы карт: {info[4]} | Расширенные наборы карт: {info[5]}"
   )
  elif info[2] <= 9 and get_user_card_count(arg_id, 6) > 0:
   text += (
    f"</blockquote>\nВсего: {info[3]} | {info[2]}/10 открыто\n"
    f"Обычные наборы карт: {info[4]} | Расширенные наборы карт: {info[5]}"
  )
  elif info[2] == 10 and get_user_card_count(arg_id, 6) > 0:
   text += (
    f"</blockquote>\nВсего: {info[3]} | {info[2]}/10 открыто \n"
    f"Обычные наборы карт: {info[4]} | Расширенные наборы карт: {info[5]}"
   )
  text += f"\nПроцент прохождения: {info[6]}%"
  await message.answer(text)
  waiting_users.discard(user_id)

async def main():
 asyncio.create_task(reminder())
 asyncio.create_task(season_dispatcher())
 asyncio.create_task(global_rewards_dispatcher())
 await dp.start_polling(bot)

if __name__ == "__main__":
 try:
  asyncio.run(main())
 except KeyboardInterrupt:
  print("Бот выключен")
  print("67")