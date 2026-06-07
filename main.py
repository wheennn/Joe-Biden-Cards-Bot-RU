from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import html_decoration as hd
from aiogram.types import FSInputFile, message, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from html import escape
import os
import random
import sqlite3
import time
import asyncio

waiting_users = set()
CD = 900

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

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML),)
dp = Dispatcher()

card_names = {
 1: "Водолаз Джо Байден",
 2: "Сикс Севен Джо Байден",
 3: "Праздничный Джо Байден",
 4: "Обычный Джо Байден",
 5: "Сигма Джо Байден",
 6: "Пожизненный Водолаз Джо Байден"
}
card_descriptions = {
 1: "Потно пахающий водолаз, выполняющий всю грязную работу. Одет в неплохое оборудование, но не сравнится с Пожизненным Водолазом. Как можно заметить, его труд был оценен поэтому он стал довольно редкой картой.",
 2: "Стереотипный ребенок, смеющийся с молодежного «67». Надел пропеллерную кепку, чтобы его не сдул ветер, и показывает свой мем. Лучшая версия нас.",
 3: "Приодетый в колпак, готов праздновать свой день рождения в любой момент организовывая специальное государственное событие.",
 4: "Ничем не отличающийся от других Джо Байден, является простым человеком, а не ярким образом.",
 5: "В крутых и стильных очках, не боится толпы и ее мнения, ведь как раз таки он — местный авторитет с миллионами фанаток по всему миру.",
 6: "Более опытный и глубоководный водолаз. Оснащен профессиональным оборудованием и готов бороться за трон Joe Biden Cards. Эксклюзивен за топ 1 мира в течение сезонов."
}
card_drop_diapazones = {
 5: 1,
 1: 5,
 2: 15,
 3: 45,
 4: 100,
 6: 0
}
card_chances = {
 1: 4,
 2: 10,
 3: 30,
 4: 55,
 5: 1,
 6: 0
}
card_xps = {
 1: 40,
 2: 15,
 3: 6,
 4: 2,
 5: 100,
 6: 0
}

card_pack_selection = InlineKeyboardBuilder() # Выбор действия при просмотре информации набора карт
card_pack_selection.button(text="Открыть", callback_data="opening")
card_pack_selection.button(text="Следующий набор", callback_data="next_pack")
card_pack_selection.adjust(1)

leaderboard_mode_selection = InlineKeyboardBuilder() # Выбор фильтра лидерборда
leaderboard_mode_selection.button(text="Сезонный лидерборд", callback_data="season_leaderboard")
leaderboard_mode_selection.button(text="Лидерборд достижений", callback_data="records_leaderboard")
leaderboard_mode_selection.adjust(1)

market_purchase_selection = InlineKeyboardBuilder() # Выбор покупки во временнем маркете
market_purchase_selection.button(text="x1 набор — 9 XP", callback_data="one_fpack_purchase")
market_purchase_selection.button(text="x10 наборов — 75 XP", callback_data="ten_fpacks_purchase")
market_purchase_selection.adjust(1)

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

try:
 cursor.execute("ALTER TABLE users ADD COLUMN winner_s0 TEXT")
 db.commit()
 print("Столбец 'winner_s0' успешно создан!")
except sqlite3.OperationalError:
 print("Столбец 'winner_s0' уже добавлен.")
try:
 cursor.execute("ALTER TABLE users ADD COLUMN fpacks INTEGER DEFAULT 0")
 db.commit()
 print("Столбец 'fpacks' успешно создан!")
except sqlite3.OperationalError:
 print("Столбец 'fpacks' уже добавлен.")

