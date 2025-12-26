import discord
from discord.ext import commands
import random

WELCOME_CHANNEL_ID = 1454210909965914113

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Проверяем, что пользователь зашел в нужный канал
        if before.channel != after.channel and after.channel and after.channel.id == WELCOME_CHANNEL_ID:
            greetings = [
                f"🎉 **ДОБРО ПОЖАЛОВАТЬ В СЕМЬЮ!** 🎉\n\n"
                f"**{member.mention} зашел в святая святых!**\n"
                f"Приготовьтесь к эпичным приключениям в мире костей!",

                f"🌟 **ЗВЕЗДА ПРИБЫЛА!** 🌟\n\n"
                f"Семья Ludoman приветствует {member.mention}!\n"
                f"Готовь кости, начинается магия!",

                f"🔥 **НОВАЯ ЭНЕРГИЯ В СЕМЬЕ!** 🔥\n\n"
                f"Все приветствуем {member.mention}!\n"
                f"У нас пополнение! Готовьте напитки и удачу!",
            ]

            welcome_channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
            if welcome_channel:
                try:
                    welcome_embed = discord.Embed(
                        description=random.choice(greetings),
                        color=random.choice([0x9b59b6, 0x3498db, 0x2ecc71, 0xf1c40f])
                    )

                    if member.avatar:
                        welcome_embed.set_thumbnail(url=member.avatar.url)

                    welcome_embed.set_footer(text="Ludoman clnx • Добро пожаловать в семью!")

                    await welcome_channel.send(embed=welcome_embed)
                    print(f"👋 Отправлено приветствие для {member} в канале {welcome_channel.name}")
                except Exception as e:
                    print(f"Ошибка при отправке приветствия: {e}")

async def setup(bot):
    await bot.add_cog(EventsCog(bot))
