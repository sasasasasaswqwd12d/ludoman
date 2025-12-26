import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import asyncio
from datetime import datetime
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
            intents=intents,
            application_id=os.getenv('APPLICATION_ID', None)
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

    async def setup_hook(self):
        print(f'{self.user} запускается...')
        await self.load_extension("cogs.application")
        await self.load_extension("cogs.events")
        self.change_status.start()

    async def on_ready(self):
        print(f'Бот {self.user} успешно запущен!')
        print(f'Создатель: Mason')
        print(f'Семья: Ludoman clnx')
        await self.tree.sync()

    @tasks.loop(seconds=30)
    async def change_status(self):
        status = self.statuses[self.current_status]
        activity = discord.Activity(
            type=status["type"],
            name=status["name"]
        )
        await self.change_presence(activity=activity)
        self.current_status = (self.current_status + 1) % len(self.statuses)

bot = LudomanBot()

# Запуск бота
if __name__ == "__main__":
    bot.run(TOKEN)