async def season_calculations(): # ДИСПЕТЧЕР СЕЗОНОВ v0.1.2+
 global season, season_start, season_end, season_desc, season_duration
 season = 0
 while True:
  if 1777203780 <= int(time.time()) <= 1780912800 and season == 0: # ДОСЕЗОННЫЙ ПЕРИОД
   season_start = 1777203780
   season_end = 1780912800
   season_desc = "Затишье перед бурей — попытайтесь достигнуть топ 1 мира чтобы получить эксклюзивную карту <b>Пожизненного Водолаза Джо Байдена</b> и забронировать место в разделе архивированных достижений списка лидеров, прежде чем начнётся полноценная система сезонов!"
   season_duration = (season_end - season_start) // 86400
  else:
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
   cursor.execute("SELECT full_name, user_id, xp FROM users ORDER BY xp DESC LIMIT 1 OFFSET 2") # ВЫДАЧА НАГРАДЫ ЗА ТОП 1 МИРА
   user = cursor.fetchone()
   cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user[1],))
   count_before = cursor.fetchone()[0]
   cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user[1],))
   prev_time = cursor.fetchone()[0]
   text = f"{user[0]}, за {season_duration} дней вы смогли набрать {user[2]} XP, заняв при этом топ 1 мира. В честь этого вы получаете эксклюзивного <b>x1 Пожизненного Водолаза Джо Байдена</b>.\n\nТакже теперь вы появились в разделе архивированных достижений списка лидеров!\n\n"
   await bot.send_message(chat_id=user[1], text=text)
   add_card(user[1], 6, 0, user[0]) # ВЫПАДЕНИЕ ПОЖИЗНЕННОГО ВОДОЛАЗА
   cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (?, ?)", (dev_id, dev_mini_id))
   row = cursor.fetchone()
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
   cursor.execute("UPDATE users SET winner_s0 = ?", (user[0],))
   db.commit()
   if count_after == 6 and count_before == 5:
    text = "Вы собрали абсолютно полную коллекцию Джо Байденов, включая эксклюзивы!\nПоследней нужной картой стал <b>Пожизненный Водолаз Джо Байден</b>.\n\nВы можете просмотреть обновлённый лидерборд с вашим ником используя /leaderboard."
    await bot.send_message(chat_id=user[1], text=text)
   cursor.execute("SELECT full_name, user_id, xp FROM users") # ВЫДАЧА БОНУСА В ЧЕСТЬ НАЧАЛА СЕЗОНА
   members = cursor.fetchall()
   for member in members:
    try:
     text = f"Новый сезон начался! Соревнуйтесь за топ 1 мира, чтобы получить эксклюзивного <b>Пожизненного Водолаза Джо Байдена</b>\n\nОпыт всех игроков был обнулён, а также в честь начала первого полноценного сезона каждому выдано <b>x5 обычных наборов карт</b>."
     cursor.execute("UPDATE users SET fpacks = fpacks + 5, xp = 0 WHERE user_id = ?", (member[1],))
     await bot.send_message(chat_id=member[1], text=text)
     await asyncio.sleep(0.1)
    except Exception as e:
     print(f"Не удалось отправить уведомление для {member[1]}: {e}")
   db.commit()
   season += 1
   await asyncio.sleep(6)
  await asyncio.sleep(1)

@dp.message(Command("all_info"))  # АДМИН КОМАНДА v0.1.1.3+
async def showing_db_info(message: types.Message):
 if message.from_user.id not in [dev_id, dev2_id]:
  text = "У вас недостаточно прав для использования команды /all_info."
  await message.answer(text)
  return
 cursor.execute("SELECT user_id FROM users")
 ids = [row[0] for row in cursor.fetchall()]
 text = "<b>ВСЯ ИНФОРМАЦИЯ</b>\n"
 for id in ids:
  cursor.execute("SELECT full_name, xp, total_cards, unlocked_cards FROM users WHERE user_id = ?", (id,))
  row = cursor.fetchone()
  full_name, xp, total_cards, unlocked_cards = row if row else ("Anon", 0, 0, 0)
  text += f"\n<b>{full_name} — {id} | {xp} XP</b>\n"
  cursor.execute("SELECT card_id, count FROM user_cards WHERE user_id = ?", (id,))
  user_cards = cursor.fetchall()
  for card_id, count in user_cards:
   card_name = card_names.get(card_id, f"Карта не найдена")
   text += f"{card_name} — x{count}\n"
  if unlocked_cards <= 5:
   text += f"Всего: {total_cards} карт | Открыто: {unlocked_cards}/5\n"
  elif unlocked_cards == 6:
   text += f"Всего: {total_cards} карт | Открыто: {unlocked_cards}/6\n"
  if id == t1_season0:
   text += (
    "\nПервый в мире <b>Водолаз Джо Байден</b>\n"
    "Первый в мире <b>Сикс Севен Джо Байден</b>\n"
    "Первый в мире <b>Праздничный Джо Байден</b>\n"
    "Первый в мире <b>Обычный Джо Байден</b>\n"
   )
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
  "<b>⚡️ ОБНОВЛЕНИЕ v0.1.2 ВЫШЛО!</b>\n\n"
  "Новое:\n"
  "<blockquote>— Добавлены 2 новые карты: эксклюзивный <b>Пожизненный Водолаз Джо Байден</b> и редкий <b>Сигма Джо Байден</b>.\n"
  "— Внедрена система сезонов: соревновательные периоды, в течение которых игроки борются за эксклюзивную карту. Накопленный за сезон XP сбрасывается перед началом следующего.\n"
  "— Сезонный маркет: временный магазин, который открывается в последний день сезона. Позволяет приобрести наборы карт за накопленный XP, чтобы получить преимущество в следующем сезоне или просто попытаться выбить новую редкую карту.\n"
  "— Команда <b>/profile</b>: добавлена возможность просмотра профиля другого игрока через его <b>Telegram-ID</b>.</blockquote>\n\n"
  "QoL:\n"
  "<blockquote>— Возможность открытия купленных или полученных в подарок наборов карт в любое время, в обход стандартного КД.\n"
  "— Полный переход интерфейса бота на <b>инлайн-кнопки</b> по многочисленным просьбам игроков.\n"
  "— Оптимизация лидерборда: фильтры «по первенству» и «по коллекции» объединены в общую вкладку со всеми активными и архивными достижениями игроков.\n"
  "— Полностью изменены описания всех карт и обновлен общий стиль их подачи.\n"
  "— Добавлены специальные префиксы для учетных записей администрации.\n"
  "— Исправлены грамматические ошибки, опечатки и улучшена читаемость системных сообщений и в некоторых местах добавлено форматирование.</blockquote>\n\n"
  "В этот раз одноразовая награда по команде недоступна, но в честь выхода обновления в /market уже действуют <b>скидки от -10% до -25%</b>. Также завтра, сразу после старта нового сезона, всем игрокам будет начислено <b>x5 обычных наборов карт</b>."
 )
 cursor.execute("SELECT user_id FROM users")
 rows = cursor.fetchall()
 count = 0
 if int(time.time()) < 1780848000:
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

