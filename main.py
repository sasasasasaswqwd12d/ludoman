import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import asyncio
import random
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Настройка intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class LudomanBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )
        self.statuses = [
            {"type": discord.ActivityType.playing, "name": "в кости"},
            {"type": discord.ActivityType.streaming, "name": "дрочит"},
            {"type": discord.ActivityType.custom, "name": "😴 спит"},
            {"type": discord.ActivityType.listening, "name": "🍔 ест"},
            {"type": discord.ActivityType.playing, "name": "GTA RP"},
            {"type": discord.ActivityType.watching, "name": "троллей"}
        ]
        self.current_status = 0
        self.is_ready = False

class LudomanBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )
        self.statuses = [
            # ... статусы ...
        ]
        self.current_status = 0
        self.is_ready = False
        self.temp_applications = {}  # Добавить эту строку для временного хранения заявок

    async def setup_hook(self):
        print(f'{self.user} запускается...')
        try:
            # Загружаем коги
            await self.load_extension("cogs.application")
            await self.load_extension("cogs.events")
            print("Коги успешно загружены!")
        except Exception as e:
            print(f"Ошибка при загрузке когов: {e}")

    async def on_ready(self):
        print(f'✅ Бот {self.user} успешно запущен!')
        print(f'👑 Создатель: Mason')
        print(f'🎲 Семья: Ludoman clnx')

        # Устанавливаем начальный статус
        await self.set_initial_status()

        # Запускаем задачу смены статуса
        self.change_status.start()

        try:
            await self.tree.sync()
            print("✅ Команды синхронизированы!")
        except Exception as e:
            print(f"Ошибка при синхронизации команд: {e}")

        self.is_ready = True

    async def set_initial_status(self):
        """Устанавливает начальный статус"""
        if self.statuses:
            status = self.statuses[0]
            activity = discord.Activity(
                type=status["type"],
                name=status["name"]
            )
            await self.change_presence(activity=activity)
            print(f"📊 Установлен начальный статус: {status['name']}")

    @tasks.loop(seconds=30)
    async def change_status(self):
        if not self.is_ready or not self.ws:
            return

        try:
            status = self.statuses[self.current_status]
            activity = discord.Activity(
                type=status["type"],
                name=status["name"]
            )
            await self.change_presence(activity=activity)
            print(f"📊 Смена статуса: {status['name']}")
            self.current_status = (self.current_status + 1) % len(self.statuses)
        except Exception as e:
            print(f"Ошибка при смене статуса: {e}")

    @change_status.before_loop
    async def before_change_status(self):
        """Ждем, пока бот будет готов"""
        await self.wait_until_ready()

bot = LudomanBot()

# Запуск бота
if __name__ == "__main__":
    if TOKEN:
        print("🚀 Запуск бота Ludoman clnx...")
        bot.run(TOKEN)
    else:
        print("❌ Ошибка: Токен не найден! Проверьте файл .env")
