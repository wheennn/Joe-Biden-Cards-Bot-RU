# Joe Biden Cards — v0.1.4
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
season_start = 0
season_end = 0
season_desc = ""
season_duration = 0
season = 0
waiting_users = set()
if int(time.time()) <= 1782594000:
 fpack_CD = 900 * 0.8
 spack_CD = 1800 * 0.8
else:
 fpack_CD = 900
 spack_CD = 1800
fpack_full_coll = 5
spack_full_coll = 5
exclusive_full_coll = 1
full_coll = 10

base_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(base_dir, "data.env"))

token = os.getenv("BOT_TOKEN")
test_token = os.getenv("TEST_BOT_TOKEN")
db_name = os.getenv("DATABASE").strip()
dev_id = int(os.getenv("DEV_ID"))
dev2_id = int(os.getenv("DEV2_ID"))
dev_mini_id = int(os.getenv("DEV_MINI_ID"))

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
 10: "Троллфейс Джо Байден",
 11: "Финальный Босс Джо Байден"
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
 10: "Очень могущественный и непобедимый Джо Байден. Натапал хомячка в 2024 году и ушёл на пенсию, ведь заработал на три поколения вперёд. Одет в стильную маску троллфейса, чтобы демонстрировать всем, что с ним лучше не шутить.",
 11: "Последний и самый хардкорный босс, выбивание которого становится настоящим испытанием. Сбежал из популярной RPG-игры, чтобы попасть в Joe Biden Cards и показать игрокам своё величие. Закован в тяжёлую броню, вооружён огромным мечом и появляется прямо посреди очередной пламенной зарубы. Говорят, победить его невозможно. К счастью — выбить можно."
}
card_drop_diapazones = {
 11: 1,
 10: 5,
 9: 15,
 8: 45,
 7: 100,
 5: 1,
 1: 5,
 2: 15,
 3: 45,
 4: 100
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
 10: 4,
 11: 1
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
 11: 190
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
 10: "21.06"
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
prefixes = {
 1: "[DEV] ",
 2: "[🥇] ",
 3: "[🥈] ",
 4: "[🥉] "
}
season_nums_to_words = {
 0: "нулевом",
 1: "первом",
 2: "втором",
 3: "третьем",
 4: "четвёртом",
 5: "пятом"
}

leaderboard_mode_selection = InlineKeyboardBuilder() # Выбор фильтра лидерборда
leaderboard_mode_selection.button(text="Сезонный лидерборд", callback_data="season_leaderboard")
leaderboard_mode_selection.button(text="Лидерборд достижений", callback_data="records_leaderboard")
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
 reward_name TEXT NOT NULL,
 reward_indicator INTEGER NOT NULL,
 reward_xp INTEGER NOT NULL,
 reward_stage INTEGER NOT NULL,
 status INTEGER DEFAULT 0 NOT NULL,
 id INTEGER DEFAULT 1 NOT NULL,
 CONSTRAINT status_check CHECK (status IN (0, 1)),
 CONSTRAINT stage_check CHECK (reward_stage IN (1, 2, 3, 4, 5)),
 UNIQUE(id, reward_name, reward_stage)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
 openings_per_time INTEGER DEFAULT 1,
 showing_prefixes INTEGER DEFAULT 1,
 user_id INTEGER PRIMARY KEY
)
""")
db.commit()

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
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 opening_time_before = row[0] if row else 0
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
  if type == "cd":
   if pack_name == "fpack":
    current_left = fpack_CD - int(time.time() - opening_time_before)
   else:
    current_left = spack_CD - int(time.time() - opening_time_before)
   if current_left > 0:
    minutes = int(current_left // 60)
    seconds = int(current_left % 60)
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
      cursor.execute("UPDATE users SET spack_progress = spack_progress + 20 WHERE user_id = ?", (user_id,))
     cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
     cursor.execute("UPDATE users SET total_progress = total_progress + 10 WHERE user_id = ?", (user_id,))
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
     card_ids = [5, 1, 2, 3, 4] if pack_name == "fpack" else [11, 10, 9, 8, 7] if pack_name == "spack" else [0, 0, 0, 0, 0]
     from_where = "Обычного Набора Карт" if pack_name == "fpack" else "Расширенного Набора Карт" if pack_name == "spack" else ""
     stage = "Первой стадии" if pack_name == "fpack" else "Второй стадии" if pack_name == "spack" else ""
     next_stage = "Второй стадии" if pack_name == "fpack" else "Третьей стадии" if pack_name == "spack" else ""
     reward_xp = 50 if pack_name == "fpack" else 125 if pack_name == "spack" else 0
     unlocked_pack = "Расширенный Набор Карт" if pack_name == "fpack" else "tpack" if pack_name == "spack" else ""
     text = (
      f"Вы собрали <b>полную коллекцию Джо Байденов</b> из <b>{from_where}</b> и завершили прохождение <b>{stage}</b>! Последней нужной картой стал <b>{card_names.get(i, "")}</b>. Теперь вы разблокировали <b>{unlocked_pack}</b> и начали прохождение <b>{next_stage}</b>. В честь этого вы получаете награду в виде <b>{reward_xp} XP</b> и <b>3 следующих набора карт</b>.\n"
      f"С этого момента при открытии {from_where[:-5].lower()} вы будете получать в два раза меньше опыта.\n\n"
      "<b>Ваши показатели на момент достижения:</b>\n<blockquote>"
     )
     for i in card_ids:
      text += f"{card_names.get(i)} — x{get_user_card_count(user_id, i)}\n"
     text += (
      f"В сумме: {sum(get_user_card_count(user_id, cid) for cid in card_ids)}</blockquote>\n"
      "Вы можете поделиться или померяться данными счетчиками с вашими друзьями, пересылая это сообщение.\n\n"
      "Для открытия и просмотра нового набора нажмите /card, или /menu для просмотра вашей уникальной коллекции"
     )
     if pack_name == "fpack":
      cursor.execute("UPDATE users SET xp = xp + 50, spacks = spacks + 3, pack_stage = 2 WHERE user_id = ?", (user_id,))
     elif pack_name == "spack":
      cursor.execute("UPDATE users SET xp = xp + 125 WHERE user_id = ?", (user_id,))
     db.commit()
     await callback.message.answer(text)
    if total_before == full_coll - 1 and total_after == full_coll: 
     text = (
      f"<b>{escape(nickname)}</b>, вы собрали <b>полную коллекцию Джо Байденов</b> из <b>10 карт</b>! Теперь вы официально прошли <b>Joe Biden Cards</b> и ваш общий достигнутый <b>прогресс равен 100%</b>!\n\n"
      "Поскольку бот активно обновляется и выходят новые карты, с целью баланса мы не можем выдать вам какую-либо награду, но знайте, <b>ваше имя</b> уже записано в <b>истории проекта!</b>\n\n"
      "Продолжайте играть, дожидаться новых обновлений и соревноваться за топ-1 мира, ведь теперь перед вами полностью открыта сфера соревнований за эксклюзивные награды!"
     )
     cursor.execute("UPDATE users SET total_progress = 100 WHERE user_id = ?", (user_id,))
     db.commit()
     await callback.message.answer(text)
    elif total_before == full_coll and total_after == full_coll + 1:
     text = (
      f"<b>{escape(nickname)}</b>, вы собрали <b>абсолютно полную коллекцию Джо Байденов</b> из <b>11 карт</b>! Теперь вы официально прошли <b>Joe Biden Cards и ваш общий достигнутый <b>прогресс равен 100%</b>!\n\n"
      "Поскольку бот активно обновляется и выходят новые карты, с целью баланса мы не можем выдать вам какую-либо награду, но знайте, <b>ваше имя</b> уже записано в <b>истории проекта!</b>\n\n"
      "Продолжайте играть, дожидаться новых обновлений и соревноваться за топ-1 мира!"
     )
     cursor.execute("UPDATE users SET total_progress = 100 WHERE user_id = ?", (user_id,))
     db.commit()
     await callback.message.answer(text)
    if type == "accumulations":
     cursor.execute("UPDATE users SET last_card_time = ? WHERE user_id = ?", (opening_time_before, user_id))
     db.commit()
    await callback.answer()
    break
def prefixes_selection(id: int):
 cursor.execute("SELECT user_id FROM users WHERE user_id NOT IN (?, ?) ORDER BY xp DESC LIMIT 3",(dev_id, dev_mini_id))
 rows = cursor.fetchall()
 top_ids = [r[0] for r in rows]
 while len(top_ids) < 3:
  top_ids.append(0)
 index = 1
 status = ""
 if id in (dev_id, dev_mini_id):
  status = prefixes.get(1)
 else:
  for i in top_ids:
   if id == i:
    status = prefixes.get(index + 1)
    break
   index += 1
 return status
async def market_purchase(callback: CallbackQuery, cost: int, product_quantity: int, product_name: str, is_one_time: bool):
 global season, season_start, season_end, season_desc, season_duration
 left_before_s_end = season_end - time.time()
 user_id = callback.from_user.id
 cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 xp = row[0] if row else 0
 name_in_text = "Обычных" if product_name == "fpacks" else "Расширенных"
 if 86400 >= left_before_s_end > 0:
  if is_one_time == True:
   cursor.execute("SELECT purchased_special_action FROM users WHERE user_id = ?", (user_id,))
   row = cursor.fetchone()
   did_purchase = row[0] if row else 0
   if did_purchase == 1:
    purchase_succeed = False
   else:
    purchase_succeed = True
  elif is_one_time == False:
   purchase_succeed = True
  if purchase_succeed == True:
   if xp >= cost:
    cursor.execute(f"UPDATE users SET xp = xp - ?, {product_name} = {product_name} + ? WHERE user_id = ?", (cost, product_quantity, user_id))
    db.commit()
    text = f"Вы успешно приобрели <b>x{product_quantity} {name_in_text} Наборов Карт</b> за {cost} XP"
    await callback.message.answer(text)
   else:
    text = "Недостаточно XP для покупки. Попробуйте позже."
    await callback.message.answer(text)
  else:
   text = f"Вы уже приобрели акцию <b>x{product_quantity} {name_in_text}</b> за <b>{cost}</b>"
   await callback.answer()
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await callback.message.answer(text)
  await callback.answer()
async def opening_per_time_setting(callback: CallbackQuery, change_to: int):
 user_id = callback.from_user.id
 cursor.execute("UPDATE settings SET openings_per_time = ? WHERE user_id = ?", (change_to, user_id))
 db.commit()
 noun = "карте" if change_to == 1 else "карты"
 if noun == "карты" and change_to == 5:
  noun = "карт"
 text = f"Вы успешно изменили эту настройку. Теперь при открытии наборов из запасов вы всегда будете открывать по {change_to} {noun} за раз."
 opening_per_time_back_to_settings = InlineKeyboardBuilder() # Возможность выйти после смены настройки
 opening_per_time_back_to_settings.button(text="Назад", callback_data="back_to_settings")
 await callback.message.edit_text(text=text, reply_markup=opening_per_time_back_to_settings.as_markup())
 await callback.answer()
async def showing_global_achs_by_card(callback: CallbackQuery, card_name: str):
 pack_name = "Обычный набор" if card_name in ("sigma", "diver", "sixseven") else "Расширенный набор"
 achievement_name = "Тираж Сигм" if card_name == "sigma" else "Тираж Водолазов" if card_name == "diver" else "Тираж Сикс Севенов" if card_name == "sixseven" else "Тираж Финальных Боссов" if card_name == "finalboss" else "Тираж Троллфейсов" if card_name == "trollface" else "Тираж .exe" if card_name == "exe" else ""
 card_id = 5 if card_name == "sigma" else 1 if card_name == "diver" else 2 if card_name == "sixseven" else 11 if card_name == "finalboss" else 10 if card_name == "trollface" else 9 if card_name == "exe" else 0
 text = (
  "<b>🏆 ГЛОБАЛЬНЫЕ ДОСТИЖЕНИЯ</b>\n\n"
  f"<blockquote>Фильтр: {pack_name} / {achievement_name}</blockquote>\n\n"
 )
 cursor.execute("SELECT reward_xp, reward_indicator, status, reward_stage FROM global_rewards WHERE id = 1 AND reward_name = ?", (card_name + "_cards",))
 rows = cursor.fetchall()
 cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id NOT IN (?, ?) AND card_id = ?", (dev_id, dev_mini_id, card_id))
 res = cursor.fetchone()[0]
 dictictictict = {}
 name_of_especially_this_keyboard_just_for_fun = "global_achievements_" + card_name
 dictictictict[name_of_especially_this_keyboard_just_for_fun] = InlineKeyboardBuilder()
 callback_data = "global_achs_by_fpacks" if card_name in ("sigma", "diver", "sixseven") else "global_achs_by_spacks"
 dictictictict[name_of_especially_this_keyboard_just_for_fun].button(text="Назад", callback_data=callback_data)
 if rows:
  for row in rows:
   reward_xp, reward_indicator, status, reward_stage = row
   quantity = res if status == 0 else reward_indicator
   quantity = quantity if quantity != None else 0
   text += (
    f"<b>{achievement_name} —  Уровень {reward_stage}</b>\n"
    f"<blockquote>Прогресс: {quantity}/{reward_indicator}\n"
    f"Полная награда: {reward_xp} XP</blockquote>\n\n"
   )
 else:
  text = "Пока что этот раздел <b>пуст</b>, вернитесь позже."
 await callback.message.edit_text(text=text, reply_markup=dictictictict[name_of_especially_this_keyboard_just_for_fun].as_markup())
 await callback.answer()

async def setup_v0_1_4(): # СЕТАП ДЛЯ v0.1.4
 await bot.send_message(chat_id=dev_id, text="Запуск setup v0.1.4...")
 cursor.execute("INSERT OR IGNORE INTO settings (user_id) SELECT user_id FROM users")
 db.commit()
 alters = ["ALTER TABLE users ADD COLUMN pack_stage INTEGER DEFAULT 1","ALTER TABLE users ADD COLUMN fpack_unlocked_cards INTEGER DEFAULT 0","ALTER TABLE users ADD COLUMN spack_unlocked_cards INTEGER DEFAULT 0","ALTER TABLE users ADD COLUMN fpack_progress INTEGER DEFAULT 0","ALTER TABLE users ADD COLUMN spack_progress INTEGER DEFAULT 0","ALTER TABLE users ADD COLUMN total_progress INTEGER DEFAULT 0","ALTER TABLE users ADD COLUMN purchased_special_action INTEGER DEFAULT 0","ALTER TABLE settings ADD COLUMN showing_my_profile INTEGER DEFAULT 1"]
 for sql in alters:
  try: cursor.execute(sql)
  except sqlite3.OperationalError: pass
 db.commit()
 cursor.execute("SELECT full_name, purchased_special_action, user_id, fpack_unlocked_cards, spack_unlocked_cards, total_progress, spack_progress FROM users")
 rows = cursor.fetchall()
 text = "📊 Список пользователей, приобретших акцию <b>x25 Обычных Наборов Карт за 260 XP</b>\n\n"
 for row in rows:
  full_name, purchased, uid, f_unlocked, s_unlocked, t_progress, s_progress = row or (None,0,None,0,0,0)
  status = "Приобрёл ✅" if purchased == 1 else "Не приобрёл ❌"
  text += f"{escape(full_name or 'Anon')} — {status}\n"
  if t_progress >= 50:
   cursor.execute("UPDATE users SET spack_progress = spack_unlocked_cards * 20 WHERE user_id = ?", (uid,))
  cursor.execute("UPDATE users SET total_progress = (fpack_unlocked_cards + spack_unlocked_cards) * 10 WHERE user_id = ?", (uid,))
  if purchased == 1 and get_user_card_count(uid, 6) > 0:
   if s_unlocked == ((f_unlocked + s_unlocked) * 11) + 11:
    cursor.execute("UPDATE users SET total_progress = total_progress - 11 WHERE user_id = ?", (uid,))
 try: await bot.send_message(chat_id=dev_id, text=text)
 except: pass
 print(f"Отчёт о покупках акции ({len(rows)} пользователей)")
 cursor.execute("UPDATE users SET purchased_special_action = 0")
 db.commit()
 cursor.execute("PRAGMA table_info(season_info)")
 cols = [r[1] for r in cursor.fetchall()]
 if "season" not in cols:
  try: cursor.execute("ALTER TABLE season_info ADD COLUMN season INTEGER")
  except: pass
 if "winner" not in cols:
  try: cursor.execute("ALTER TABLE season_info RENAME COLUMN winner_s0 TO winner")
  except: pass
  try: cursor.execute("ALTER TABLE season_info ADD COLUMN winner TEXT")
  except: pass
 cursor.execute("SELECT COUNT(*) FROM season_info")
 if cursor.fetchone()[0] == 0:
  cursor.executemany("INSERT INTO season_info (season, winner) VALUES (?, NULL)",[(0,),(1,),(2,)])
  cursor.execute("UPDATE season_info SET winner = 'cwendyzz' WHERE season = 0")
  cursor.execute("UPDATE season_info SET winner = 'Mᴇ Cʀᴀꜰᴛ♡' WHERE season = 1")
 db.commit()
 cursor.execute("DROP TABLE IF EXISTS global_rewards")
 db.commit()
 cursor.execute("""CREATE TABLE IF NOT EXISTS global_rewards (reward_name TEXT NOT NULL,reward_indicator INTEGER NOT NULL,reward_xp INTEGER NOT NULL,reward_stage INTEGER NOT NULL,status INTEGER DEFAULT 0 NOT NULL,id INTEGER DEFAULT 1 NOT NULL,CONSTRAINT status_check CHECK (status IN (0, 1)),CONSTRAINT stage_check CHECK (reward_stage IN (1, 2, 3, 4, 5)),UNIQUE(id, reward_name, reward_stage))""")
 db.commit()
 cursor.execute("SELECT COUNT(*) FROM global_rewards")
 if cursor.fetchone()[0] == 0:
  rewards_data = [('total_cards',100,50,1,1),('total_cards',300,150,2,1),('total_cards',500,250,3,1),('total_cards',1000,750,4,0),('sigma_cards',5,200,1,1),('sigma_cards',10,500,2,0),('diver_cards',10,100,1,1),('diver_cards',25,250,2,1),('diver_cards',50,500,3,0),('sixseven_cards',25,50,1,1),('sixseven_cards',50,100,2,1),('sixseven_cards',100,300,3,0),('finalboss_cards',5,375,1,0),('trollface_cards',10,200,1,0),('trollface_cards',25,500,2,0),('exe_cards',25,125,1,0),('exe_cards',50,250,2,0)]
  cursor.executemany("INSERT INTO global_rewards (reward_name,reward_indicator,reward_xp,reward_stage,status) VALUES (?,?,?,?,?)", rewards_data)
  db.commit()
 cursor.execute("CREATE TABLE IF NOT EXISTS useful_info ([максим пидорас 6767] TEXT)")
 cursor.execute("INSERT OR IGNORE INTO useful_info ([максим пидорас 6767]) VALUES ('да')")
 db.commit()
 cursor.execute("SELECT [максим пидорас 6767] FROM useful_info")
 row = cursor.fetchone()
 if row and row[0] == 'да':
  try:
   await bot.send_message(chat_id=dev2_id,text="<b>⏳ Достаю информацию из БД...</b>\n\nОпираясь на данные из файла <b>archived_database.db</b>, сообщаю, что Максим — пидорас 6767:\n\n<code>максим пидорас 6767 = 'да'</code>")
   await bot.send_message(chat_id=dev_id,text="✅ Максим успешно получил ваше сообщение.")
  except: pass
 cursor.execute("INSERT OR IGNORE INTO season_info (season, winner) VALUES (0, 'cwendyzz'), (1, 'Mᴇ Cʀᴀꜰᴛ♡'), (2, NULL)")
 cursor.execute("UPDATE season_info SET winner = 'cwendyzz' WHERE season = 0 AND (winner IS NULL OR winner = '')")
 cursor.execute("UPDATE season_info SET winner = 'Mᴇ Cʀᴀꜰᴛ♡' WHERE season = 1 AND (winner IS NULL OR winner = '')")
 cursor.execute("UPDATE season_info SET season = 0 WHERE winner = 'cwendyzz'")
 cursor.execute("UPDATE season_info SET season = 1 WHERE winner = 'Mᴇ Cʀᴀꜰᴛ♡';")
 cursor.execute("UPDATE card_stats SET first_unlocked = '𔓕 ⊹ ◜⛩️◞  ꩜ すばらしい ꩜ ◜🪽◞ `⌁ ' WHERE card_id = 10")
 db.commit()
 await bot.send_message(chat_id=dev_id, text="Setup v0.1.4 полностью завершён")

async def global_rewards_dispatcher(): # ДИСПЕТЧЕР ОБЩИХ ДОСТИЖЕНИЙ И НАГРАД v0.1.3+
 reward_card_map = {
  "sigma_cards": 5,
  "diver_cards": 1,
  "sixseven_cards": 2,
  "finalboss_cards": 11,
  "trollface_cards": 10,
  "exe_cards": 9
 }
 while True:
  cursor.execute("SELECT reward_name, reward_indicator, reward_xp, reward_stage FROM global_rewards WHERE status = 0 AND id = 1 ORDER BY reward_name, reward_stage")
  rewards = cursor.fetchall()
  for reward_name, reward_indicator, reward_xp, reward_stage in rewards:
   total_reward = reward_name == "total_cards"
   if not total_reward:
    card_id = reward_card_map.get(reward_name)
   if total_reward:
    cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
    name = "Общий Тираж"
   else:
    cursor.execute("SELECT SUM(count) FROM user_cards WHERE card_id = ? AND user_id NOT IN (?, ?)", (card_id, dev_id, dev_mini_id))
   row = cursor.fetchone()
   global_count = row[0] if row and row[0] else 0
   if not total_reward:
    card_name = card_names.get(card_id, "???")
    if card_name  == "Джо Байден.exe":
     card_name = "exe"
    elif card_name in ("Сигма Джо Байден", "Водолаз Джо Байден", "Сикс Севен Джо Байден", "Финальный Босс Джо Байден", "Троллфейс Джо Байден"):
     card_name = card_name.replace(" Джо Байден", "")
    if card_name == "Финальный Босс":
     card_name = "Финальных Боссов"
    elif card_name.endswith(("н", "з", "с")):
     card_name += "ов"
    elif card_name.endswith("а"):
     card_name = card_name[:-1]
    name = f"Тираж {card_name}"
   if global_count < reward_indicator:
    continue
   cursor.execute("UPDATE global_rewards SET status = 1 WHERE reward_name = ? AND reward_stage = ? AND status = 0", (reward_name, reward_stage))
   if cursor.rowcount == 0:
    continue
   db.commit()
   goal_name = f"{name} — Уровень {reward_stage}"
   cursor.execute("SELECT user_id, full_name, total_cards FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
   users = cursor.fetchall()
   for user_id, nickname, total_cards in users:
    if total_reward:
     player_count = total_cards or 0
    else:
     cursor.execute("SELECT count FROM user_cards WHERE user_id = ? AND card_id = ?", (user_id, card_id))
     row = cursor.fetchone()
     player_count = row[0] if row else 0
    goal_percentage = min(1, player_count / global_count) if global_count else 0
    earned_xp = int(reward_xp * goal_percentage)
    if earned_xp <= 0:
     continue
    text = f"{escape(nickname)}, поздравляем с выполнением глобального достижения <b>{goal_name}</b>! Вам начислено <b>{earned_xp} XP</b>. Вы смогли набрать <b>{int(goal_percentage * 100)}%</b> от общей цели, собрав <b>{player_count}</b> из <b>{reward_indicator}</b> необходимых карт!"
    if goal_percentage != 0:
     try:
      await bot.send_message(chat_id=user_id, text=text)
      cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (earned_xp, user_id))
     except TelegramAPIError as e:
      print(f"Ошибка при отправке награды для {user_id}: {e}")
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
     text = "🛍 Остался 1 день до окончания сезона, поэтому временный маркет возвращается!\n\nВ нём доступны акции на <b>Обычные</b> и <b>Расширенные Наборы Карт</b> со скидками до <b>-17%</b>, а также особая одноразовая акция для ускорения прогресса глобальных достижений.\n\nЗакупайтесь или изучайте полный список товаров с помощью команды /market"
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
     cursor.execute("UPDATE season_info SET winner = ? WHERE season = 2", (user[0],))
     db.commit()
     if count_after == full_coll + 1 and count_before == full_coll:
      text = (
       f"<b>{escape(user[0])}</b>, вы собрали <b>абсолютно полную коллекцию Джо Байденов</b> из <b>11 карт</b>! Теперь вы официально прошли <b>Joe Biden Cards и ваш общий достигнутый <b>прогресс равен 100%</b>!\n\n"
       "Поскольку бот активно обновляется и выходят новые карты, с целью баланса мы не можем выдать вам какую-либо награду, но знайте, <b>ваше имя</b> уже записано в <b>истории проекта!</b>\n\n"
       "Продолжайте играть, дожидаться новых обновлений и соревноваться за топ-1 мира!"
      )
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

@dp.message(Command("settings_info")) # АДМИН КОМАНДА v0.1.4+
async def showing_settings_info_from_db(message: types.Message):
 user_id = message.from_user.id
 if user_id not in [dev_id, dev2_id, dev_mini_id]:
  text = "У вас недостаточно прав для использования команды /settings_info."
  await message.answer(text)
  return
 cursor.execute("SELECT user_id FROM users")
 ids = [row[0] for row in cursor.fetchall()]
 text = "<b>ИНФОРМАЦИЯ О НАСТРОЙКАХ</b>\n\n"
 for id in ids:
  cursor.execute("SELECT openings_per_time, showing_prefixes, showing_my_profile FROM settings WHERE user_id = ?", (id,))
  row = cursor.fetchone()
  oppeti, shpr, shmypr = row if row else (0, 0, 0)
  cursor.execute("SELECT username FROM users WHERE user_id = ?", (id,))
  row = cursor.fetchone()
  us = row[0] if row else 0
  shpr = "✅" if shpr == 1 else "❌"
  shmypr = "✅" if shmypr == 1 else "❌"
  link_formatting_start = f"<a href='https://t.me/{us}'>" if us != "Anon" else f"<a href='tg://user?id={id}'>"
  link_formatting_end = "</a>"
  text += (
   f"<b>{link_formatting_start}ID: {id}{link_formatting_end}</b>\n"
   f"<blockquote>Открытие карт за раз: {oppeti}\n"
   f"Отображение префиксов: {shpr}\n"
   f"Отображение моего профиля: {shmypr}</blockquote>\n\n"
  )
 await message.answer(text, disable_web_page_preview=True)

@dp.message(Command("all_info"))  # АДМИН КОМАНДА v0.1.1.3+
async def showing_db_info(message: types.Message):
 user_id = message.from_user.id
 if message.from_user.id not in [dev_id, dev2_id, dev_mini_id]:
  text = "У вас недостаточно прав для использования команды /all_info."
  await message.answer(text)
  return
 cursor.execute("SELECT user_id FROM users")
 ids = [row[0] for row in cursor.fetchall()]
 text = "<b>ВСЯ ИНФОРМАЦИЯ</b>\n"
 for id in ids:
  cursor.execute("SELECT full_name, xp, total_cards, unlocked_cards, fpacks, last_card_time, total_progress, fpack_progress, spack_progress, fpack_unlocked_cards, spack_unlocked_cards, spacks, pack_stage, username FROM users WHERE user_id = ?", (id,))
  row = cursor.fetchone()
  full_name, xp, total_cards, unlocked_cards, fpacks, last_card_time, total_progress, fpack_progress, spack_progress, fpack_unlocked_cards, spack_unlocked_cards, spacks, pack_stage, username = row if row else ("Anon", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  if pack_stage == 1:
   stg_progress = fpack_progress
  elif pack_stage == 2:
   stg_progress = spack_progress
  cursor.execute("SELECT showing_prefixes FROM settings WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  showing_prefixes = row[0] if row else 0
  if showing_prefixes == 1:
   status = prefixes_selection(id)
  else:
   status = ""
  text += (
   f"\n<b>{status}{escape(full_name)} — {id} | {xp} XP</b>\n"
   f"Стадия прохождения: {pack_stage} [{stg_progress}%]\n\n"
  )
  if get_user_card_count(id, 6) >= 1:
   text += (
    "Эксклюзивные:\n"
    f"<blockquote>Пожизненный Водолаз Джо Байден — x{get_user_card_count(id, 6)}</blockquote>\n"
   )
  if total_cards == 0:
   text += "<blockquote>Список карт данного игрока пуст\n"
  else:
   text += "Обычные:\n<blockquote>"
  for i in card_drop_diapazones.keys():
   card_name = card_names.get(i, f"Карта не найдена")
   if get_user_card_count(id, i) > 0:
    text += f"{card_name} — x{get_user_card_count(id, i)}\n"
  how_much_is_needed = full_coll if unlocked_cards <=9 and get_user_card_count(id, 6) == 0 else full_coll + 1
  text += f"</blockquote>\nВсего: {total_cards} карт | Открыто: {unlocked_cards}/{how_much_is_needed}"
  text += f"\nОбычные Наборы Карт: {fpacks}"
  text += f"\nРасширенные Наборы Карт: {spacks}"
  text += f"\nПоследнее открытие: {datetime.fromtimestamp(last_card_time).date()}"
  text += f"\nПроцент прохождения: {total_progress}%\n"
 cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 row = cursor.fetchone()
 total_count = row[0] if row and row[0] is not None else 0
 cursor.execute("SELECT SUM(xp) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 row = cursor.fetchone()
 total_xp = row[0] if row and row[0] is not None else 0
 text += f"\n<b>Всего: {total_count} карт | {total_xp} XP</b>"
 if len(text) >= 4096:
  part1 = text[:4096].replace("<b>", "").replace("</b>", "").replace("<blockquote>", "").replace("</blockquote>", "")
  part2 = text[4096:].replace("<b>", "").replace("</b>", "").replace("<blockquote>", "").replace("</blockquote>", "")
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
  "<b>⚡️ ОБНОВЛЕНИЕ v0.1.4 ВЫШЛО!</b>\n\n"
  "Новое:\n"
  "<blockquote>— Добавлена новая карта <b>Финальный Босс Джо Байден</b> с шансом 1% из <b>Расширенного набора</b>.\n"
  "— Переработана система глобальных достижений: весь интерфейс перенесён в новую команду <b>/achievements</b>. Теперь все достижения удобно просматриваются с помощью фильтров, навигации и инлайн-кнопок.\n"
  "— Добавлено 6 новых достижений, включая <b>«Общий Тираж — Уровень 4»</b> и первые уровни тиража для карт <b>Расширенного Набора</b>.\n"
  "— В лидербордах ники игроков теперь являются кликабельными ссылками на их Telegram-профили.\n"
  "— Полностью переработано меню настроек: теперь /settings использует удобное инлайн-меню с мгновенным применением изменений, похожее на /achievements.\n"
  "— Добавлена новая настройка <b>«Отображение моего профиля»</b>, а также опция открытия 5 наборов за раз.\n"
  "— Добавлена административная команда <b>/settings_info</b> для просмотра личных настроек игроков.</blockquote>\n\n"
  "QoL:\n"
  "<blockquote>— Актуализированы текстовые напоминания — названия карт и наборов теперь соответствуют стадии игрока.\n"
  "— Новые показатели в лидерборде достижений.\n"
  "— Команда /card теперь сразу показывает набор, соответствующий текущей стадии игрока.\n"
  "— Неизвестные карты в предпросмотре набора теперь отображаются как <b>???</b>.</blockquote>\n\n"
  "Изменения баланса:\n"
  "<blockquote>— Увеличены награды за <b>«Тираж Сигма — Уровень 2»</b> (400 → 500 XP) и <b>«Тираж Сикс Севен — Уровень 3»</b> (200 → 300 XP)\n"
  "— Уменьшен шанс выпадения <b>Троллфейса Джо Байдена</b> (5% → 4%).</blockquote>\n\n"
  "Исправления багов:\n"
  "<blockquote>— Исправлен баг, из-за которого подсчет общего прогресса у владельцев <b>Пожизненного Водолаза Джо Байдена</b> происходил неверно.\n"
  "— Исправлен визуальный баг, из-за которого у новых игроков стадия была равна 0.\n"
  "— Исправлен баг, из-за которого игрок, первым открывший <b>Троллфейса Джо Байдена</b>, не отображался в лидерборде достижений.\n"
  "— Исправлено множество мелких визуальных и функциональных ошибок.</blockquote>\n\n"
  "Техническое:\n"
  "<blockquote>— Значительная оптимизация кода.\n"
  "— Миграция базы данных.</blockquote>\n\n"
  "В честь выхода обновления <b>КД всех наборов</b> уменьшен на <b>20%</b> до этого воскресенья."
 )
 cursor.execute("SELECT user_id FROM users")
 rows = cursor.fetchall()
 count = 0
 if int(time.time()) < 1782464400:
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
  print("Столбец collected_gift уже существует.")
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
  text = "⏱️ Срок получения подарка <b>истек</b>. Его действие закончилось <b>19 июня в 15:00</b>."
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
 left_before_s_end = season_end - time.time()
 if 86400 >= left_before_s_end > 0:
  h = int(left_before_s_end // 3600)
  m = int((left_before_s_end % 3600) // 60)
  market_purchase_selection = InlineKeyboardBuilder() # Выбор покупки во временном маркете
  text = (
   f"<b>🛍 ВРЕМЕННЫЙ МАРКЕТ</b> — до закрытия {h}ч {m}м\n\n"
   "<blockquote>Здесь вы можете обменять ваш опыт в конце сезона на наборы карт, чтобы поохотиться за новыми добавленными редкими картами или получить фору в начале следующего сезона.</blockquote>\n\n"
   "Доступные акции:\n"
   "<blockquote>🃏 <b>x1 Обычный Набор Карт</b> — 15 XP\n"
   "🃏 <b>x10 Обычных Наборов Карт</b> — <s>150</s> 125 XP (-17%)"
  )
  market_purchase_selection.button(text="x1 Обычный Набор Карт", callback_data="one_fpack_purchase")
  market_purchase_selection.button(text="x10 Обычных Наборов Карт", callback_data="ten_fpacks_purchase")
  if pack_stage > 1:
   text += (
    "\n🃏 <b>x1 Расширенный Набор Карт</b> — 25 XP"
    "\n🃏 <b>x10 Расширенных Наборов Карт</b> — <s>250</s> 210 XP (-16%)"
   )
   market_purchase_selection.button(text="x1 Расширенный Набор Карт", callback_data="one_spack_purchase")
   market_purchase_selection.button(text="x10 Расширенных Наборов Карт", callback_data="ten_spacks_purchase")
  text += "</blockquote>"
  text += "\n\nВыберите акцию для покупки"
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
 await market_purchase(callback, 15, 1, "fpacks", False)

@dp.callback_query(F.data == "ten_fpacks_purchase")
async def processing_ten_fpacks_purchase(callback: CallbackQuery):
 await market_purchase(callback, 125, 10, "fpacks", False)

@dp.callback_query(F.data == "one_spack_purchase")
async def processing_one_spack_purchase(callback: CallbackQuery):
 await market_purchase(callback, 25, 1, "spacks", False)

@dp.callback_query(F.data == "ten_spacks_purchase")
async def processing_ten_spacks_purchase(callback: CallbackQuery):
 await market_purchase(callback, 210, 10, "spacks", False)

@dp.callback_query(F.data == "global_achs_boost_purchase")
async def processing_global_achs_boost_purchase(callback: CallbackQuery):
 await market_purchase(callback, 260, 25, "fpacks", True)

@dp.message(Command("leaderboard")) # СПИСОК ЛИДЕРОВ v0.1+
async def show_leaderboard(message: types.Message):
 text = "Выберите режим лидерборда для его просмотра:"
 await message.answer(text, reply_markup=leaderboard_mode_selection.as_markup())

@dp.callback_query(F.data == "season_leaderboard") # Сезонный лидерборд
async def handle_season_leaderboard(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 cursor.execute("SELECT full_name, xp, user_id, username FROM users WHERE user_id NOT IN (?, ?) ORDER BY XP DESC LIMIT 5", (dev_id, dev_mini_id))
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
  cursor.execute("SELECT showing_my_profile FROM settings WHERE user_id = ?", (user[2],))
  show_my_tg_profile = cursor.fetchone()[0]
  link_start = f"<a href='https://t.me/{user[3]}'>" if show_my_tg_profile == 1 else ""
  link_end = "</a>" if show_my_tg_profile == 1 else ""
  results += f"{link_start}{medal}{dot} {escape(user[0])} — {user[1]} XP{link_end}\n"
  rank += 1
 cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 row = cursor.fetchone()
 total_cards = row[0] if row and row[0] else 0
 results += f"\nВсего карточек существует: {total_cards}\n\n"
 await callback.message.answer(results, disable_web_page_preview=True) 
 await callback.answer()

@dp.callback_query(F.data == "records_leaderboard")
async def handle_records_leaderboard(callback: CallbackQuery):
 cursor.execute("SELECT full_name, username FROM users WHERE fpack_unlocked_cards = 5 AND spack_unlocked_cards = 5 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with10 = cursor.fetchall()
 cursor.execute("SELECT full_name, username FROM users WHERE unlocked_cards = ? AND user_id NOT IN (?, ?)", (full_coll, dev_id, dev_mini_id))
 users_with11 = cursor.fetchall()
 cursor.execute("SELECT COUNT(*) FROM users WHERE fpack_unlocked_cards = 5 AND spack_unlocked_cards = 5 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with_full_coll10 = cursor.fetchone()[0] or 0
 cursor.execute("SELECT COUNT(*) FROM users WHERE unlocked_cards = ? AND user_id NOT IN (?, ?)", (full_coll + 1, dev_id, dev_mini_id))
 users_with_full_coll11 = cursor.fetchone()[0] or 0

 results = "<b>🏆 ЛИДЕРБОРД ДОСТИЖЕНИЙ</b>"

 if users_with10:
  names_10 = [f"<a href='https://t.me/{u[1]}'>{escape(u[0])}</a>" for u in users_with10]
  results += "\n\nПолная коллекция (10/10):\n<blockquote>" + ", ".join(names_10) + f"</blockquote>\nВсего игроков: {users_with_full_coll10}"
 if users_with11:
  names_11 = [f"<a href='https://t.me/{u[1]}'>{escape(u[0])}</a>" for u in users_with11]
  results += "\n\nПолная коллекция (11/11):\n<blockquote>" + ", ".join(names_11) + f"</blockquote>\nВсего игроков: {users_with_full_coll11}"

 cursor.execute("SELECT winner, season FROM season_info WHERE winner IS NOT NULL ORDER BY season")
 winners = cursor.fetchall()
 if winners:
  results += "\n\nПобедители сезонов:\n<blockquote>"
  seen = set()
  for w_name, w_season in winners:
   if not w_name or w_name in seen: continue
   seen.add(w_name)
   try:
    w_season = int(w_season)
   except:
    w_season = -1
   if w_season == 0:
    season_text = "нулевого"
   elif w_season == 1:
    season_text = "первого"
   elif w_season == 2:
    season_text = "второго"
   else:
    season_text = "неизвестного"
   
   cursor.execute("SELECT user_id FROM users WHERE full_name = ?", (w_name,))
   row = cursor.fetchone()
   uid = row[0] if row else None
   link_start = link_end = ""
   if uid:
    cursor.execute("SELECT showing_my_profile FROM settings WHERE user_id = ?", (uid,))
    show_row = cursor.fetchone()
    show = show_row[0] if show_row else 0
    if show == 1:
     cursor.execute("SELECT username FROM users WHERE full_name = ?", (w_name,))
     us_row = cursor.fetchone()
     us = us_row[0] if us_row else None
     if us:
      link_start = f"<a href='https://t.me/{us}'>"
      link_end = "</a>"
   results += f"{link_start}{escape(w_name)}{link_end} — топ-1 мира {season_text} сезона\n"
  results += "</blockquote>"
 achievers = ['Victony Universal', 'Mᴇ Cʀᴀꜰᴛ♡', 'cwendyzz', 'Mᴇ Cʀᴀꜰᴛ♡', '𔓕 ⊹ ◜⛩️◞  ꩜ すばらしい ꩜ ◜🪽◞ `⌁']
 achievements = ['первый в мире <b>Открытый Обычный Набор</b> (23.04)', 'первый в мире <b>Открытый Расширенный Набор</b>', 'первая в мире <b>полная коллекция 4/4</b> (26.04)', 'первая в мире <b>полная коллекция 5/5</b> (08.06)', 'первая в мире <b>полная коллекция 9/9</b> (21.06)']
 results += "\n<b>АРХИВИРОВАННЫЕ ДОСТИЖЕНИЯ</b>\n\nПервооткрыватели:\n<blockquote>"
 for nickname, achievement in zip(achievers, achievements):
  cursor.execute("SELECT username, user_id FROM users WHERE full_name = ?", (nickname,))
  row = cursor.fetchone()
  us, idd = row if row else (None, 0)
  cursor.execute("SELECT showing_my_profile FROM settings WHERE user_id = ?", (idd,))
  row = cursor.fetchone()
  show = row[0] if row else 0
  link_start = f"<a href='https://t.me/{us}'>" if show == 1 and us else ""
  link_end = "</a>" if show == 1 and us else ""
  results += f"{link_start}{nickname}{link_end} — {achievement}\n"
 for i in card_drop_diapazones.keys():
  cursor.execute("SELECT first_unlocked FROM card_stats WHERE card_id = ?", (i,))
  row = cursor.fetchone()
  first = row[0] if row else None
  if not first: continue
  cursor.execute("SELECT user_id FROM users WHERE full_name = ?", (first,))
  row = cursor.fetchone()
  idd = row[0] if row else 0
  cursor.execute("SELECT showing_my_profile FROM settings WHERE user_id = ?", (idd,))
  row = cursor.fetchone()
  show = row[0] if row else 0
  cursor.execute("SELECT username FROM users WHERE user_id = ?", (idd,))
  us_row = cursor.fetchone()
  us = us_row[0] if us_row else None
  link_start = f"<a href='https://t.me/{us}'>" if show == 1 and us else ""
  link_end = "</a>" if show == 1 and us else ""
  results += f"{link_start}{escape(first)}{link_end} — первый в мире <b>{card_names.get(i)}</b> ({first_unlocked_date.get(i, '')})\n"
 results += "</blockquote>"

 await callback.message.answer(results, disable_web_page_preview=True)
 await callback.answer()

@dp.message(Command("achievements")) # КОМАНДА ГЛОБАЛЬНЫХ ДОСТИЖЕНИЙ v0.1.4+
async def handle_global_achievements(event: types.Message | CallbackQuery):
 cursor.execute("SELECT COUNT(*), SUM(reward_xp) FROM global_rewards WHERE status = 1")
 row = cursor.fetchone()
 completed_already, gave_away_already = row if row else (0, 0)
 text = (
 "<b>🏆 ГЛОБАЛЬНЫЕ ДОСТИЖЕНИЯ</b>\n\n"
 "<blockquote>Здесь вы можете просмотреть информацию о всех глобальных достижениях в боте или отследить их прогресс. Используйте навигацию в виде инлайн-кнопок, чтобы перейти к нужному разделу.</blockquote>\n\n"
 f"Всего выполнено: {completed_already}/17\n"
 f"Всего получено: {gave_away_already}/4650 XP\n\n"
 "Выберите фильтр для просмотра глобальных достижений."
 )
 global_achievements_inl = InlineKeyboardBuilder()
 global_achievements_inl.button(text="Общие", callback_data="global_achs_by_totals")
 global_achievements_inl.button(text="Обычный Набор Карт", callback_data="global_achs_by_fpacks")
 global_achievements_inl.button(text="Расширенный Набор Карт", callback_data="global_achs_by_spacks")
 global_achievements_inl.adjust(1)
 if isinstance (event, types.Message):
   await event.answer(text=text, reply_markup=global_achievements_inl.as_markup())
 elif isinstance (event, CallbackQuery):
   await event.message.edit_text(text=text, reply_markup=global_achievements_inl.as_markup())
   await event.answer()

@dp.callback_query(F.data == "global_achs_by_totals")
async def demonstrating_global_achs_by_totals(callback: CallbackQuery):
 text = (
  "<b>🏆 ГЛОБАЛЬНЫЕ ДОСТИЖЕНИЯ</b>\n"
  "<blockquote>Фильтр: Общий Тираж</blockquote>\n\n"
 )
 cursor.execute("SELECT reward_xp, reward_indicator, status, reward_stage FROM global_rewards WHERE id = 1 AND reward_name = 'total_cards'")
 rows = cursor.fetchall()
 cursor.execute("SELECT SUM(total_cards) FROM users WHERE user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 res = cursor.fetchone()[0]
 global_achievements_totals = InlineKeyboardBuilder()
 global_achievements_totals.button(text="Назад", callback_data="back_to_global_achs_main_menu")
 if rows:
  for row in rows:
   reward_xp, reward_indicator, status, reward_stage = row
   quantity = res if status == 0 else reward_indicator
   quantity = quantity if quantity != None else 0
   text += (
    f"<b>Общий Тираж —  Уровень {reward_stage}</b>\n"
    f"<blockquote>Прогресс: {quantity}/{reward_indicator}\n"
    f"Полная награда: {reward_xp} XP</blockquote>\n\n"
   )
 else:
  text = "Пока что этот раздел <b>пуст</b>, вернитесь позже."
 await callback.message.edit_text(text=text, reply_markup=global_achievements_totals.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "global_achs_by_fpacks")
async def demonstrating_global_achs_by_fpacks(callback: CallbackQuery):
 global_achievements_fpacks = InlineKeyboardBuilder()
 global_achievements_fpacks.button(text="Тираж Сигм", callback_data="global_achs_by_sigma")
 global_achievements_fpacks.button(text="Тираж Водолазов", callback_data="global_achs_by_diver")
 global_achievements_fpacks.button(text="Тираж Сикс Севен", callback_data="global_achs_by_sixseven")
 global_achievements_fpacks.button(text="Назад", callback_data="back_to_global_achs_main_menu")
 global_achievements_fpacks.adjust(1)
 cursor.execute("SELECT COUNT(*), SUM(reward_xp) FROM global_rewards WHERE id = 1 AND status = 1 AND reward_name IN ('sigma_cards', 'diver_cards', 'sixseven_cards')")
 row = cursor.fetchone()
 completed_already = row[0] if row else 0
 gave_away_already = row[1] if row is not None else 0
 text = (
 "<b>🏆 ГЛОБАЛЬНЫЕ ДОСТИЖЕНИЯ</b>\n"
 "<blockquote>Фильтр: Обычный набор карт</blockquote>\n\n"
 "Доступные опции:\n\n"
 "<b>Тираж Сигм — 2 уровня</b>\n"
 "<blockquote>Полная награда: 700 XP</blockquote>\n\n"
 "<b>Тираж Водолазов — 3 уровня</b>\n"
 "<blockquote>Полная награда: 850 XP</blockquote>\n\n"
 "<b>Тираж Сикс Севен — 3 уровня</b>\n"
 "<blockquote>Полная награда: 450 XP</blockquote>\n\n"
 f"Выполнено: {completed_already}/8 \n"
 f"Получено: {gave_away_already}/2000 XP\n\n"
 "Выберите следующий фильтр для просмотра достижений конкретной карты"
 )
 await callback.message.edit_text(text=text, reply_markup=global_achievements_fpacks.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "global_achs_by_spacks")
async def demonstrating_global_achs_by_spacks(callback: CallbackQuery):
 global_achievements_spacks = InlineKeyboardBuilder()
 global_achievements_spacks.button(text="Тираж Финальных Боссов", callback_data="global_achs_by_finalboss")
 global_achievements_spacks.button(text="Тираж Троллфейсов", callback_data="global_achs_by_trollface")
 global_achievements_spacks.button(text="Тираж .exe", callback_data="global_achs_by_.exe")
 global_achievements_spacks.button(text="Назад", callback_data="back_to_global_achs_main_menu")
 global_achievements_spacks.adjust(1)
 cursor.execute("SELECT COUNT(*), SUM(reward_xp) FROM global_rewards WHERE id = 1 AND status = 1 AND reward_name IN ('finalboss_cards', 'trollface_cards', 'exe_cards')")
 row = cursor.fetchone()
 completed_already = row[0] if row else 0
 gave_away_already = row[1] if row is not None else 0
 if gave_away_already in (None, "None"):
  gave_away_already = 0
 text = (
 "<b>🏆 ГЛОБАЛЬНЫЕ ДОСТИЖЕНИЯ</b>\n"
 "<blockquote>Фильтр: Расширенный набор карт</blockquote>\n\n"
 "Доступные опции:\n\n"
 "<b>Тираж Финальных Боссов — 1 уровень</b>\n"
 "<blockquote>Полная награда: 375 XP</blockquote>\n\n"
 "<b>Тираж Троллфейсов — 2 уровня</b>\n"
 "<blockquote>Полная награда: 700 XP</blockquote>\n\n"
 "<b>Тираж .exe — 2 уровня</b>\n"
 "<blockquote>Полная награда: 375 XP</blockquote>\n\n"
 f"Выполнено: {completed_already}/5 \n"
 f"Получено: {gave_away_already}/1450 XP\n\n"
 "Выберите следующий фильтр для просмотра достижений конкретной карты"
 )
 await callback.message.edit_text(text=text, reply_markup=global_achievements_spacks.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "global_achs_by_finalboss")
async def demonstrating_global_achs_by_finalboss(callback: CallbackQuery):
 await showing_global_achs_by_card(callback, "finalboss")

@dp.callback_query(F.data == "global_achs_by_trollface")
async def demonstrating_global_achs_by_trollface(callback: CallbackQuery):
 await showing_global_achs_by_card(callback, "trollface")

@dp.callback_query(F.data == "global_achs_by_.exe")
async def demonstrating_global_achs_by_exe(callback: CallbackQuery):
 await showing_global_achs_by_card(callback, "exe")

@dp.callback_query(F.data == "global_achs_by_sigma")
async def demonstrating_global_achs_by_sigma(callback: CallbackQuery):
 await showing_global_achs_by_card(callback, "sigma")

@dp.callback_query(F.data == "global_achs_by_diver")
async def demonstrating_global_achs_by_diver(callback: CallbackQuery):
 await showing_global_achs_by_card(callback, "diver")

@dp.callback_query(F.data == "global_achs_by_sixseven")
async def demonstrating_global_achs_by_sixseven(callback: CallbackQuery):
 await showing_global_achs_by_card(callback, "sixseven")

@dp.callback_query(F.data == "back_to_global_achs_main_menu")
async def backing_to_main_menu_of_global_achievements(callback: CallbackQuery):
 await handle_global_achievements(callback)

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
 "Актуальная версия: v0.1.4"
 )
 await message.answer(text=text, disable_web_page_preview=True)

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
 if showing_prefixes ==  1:
  status = prefixes_selection(user_id)
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
 else:
  text += "\n\n<blockquote>Список карт данного игрока пуст\n"
 for i in card_drop_diapazones.keys():
  if get_user_card_count(user_id, i) > 0:
   text += f"{card_names.get(i, "")} — x{get_user_card_count(user_id, i)}\n"
 how_much_is_needed = 10 if info[2] <= 10 and get_user_card_count(user_id, 6) == 0 else 11
 text += (
  f"</blockquote>\nВсего: {info[3]} | {info[2]}/{how_much_is_needed} открыто\n"
  f"Обычные наборы карт: {info[4]}\n"
  f"Расширенные наборы карт: {info[5]}\n"
  f"Процент прохождения: {info[6]}%"
 )
 await message.answer(text)

@dp.message(Command("card")) # КОМАНДА ДЛЯ ОТКРЫТИЯ КАРТЫ v0.1+
async def deciding_which_pack_to_show(message: types.Message):
 user_id = message.from_user.id
 cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 stg = row[0] if row else 0
 if stg == 1:
  await handling_fpack_info(message)
 elif stg == 2:
  await handling_spack_info(message)
 
async def handling_fpack_info(event: types.Message | types.CallbackQuery):
 user_id = event.from_user.id
 nickname = event.from_user.full_name
 username = event.from_user.username
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
 )
 fpack_cards = [5, 4, 3, 2, 1]
 for i in card_drop_diapazones.keys():
  if i in fpack_cards:
   if get_user_card_count(user_id, i) >= 1:
    text += f"{card_names.get(i, "Неизвестная карта")} — {card_chances.get(i, 0)}%\n"
   else:
    text += f"??? — {card_chances.get(i, 0)}%\n"
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
  minutes = int(current_left // 60)
  seconds = int(current_left % 60)
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
  minutes = int(current_left // 60)
  seconds = int(current_left % 60)
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
async def handling_spack_info(event: types.Message | types.CallbackQuery):
 user_id = event.from_user.id
 nickname = event.from_user.full_name
 username = event.from_user.username
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
 )
 spack_cards = [11, 10, 9, 8, 7]
 for i in card_drop_diapazones.keys():
  if i in spack_cards:
   if get_user_card_count(user_id, i) >= 1:
    text += f"{card_names.get(i, "Неизвестная карта")} — {card_chances.get(i, 0)}%\n"
   else:
    text += f"??? — {card_chances.get(i, 0)}%\n"
 card_pack_selection = InlineKeyboardBuilder() # Выбор действия при просмотре информации набора карт
 if stg >= 2:
  card_pack_selection.button(text="Открыть", callback_data="opening_spack_method")
 card_pack_selection.button(text="Предыдущий набор", callback_data="prev_pack")
 card_pack_selection.adjust(1)
 if isinstance (event, types.Message):
  await event.answer(text=text, reply_markup=card_pack_selection.as_markup())
 elif isinstance (event, CallbackQuery):
  await event.message.edit_text(text=text, reply_markup=card_pack_selection.as_markup())
  await event.answer()

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
   cursor.execute("SELECT pack_stage FROM users WHERE user_id = ?", (user_id,))
   res = cursor.fetchone()
   stg = row[0] if row else 0
   pack_name = "обычного набора карточек" if stg == 1 else "расширенного набора карточек"
   cd_first = 1800 if stg == 1 else 3600
   card2441 = "Водолаза" if stg == 1 else "Троллфейса"
   card2442 = "Сигму" if stg == 1 else "Финального Босса"
   card_slogan244 = "Не хочешь оказаться на дне как Водолаз?" if stg == 1 else "Не хочешь оказаться в банкротстве как Троллфейс?"
   card245 = "Сигма Джо Байден" if stg == 1 else "Финальный Босс Джо Байден"
   card83 = "Сигма" if stg == 1 else "Финальный Босс"
   card231 = "Сикс Севен Джо" if stg == 1 else "Джо.exe"
   card232 = "Сигмой" if stg == 1 else "Финальным Боссом"
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
      text = f"Хочешь получить хотя-бы <b>{card2441}</b> или даже <b>{card2442}</b>? Так делай хоть что-то, а то с момента твоего последнего открытия прошёл уже целый день!\n\n<b>{card_slogan244}</b>? Заходи и открывай набор с карточками через /card"
     elif random_reminder == 5:
      text = f"Знаешь, <b>{card245}</b> ведь тоже не сразу стал таким крутым, <b>он достиг этого самостоятельно</b>. А вот ты — лентяй! Иди и открывай карточку, если хочешь достичь хоть чего-то!\n\nНажми /card для открытия"
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
      text = f"😡 Ах ты проказник вот такой! Не заходишь в бота уже 8 часов, значит <b>плакал за тобой {card83}</b>! Не быть тебе топ 1 мира с такой дисциплиной.\n\nНажми /card чтобы открыть набор карточек"
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
      text = f"😉 Раз ты хочешь получить хотя бы <b>{card231}</b>, лучше не забывай открывать карточки. А там, вдруг ты захочешь <b>поохотиться за {card232} и топ 1 мира</b>.\n\nНажми /card чтобы открыть набор карточек"
     elif random_reminder == 4:
      text = "⌛ Часики тикают, а <b>твои шансы достичь топа всё уменьшаются</b>!\n\nНажми /card и компенсируй утерянное"
     await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_2 = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
    elif cd_first <= diff < 7200 and reminder_cd == 0:
     random_reminder = random.randint(1, 2)
     if random_reminder == 1:
      text = f"⏱️ КД {pack_name} закончился! Нажмите /card для открытия"
     elif random_reminder == 2:
      text = f"⏱️ Пришло время выбивать новых Джо Байденов — КД {pack_name} закончился! Используй /card для открытия"
     await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_cd = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
   except Exception as e:
    print(f"Не удалось отправить уведомление для {user_id}: {e}")
  unique_time_check = random.randint(1800, 3600)
  await asyncio.sleep(unique_time_check)

@dp.message(Command("settings")) # КОМАНДА НАСТРОЕК v0.1.3+
async def showing_and_setting_up_settings(event: types.Message | types.CallbackQuery):
 user_id = event.from_user.id 
 cursor.execute("INSERT OR IGNORE INTO settings (user_id) VALUES (?)", (user_id,))
 db.commit()
 cursor.execute("SELECT openings_per_time, showing_prefixes, showing_my_profile FROM settings WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 opening_per_time = row[0]
 showing_prefixes = row[1]
 showing_my_tg_profile = row[2]
 showing_prefixes = "On" if showing_prefixes == 1 else "Off"
 showing_my_tg_profile = "On" if showing_my_tg_profile == 1 else "Off"
 text = (
  "⚙️ <b>НАСТРОЙКИ</b>\n\n"
  f"Открытие карт за раз — {opening_per_time}\n"
  "<blockquote>Количество карт которые открываются за одно нажатие при распаковке из запасов</blockquote>\n\n"
  f"Отображение префиксов — {showing_prefixes}\n"
  "<blockquote>Отображение уникальных префиксов в вашем или чужом профиле</blockquote>\n\n"
  f"Отображение моего профиля — {showing_my_tg_profile}\n"
  "<blockquote>Отображение ссылки на ваш TG-профиль в лидерборде</blockquote>\n\n"
  "Контрибьюторы\n"
  "<blockquote>Люди, сделавшие вклад в развитие проекта</blockquote>\n\n"
  "В течение будущих обновлений кастомные функции и настройки будут добавлятся."
 )
 settings = InlineKeyboardBuilder() # Выбор действия в настройках
 settings.button(text="Открытие карт за раз", callback_data="opening_per_time")
 settings.button(text="Отображение префиксов", callback_data="showing_prefixes")
 settings.button(text="Отображение моего профиля", callback_data="showing_my_profile")
 settings.button(text="Контрибьюторы", callback_data="contributors")
 settings.adjust(1)
 if isinstance (event, types.Message):
  await event.answer(text=text, reply_markup=settings.as_markup())
 elif isinstance (event, types.CallbackQuery):
  await event.message.edit_text(text=text, reply_markup=settings.as_markup())
  await event.answer()

@dp.callback_query(F.data == "opening_per_time")
async def opening_per_time_setting_message(callback: CallbackQuery):
 text = "Выберите количество наборов карт которое вы хотите открывать за раз"
 opening_per_time = InlineKeyboardBuilder() # Выбор желанного количества наборов карт которые будут открыты за раз
 opening_per_time.button(text="1", callback_data="opening_one_per_time")
 opening_per_time.button(text="2", callback_data="opening_two_per_time")
 opening_per_time.button(text="3", callback_data="opening_three_per_time")
 opening_per_time.button(text="5", callback_data="opening_five_per_time")
 opening_per_time.button(text="Назад", callback_data="back_to_settings")
 opening_per_time.adjust(4, 1)
 await callback.message.edit_text(text=text, reply_markup=opening_per_time.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "opening_one_per_time")
async def opening_one_per_time(callback: CallbackQuery):
 await opening_per_time_setting(callback, 1)
 
@dp.callback_query(F.data == "opening_two_per_time")
async def opening_two_per_time(callback: CallbackQuery):
 await opening_per_time_setting(callback, 2)

@dp.callback_query(F.data == "opening_three_per_time")
async def opening_three_per_time(callback: CallbackQuery):
 await opening_per_time_setting(callback, 3)

@dp.callback_query(F.data == "opening_five_per_time")
async def opening_five_per_time(callback: CallbackQuery):
 await opening_per_time_setting(callback, 5)

@dp.callback_query(F.data == "showing_prefixes")
async def showing_prefixes_setting(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT showing_prefixes FROM settings WHERE user_id = ?", (user_id,))
 showing_prefixes = cursor.fetchone()[0]
 budut_ili_net = "не будут" if showing_prefixes == 1 else "будут"
 change_to_what = 0 if showing_prefixes == 1 else 1
 cursor.execute("UPDATE settings SET showing_prefixes = ? WHERE user_id = ?", (change_to_what, user_id))
 db.commit()
 text = f"Вы успешно изменили эту настройку. Теперь вам {budut_ili_net} отображаться уникальные префиксы игроков."
 showing_prefixes = InlineKeyboardBuilder() 
 showing_prefixes.button(text="Назад", callback_data="back_to_settings")
 await callback.message.edit_text(text=text, reply_markup=showing_prefixes.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "showing_my_profile")
async def showing_my_tg_profile_setting(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT showing_my_profile FROM settings WHERE user_id = ?", (user_id,))
 showing_my_tg_profile = cursor.fetchone()[0]
 budet_ili_net = "не будет" if showing_my_tg_profile == 1 else "будет"
 change_to_what = 0 if showing_my_tg_profile == 1 else 1
 cursor.execute("UPDATE settings SET showing_my_profile = ? WHERE user_id = ?", (change_to_what, user_id))
 db.commit()
 text = f"Вы успешно изменили эту настройку. Теперь ссылка на ваш профиль {budet_ili_net} отображаться в лидерборде."
 showing_my_profile = InlineKeyboardBuilder() 
 showing_my_profile.button(text="Назад", callback_data="back_to_settings")
 await callback.message.edit_text(text=text, reply_markup=showing_my_profile.as_markup())
 await callback.answer()
 
@dp.callback_query(F.data == "contributors")
async def showing_contributors(callback: CallbackQuery):
 text = (
  "<b>Контрибьюторы\n\n</b>"
  "@take_me_back_to_august — дизайн для Обычного и Праздничного Джо Байденов\n"
  "@Subarash_ii — хостинг бота и поддержка работы сервера"
 )
 contributors = InlineKeyboardBuilder() 
 contributors.button(text="Назад", callback_data="back_to_settings")
 await callback.message.edit_text(text=text, reply_markup=contributors.as_markup())
 await callback.answer()

@dp.callback_query(F.data == "back_to_settings")
async def back_to_settings_menu(callback: CallbackQuery):
 await showing_and_setting_up_settings(callback)

@dp.message(Command("profile")) # КОМАНДА ДЛЯ ПРОСМОТРА ЧУЖОГО ПРОФИЛЯ v0.1.2+
async def showing_someones_profile(message: types.Message):
 user_id = message.from_user.id
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
  if showing_prefixes ==  1:
   status = prefixes_selection(arg_id)
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
  else:
   text += "\n\n<blockquote>Список карт данного игрока пуст\n"
  for i in card_drop_diapazones.keys():
   if get_user_card_count(arg_id, i) > 0:
    text += f"{card_names.get(i, "")} — x{get_user_card_count(arg_id, i)}\n"
  if info[2] <= full_coll and get_user_card_count(arg_id, 6) == 0:
   text += (
    f"</blockquote>\nВсего: {info[3]} | {info[2]}/10 открыто\n"
    f"Обычные наборы карт: {info[4]}\n"
    f"Расширенные наборы карт: {info[5]}"
   )
  elif info[2] <= full_coll and get_user_card_count(arg_id, 6) > 0:
   text += (
    f"</blockquote>\nВсего: {info[3]} | {info[2]}/11 открыто\n"
    f"Обычные наборы карт: {info[4]}\n"
    f"Расширенные наборы карт: {info[5]}"
  )
  elif info[2] == full_coll + 1 and get_user_card_count(arg_id, 6) > 0:
   text += (
    f"</blockquote>\nВсего: {info[3]} | {info[2]}/11 открыто \n"
    f"Обычные наборы карт: {info[4]}\n"
    f"Расширенные наборы карт: {info[5]}"
   )
  text += f"\nПроцент прохождения: {info[6]}%"
  await message.answer(text)
  waiting_users.discard(user_id)

async def main():
 cursor.execute("SELECT xp FROM users WHERE user_id = ?", (dev_id,))
 row = cursor.fetchone()
 xp = row[0] if row else 0
 if int(time.time()) <= 1782464400 and xp == 271:
  await setup_v0_1_4()
 asyncio.create_task(reminder())
 asyncio.create_task(season_dispatcher())
 asyncio.create_task(global_rewards_dispatcher())
 await dp.start_polling(bot)

if __name__ == "__main__":
 try:
  asyncio.run(main())
 except KeyboardInterrupt:
  print("Бот выключен")