@dp.message(Command("market")) # КОМАНДА ВРЕМЕННОГО МАРКЕТА v0.1.2+
async def showing_market(message: types.Message):
 global season, season_start, season_end, season_desc, season_duration
 left_before_s_end = season_end - time.time()
 if 86400 >= left_before_s_end > 0:
  h = int(left_before_s_end // 3600)
  m = int((left_before_s_end % 3600) // 60)
  text = (
   f"<b>🛍 ВРЕМЕННЫЙ МАРКЕТ</b> — до закрытия {h}ч {m}м\n\n"
   "<blockquote>Здесь вы можете обменять ваш опыт в конце сезона на наборы карт, чтобы поохотиться за новыми добавленными редкими картами или получить фору в начале следующего сезона.</blockquote>\n\n"
   "Доступные акции:\n"
   "<blockquote>🃏 <b>x1 Обычный Набор Карт</b> — <s>10</s> 9 XP (-10%)\n"
   "🃏 <b>x10 Обычных Наборов Карт</b> — <s>100</s> 75 XP (-25%)</blockquote>\n\n"
   "Выберите акцию для покупки:"
  )
  await message.answer(text, reply_markup=market_purchase_selection.as_markup())
 else:
  left_before_m_appear = left_before_s_end - 86400
  d = int(left_before_m_appear // 86400)
  h = int((left_before_m_appear % 86400) // 3600)
  text = f"🚫 Временный маркет закрыт. До его появления осталось {d}д {h}ч"
  await message.answer(text)

@dp.callback_query(F.data == "one_fpack_purchase")
async def processing_one_fpack_purchase(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 xp = row[0] if row else 0
 if xp >= 9:
  cursor.execute("UPDATE users SET xp = xp - 9, fpacks = fpacks + 1 WHERE user_id = ?", (user_id,))
  db.commit()
  text = "Вы успешно приобрели <b>x1 обычный набор карт</b> за 9 XP"
  await callback.message.answer(text)
 else:
  text = "Недостаточно XP для покупки. Попробуйте позже."
  await callback.message.answer(text)
 await callback.answer()

@dp.callback_query(F.data == "ten_fpacks_purchase")
async def processing_ten_fpacks_purchase(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 xp = row[0] if row else 0
 if xp >= 75:
  cursor.execute("UPDATE users SET xp = xp - 75, fpacks = fpacks + 10 WHERE user_id = ?", (user_id,))
  db.commit()
  text = "Вы успешно приобрели <b>x10 обычных наборов карт</b> за 75 XP"
  await callback.message.answer(text)
 else:
  text = "Недостаточно XP для покупки. Попробуйте позже."
  await callback.message.answer(text)
 await callback.answer()

@dp.message(Command("leaderboard")) # СПИСОК ЛИДЕРОВ v0.1+
async def show_leaderboard(message: types.Message):
 text = "Выберите режим лидерборда для его просмотра:"
 await message.answer(text, reply_markup=leaderboard_mode_selection.as_markup())

@dp.callback_query(F.data == "season_leaderboard") # Сезонный лидерборд
async def handle_season_leaderboard(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 cursor.execute("SELECT full_name, xp FROM users WHERE user_id NOT IN (?, ?) ORDER BY XP DESC LIMIT 10", (dev_id, dev_mini_id))
 users = cursor.fetchall()
 results = "<b>🏆 СЕЗОННЫЙ ЛИДЕРБОРД</b>\n"
 left_before_s_end = season_end - time.time()
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
 rank = 1
 for user in users:
  medal = "👑" if rank == 1 else f"{rank}"
  dot = "" if rank == 1 else "."
  results += f"{medal}{dot} {escape(user[0])} — {user[1]} XP\n"
  rank += 1
 cursor.execute("SELECT SUM(total_count) FROM card_stats")
 row = cursor.fetchone()
 total_cards = row[0] if row and row[0] else 0
 cursor.execute("SELECT total_cards FROM users WHERE user_id = ?", (dev_id,))
 devs_cards = 0
 row = cursor.fetchone()
 devs_cards += int(row[0]) if row and row[0] is not None else 0
 cursor.execute("SELECT total_cards FROM users WHERE user_id = ?", (dev_mini_id,))
 row = cursor.fetchone()
 devs_cards += int(row[0]) if row and row[0] is not None else 0
 results += f"\nВсего карточек существует: {total_cards - devs_cards}\n\n"
 await callback.message.answer(results) 
 await callback.answer()

@dp.callback_query(F.data == "records_leaderboard") # Лидерборд достижений
async def handle_records_leaderboard(callback: CallbackQuery):
 global season, season_start, season_end, season_desc, season_duration
 cursor.execute("SELECT full_name FROM users WHERE unlocked_cards = 5 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with5 = cursor.fetchall()
 cursor.execute("SELECT full_name FROM users WHERE unlocked_cards = 6 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with6 = cursor.fetchall()
 cursor.execute("SELECT COUNT(*) FROM users WHERE unlocked_cards = 5 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with_full_coll5 = cursor.fetchone()[0] or 0
 cursor.execute("SELECT COUNT(*) FROM users WHERE unlocked_cards = 6 AND user_id NOT IN (?, ?)", (dev_id, dev_mini_id))
 users_with_full_coll6 = cursor.fetchone()[0] or 0
 results = "<b>🏆 ЛИДЕРБОРД ДОСТИЖЕНИЙ</b>"
 if users_with5:
  names_5 = [escape(u[0]) for u in users_with5]
  results += "\n\nПолная коллекция (5/5):\n" + ", ".join(names_5)
  results += f"\nВсего игроков: {users_with_full_coll5}"
 if users_with6:
  names_6 = [escape(u[0]) for u in users_with6]
  results += "\n\nПолная коллекция (6/6):\n" + ", ".join(names_6)
  results += f"\nВсего игроков: {users_with_full_coll6}"
 cursor.execute("SELECT winner_s0 FROM users WHERE winner_s0 IS NOT NULL AND winner_s0 != 'None' LIMIT 1")
 row = cursor.fetchone()
 the_winner_s0 = row[0] if row and row[0] is not None else "None"
 if the_winner_s0 != "None":
  results += (
   "\n\nПобедители сезонов:"
   f"\n<blockquote>{escape(the_winner_s0)} — топ-1 мира в досезонном периоде</blockquote>"
  ) 
 results += (
  "\n\n<b>АРХИВИРОВАННЫЕ ДОСТИЖЕНИЯ</b>"
  "\n\nПервооткрыватели:"
  "\n<blockquote>Victony — первый в мире <b>Открытый Набор</b> (23.04)"
 )
 cursor.execute("SELECT first_unlocked FROM card_stats WHERE card_id = 5")
 row = cursor.fetchone()
 first_id5 = row[0] if row and row[0] else "None"
 cursor.execute("SELECT first_unlocked FROM card_stats WHERE card_id = 6")
 row = cursor.fetchone()
 first_id6 = row[0] if row and row[0] else "None"
 if first_id6 != "None":
  results += f"\n{escape(first_id6)} — первый в мире <b>Пожизненный Водолаз Джо Байден</b>"
 if first_id5 != "None":
  results += f"\n{escape(first_id5)} — первый в мире <b>Сигма Джо Байден</b>"
 results += (
  "\ncwendyzz — первый в мире <b>Водолаз Джо Байден</b> (26.04)"
  "\ncwendyzz — первый в мире <b>Сикс Севен Джо Байден</b> (26.04)"
  "\nVictony — первый в мире <b>Праздничный Джо Байден</b> (23.04)"
  "\ncwendyzz — первый в мире <b>Обычный Джо Байден</b> (26.04)"
  "\ncwendyzz — первая в мире <b>Полная Коллекция</b> (26.04)</blockquote>"
 )
 await callback.message.answer(results)
 await callback.answer()

@dp.message(Command("start")) # КОМАНДА ДЛЯ СТАРТА v0.1+
async def start_handler(message: types.Message):
 text = (
 "👋 Привет, ты попал в <b>Joe Biden Cards.</b>\n\n"
 "Здесь ты можешь выбивать разные карточки с Джо Байденом, коллекционировать их и просто проводить время.\n\n"
 "Проект находится в начальной разработке, поэтому в нём могут присутствовать некоторые баги.\n\n"
 "Создано @by_when\n\n"
 "GitHub — https://github.com/wheennn/Joe-Biden-Cards-Bot-RU\n\n"
 "Весь материал используется исключительно в шуточных целях.\n\n"
 "Чтобы начать игру, используйте команду /card\n\n"
 "Актуальная версия: v0.1.2"
 )
 await message.answer(text)

@dp.message(Command("menu")) # КОМАНДА МЕНЮ v0.1+
async def handle_answer(message: types.Message):
 nickname = escape(message.from_user.full_name)
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
 cursor.execute("SELECT fpacks FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 fpacks = row[0] if row else 0
 if nickname in("wheen. <3", "wheen?🍂"):
  text = f"<b>[DEV] {nickname} | {xp} XP</b>\n"
 else:
  text = f"<b>{nickname} | {xp} XP</b>\n"
 if get_user_card_count(user_id, 6) >= 1:
  text += (
   "\nЭксклюзивные карты:\n"
   f"<blockquote>Пожизненный Водолаз Джо Байден — x{get_user_card_count(user_id, 6)}</blockquote>\n"
  )
 if total_cards > 0 and get_user_card_count(user_id, 6) == 0:
  text += "\nОбычные карты:\n<blockquote>"
 if get_user_card_count(user_id, 5) >= 1:
  text += f"Сигма Джо Байден — x{get_user_card_count(user_id, 5)}\n"
 if get_user_card_count(user_id, 1) >= 1:
  text += f"Водолаз Джо Байден — x{get_user_card_count(user_id, 1)}\n"
 if get_user_card_count(user_id, 2) >= 1:
  text += f"Сикс Севен Джо Байден — x{get_user_card_count(user_id, 2)}\n"
 if get_user_card_count(user_id, 3) >= 1:
  text += f"Праздничный Джо Байден — x{get_user_card_count(user_id, 3)}\n"
 if get_user_card_count(user_id, 4) >= 1:
  text += f"Обычный Джо Байден — x{get_user_card_count(user_id, 4)}\n"
 if collected >= 6:
  text += f"</blockquote>\nВсего: {total_cards} | Собрано: {collected}/6\n"
 else:
  text += f"</blockquote>\nВсего: {total_cards} | Собрано: {collected}/5\n"
 text += f"Наборы карт: {fpacks}"
 await message.answer(text)

@dp.message(Command("card")) # КОМАНДА ДЛЯ ОТКРЫТИЯ КАРТЫ v0.1+
async def handle_answer(message: types.Message):
 user_id = message.from_user.id
 nickname = escape(message.from_user.full_name)
 cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)", (user_id, message.from_user.full_name))
 db.commit() 
 cursor.execute(
    "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
    (user_id, nickname or "Anon")
 )
 cursor.execute(
    "UPDATE users SET full_name = ? WHERE user_id = ?",
    (nickname or "Anon", user_id)
 )
 db.commit()
 text = (
  "<b>🃏 Обычный набор карт с Джо Байденом</b>\n\n"
  "• Шансы:\n\n"
  "Сигма Джо Байден — 1%\n"
  "Водолаз Джо Байден — 4%\n"
  "Сикс Севен Джо Байден — 10%\n"
  "Праздничный Джо Байден — 30%\n"
  "Обычный Джо Байден — 55%"
 )
 await message.answer(text, reply_markup=card_pack_selection.as_markup())

@dp.callback_query(F.data == "opening")
async def opening(callback: CallbackQuery):
 user_id = callback.from_user.id
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 last_opening_time = row[0] if row else 0
 current_left = CD - int(time.time() - last_opening_time)
 cursor.execute("SELECT fpacks FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 fpacks = row[0] if row else 0
 card_pack_opening_selection = InlineKeyboardBuilder() # Выбор способа открытия набора карт
 if current_left > 0:
  minutes = current_left // 60
  seconds = current_left % 60
  card_pack_opening_selection.button(text=f"Бесплатно ({minutes}m {seconds}s)", callback_data="opening_through_cd")
 elif current_left <= 0:
  card_pack_opening_selection.button(text="Бесплатно (0m 0s)", callback_data="opening_through_cd")
 if fpacks > 0:
  card_pack_opening_selection.button(text=f"Открыть из запасов ({fpacks} шт.)", callback_data="opening_through_fpacks")
 card_pack_opening_selection.adjust(1)
 await callback.message.edit_text(text=f"Выберите способ открытия:",reply_markup=card_pack_opening_selection.as_markup())

@dp.callback_query(F.data == "opening_through_cd")
async def opening_through_cd(callback: CallbackQuery):
 user_id = callback.from_user.id
 nickname = escape(callback.from_user.full_name)
 cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
 count_before = cursor.fetchone()[0]
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 last_opening_time = row[0] if row else 0
 current_left = CD - int(time.time() - last_opening_time)
 if current_left <= 0:
  chance = random.randint(1, 100)
  devs_cards = 0
  for i in card_drop_diapazones.keys():
   if chance <= card_drop_diapazones.get(i):
    xp_to_add = card_xps.get(i, 0)
    add_card(user_id, i, xp_to_add, nickname)
    if get_user_card_count(user_id, i) == 1:
     cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
     db.commit()
    cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (7020510390, 7481475946) AND card_id = ?", (i,))
    row = cursor.fetchone()
    devs_cards = row[0] if row and row[0] is not None else 0
    actual_card_name = card_names.get(i, "").replace(" ", "")
    actual_card_name += ".jpg"
    photo = FSInputFile(os.path.join(base_dir, "images", actual_card_name))
    text = (
      "Вам выпал..\n"
     f"<b>{card_names.get(i, "")} — {card_chances.get(i, "")}%!</b>\n"
     f"+{card_xps.get(i, "")} XP\n\n"
     f"<blockquote>{card_descriptions.get(i, "")}</blockquote>\n\n"
     f"Количество: {get_user_card_count(user_id, i)}\n"
     f"Всего в мире: {get_world_card_count(i) - devs_cards}\n\n"
     "Для просмотра вашей обновленной коллекции нажмите /menu"
    )
    await callback.message.answer_photo(photo=photo, caption=text)
    cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
    count_after = cursor.fetchone()[0]
    if get_world_card_count(i) == 1:
     text = f"Вы первыми в мире открыли карту <b>{card_names.get(i, "")}</b>!\n+{card_xps.get(i, "")} XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
     await callback.message.answer(text)
     xp_to_add = card_xps.get(i, 0)
     cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
     db.commit()
    if count_after == 5 and count_before == 4:
     if user_id in full_coll_users:
      text = f"Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n +125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard\n\nПоскольку вы достигли данного показателя и получили опыт за него еще раньше, ваша текущая награда была уменьшена."
      xp_to_add = 125
     else:
      text = f"Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n +250 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
      xp_to_add = 250
     cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
     db.commit()
     await callback.message.answer(text)
    elif count_after == 6 and count_before == 5:
     if user_id in full_coll_users:
      text = f"Вы собрали абсолютно полную коллекцию Джо Байденов включая эксклюзивы!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n+125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard\n\nПоскольку вы достигли данного показателя и получили опыт за него еще раньше, ваша текущая награда была уменьшена."
      xp_to_add = 125
     else:
      text = f"Вы собрали абсолютно полную коллекцию Джо Байденов включая эксклюзивы!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n+250 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
      xp_to_add = 250
     cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
     db.commit()
     await callback.message.answer(text)
    await callback.answer()
    break
 else: 
  minutes = current_left // 60
  seconds = current_left % 60
  cursor.execute("SELECT fpacks FROM users WHERE user_id = ?", (user_id,))
  row = cursor.fetchone()
  fpacks = row[0] if row else 0
  if fpacks == 0:
   text = f"⏱️ Сейчас данный набор находится в КД. Вы сможете открыть его через <b>{minutes}m {seconds}s</b>."
  elif fpacks >= 1:
   text = f"⏱️ Сейчас данный набор находится в КД. Вы сможете открыть его через <b>{minutes}m {seconds}s</b>. Вы также можете открыть набор <b>прямо сейчас</b> потратив свои накопленные запасы."
  await callback.message.answer(text)
  
@dp.callback_query(F.data == "opening_through_fpacks")
async def opening_through_fpacks(callback: CallbackQuery):
 user_id = callback.from_user.id
 nickname = escape(callback.from_user.full_name)
 cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
 count_before = cursor.fetchone()[0]
 cursor.execute("SELECT last_card_time FROM users WHERE user_id = ?", (user_id,))
 row = cursor.fetchone()
 prev_time = row[0] if row else 0
 chance = random.randint(1, 100)
 devs_cards = 0
 for i in card_drop_diapazones.keys():
  if chance <= card_drop_diapazones.get(i):
   xp_to_add = card_xps.get(i, 0)
   add_card(user_id, i, xp_to_add, nickname)
   if get_user_card_count(user_id, i) == 1:
    cursor.execute("UPDATE users SET unlocked_cards = unlocked_cards + 1 WHERE user_id = ?", (user_id,))
    db.commit()
   cursor.execute("SELECT SUM(count) FROM user_cards WHERE user_id IN (7020510390, 7481475946) AND card_id = ?", (i,))
   row = cursor.fetchone()
   devs_cards = row[0] if row and row[0] is not None else 0
   actual_card_name = card_names.get(i, "").replace(" ", "")
   actual_card_name += ".jpg"
   photo = FSInputFile(os.path.join(base_dir, "images", actual_card_name))
   text = (
     "Вам выпал..\n"
    f"<b>{card_names.get(i, "")} — {card_chances.get(i, "")}%!</b>\n"
    f"+{card_xps.get(i, "")} XP\n\n"
    f"<blockquote>{card_descriptions.get(i, "")}</blockquote>\n\n"
    f"Количество: {get_user_card_count(user_id, i)}\n"
    f"Всего в мире: {get_world_card_count(i) - devs_cards}\n\n"
    "Для просмотра вашей обновленной коллекции нажмите /menu"
   )
   await callback.message.answer_photo(photo=photo, caption=text)
   cursor.execute("SELECT unlocked_cards FROM users WHERE user_id = ?", (user_id,))
   count_after = cursor.fetchone()[0]
   if get_world_card_count(i) == 1:
    text = f"Вы первыми в мире открыли карту <b>{card_names.get(i, "")}</b>!\n+{card_xps.get(i, "")} XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
    await callback.message.answer(text)
    xp_to_add = card_xps.get(i, 0)
    cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
    db.commit()
   if count_after == 5 and count_before == 4:
    if user_id in full_coll_users:
     text = f"Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n +125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard\n\nПоскольку вы достигли данного показателя и получили опыт за него еще раньше, ваша текущая награда была уменьшена."
     xp_to_add = 125
    else:
     text = f"Вы собрали полную коллекцию Джо Байденов!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n +250 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
     xp_to_add = 250
    cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
    db.commit()
    await callback.message.answer(text)
   elif count_after == 6 and count_before == 5:
    if user_id in full_coll_users:
     text = f"Вы собрали абсолютно полную коллекцию Джо Байденов включая эксклюзивы!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n+125 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard\n\nПоскольку вы достигли данного показателя и получили опыт за него еще раньше, ваша текущая награда была уменьшена."
     xp_to_add = 125
    else:
     text = f"Вы собрали абсолютно полную коллекцию Джо Байденов включая эксклюзивы!\nПоследней нужной картой стал <b>{card_names.get(i, "")}</b>.\n+250 XP\n\nВы можете просмотреть обновленный лидерборд с вашим ником используя /leaderboard"
     xp_to_add = 250
    cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (xp_to_add, user_id))
    db.commit()
    await callback.message.answer(text)
   await callback.answer()
   cursor.execute("UPDATE users SET last_card_time = ? WHERE user_id = ?", (prev_time, user_id))
   db.commit()
   cursor.execute("UPDATE users SET fpacks = fpacks - 1 WHERE user_id = ?", (user_id,))
   db.commit()
   break

@dp.callback_query(F.data == "next_pack")
async def next_pack(callback: CallbackQuery):
 text = "📃 Утверждаем в Конгрессе.."
 await callback.message.answer(text)

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
     cursor.execute("UPDATE reminder_spam SET reminder_24 = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
    elif 28800 <= diff < 84600 and reminder_8 == 0:
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
     cursor.execute("UPDATE reminder_spam SET reminder_8 = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
    elif 7200 <= diff < 28800 and reminder_2 == 0:
     random_reminder = random.randint(1, 3)
     if random_reminder == 1:
      text = "С момента вашего последнего открытия прошло уже около 2 часов.\n\nНажмите /card для открытия."
      await bot.send_message(chat_id=user_id, text=text)
     elif random_reminder == 2:
      text = "Твои конкуренты уже лутают опыт во всю, а ты что?\n\nНажми /card и компенсируй утерянное."
      await bot.send_message(chat_id=user_id, text=text)
     elif random_reminder == 3:
      text = "Раз ты хочешь получить хотя бы Праздничного Джо, лучше не забывай открывать карточки. А там, вдруг ты захочешь поохотиться за Водолазом и топ 1 мира.\n\nНажми /card чтоб открыть набор карточек."
      await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_2 = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
    elif 1800 <= diff < 7200 and reminder_cd == 0:
     text = "⏱️ КД обычного набора карточек закончился! Нажмите /card для открытия."
     await bot.send_message(chat_id=user_id, text=text)
     cursor.execute("UPDATE reminder_spam SET reminder_cd = ? WHERE user_id = ?", (time.time(), user_id))
     db.commit()
   except Exception as e:
    print(f"Не удалось отправить уведомление для {user_id}: {e}")
  unique_time_check = random.randint(1800, 3600)
  await asyncio.sleep(unique_time_check)

@dp.message(Command("profile")) # КОМАНДА ДЛЯ ПРОСМОТРА ЧУЖОГО ПРОФИЛЯ v0.1.2+
async def showing_someones_profile(message: types.Message):
 user_id = message.from_user.id
 text = "Введите ID игрока в телеграме, чей профиль вы хотите просмотреть."
 await message.answer(text)
 waiting_users.add(user_id)

@dp.message()
async def checking_up_answer(message: types.Message):
 nickname = message.from_user.full_name
 user_id = message.from_user.id
 if user_id in waiting_users:
  if not message.text:
   waiting_users.discard(user_id)
   return
  try:
   given_id = int(message.text)
   cursor.execute("SELECT full_name, xp, unlocked_cards, total_cards, fpacks FROM users WHERE user_id = ?", (given_id,))
   row = cursor.fetchone() 
   info = row if row else ("Неизвестный пользователь", 0, 0, 0, 0)
   if info[0] == "Неизвестный пользователь":
    text = "Данного пользователя не найдено в базе. Попробуйте еще раз."
    await message.answer(text)
    waiting_users.discard(user_id)
    return
   if given_id in (dev_id, dev_mini_id):
    text = f"<b>[DEV] {info[0]} | {info[1]} XP</b>"
   else:
    text = f"<b>{info[0]} | {info[1]} XP</b>"
   if get_user_card_count(given_id, 6) > 0:
    text += (
     "\n\nЭксклюзивные:"
     f"\n<blockquote>Пожизненный Водолаз Джо Байден — x{get_user_card_count(given_id, 6)}</blockquote>"
    )
   cursor.execute("SELECT total_cards FROM users WHERE user_id = ?", (given_id,))
   row = cursor.fetchone()
   total_cards = row[0] if row else 0
   if total_cards > 0 and get_user_card_count(given_id, 6) == 0:
    text += "\n\nОбычные:\n<blockquote>"
   if get_user_card_count(given_id, 5) > 0:
    text += f"Сигма Джо Байден — x{get_user_card_count(given_id, 5)}\n"
   if get_user_card_count(given_id, 1) > 0:
    text += f"Водолаз Джо Байден — x{get_user_card_count(given_id, 1)}\n"
   if get_user_card_count(given_id, 2) > 0:
    text += f"Сикс Севен Джо Байден — x{get_user_card_count(given_id, 2)}\n"
   if get_user_card_count(given_id, 3) > 0:
    text += f"Праздничный Джо Байден — x{get_user_card_count(given_id, 3)}\n"
   if get_user_card_count(given_id, 4) > 0:
    text += f"Обычный Джо Байден — x{get_user_card_count(given_id, 4)}\n"
   if info[2] > 5:
    text += (
     f"</blockquote>\nВсего: {info[3]} | {info[2]}/6 открыто\n"
     f"Запасы наборов карт: {info[4]}"
    )
   elif info[2] <= 5:
    text += (
    f"</blockquote>\nВсего: {info[3]} | {info[2]}/5 открыто\n"
     f"Запасы наборов карт: {info[4]}"
   )
   await message.answer(text)
   waiting_users.discard(user_id)
  except ValueError:
   text = "Вы ввели текст вместо ID игрока. Попробуйте снова."
   await message.answer(text)

async def main():
 asyncio.create_task(reminder())
 asyncio.create_task(season_calculations())
 await dp.start_polling(bot)

if __name__ == "__main__":
 try:
  asyncio.run(main())
 except KeyboardInterrupt:
  print("Бот выключен")
