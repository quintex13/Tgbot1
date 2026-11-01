import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

# Твой токен уже встроен
TOKEN = "9054857838:AAGRwF9QG_9J-ezdGiJoO3Ow6wslY3ZtFh8"

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для отслеживания времени сообщений пользователей: {user_id: [список_времени]}
user_messages = {}

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я твой личный бот-помощник для администрирования чата. "
        "Антиспам-модуль активирован!"
    )

# Обработка текстовых сообщений и проверка на спам
@dp.message(F.text)
async def anti_spam(message: Message):
    # Игнорируем сообщения от администраторов (если нужно, но пока проверяем всех)
    user_id = message.from_user.id
    now = datetime.now()

    # Если пользователя еще нет в словаре, добавляем
    if user_id not in user_messages:
        user_messages[user_id] = []

    # Оставляем только те сообщения, которые были отправлены за последнюю 1 минуту
    one_minute_ago = now - timedelta(minutes=1)
    user_messages[user_id] = [t for t in user_messages[user_id] if t > one_minute_ago]

    # Добавляем текущее сообщение
    user_messages[user_id].append(now)

    # Проверяем лимит (больше 5 сообщений за минуту)
    if len(user_messages[user_id]) > 5:
        # Сбрасываем список, чтобы не спамить предупреждениями на каждое следующее сообщение
        user_messages[user_id] = []
        await message.reply("🚨 Обнаружен спамер!")

async def main():
    print("Бот запущен и следит за чатом...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
