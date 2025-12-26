import discord
from discord.ext import commands
import random

WELCOME_CHANNEL_ID = 1454210909965914113

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel and after.channel and after.channel.id == WELCOME_CHANNEL_ID:
            greetings = [
                "🎉 **ДОБРО ПОЖАЛОВАТЬ В СЕМЬЮ!** 🎉\n\n"
                f"**{member.mention} зашел в святая святых!**\n"
                "Приготовьтесь к эпичным приключениям в мире костей!",

                "🌟 **ЗВЕЗДА ПРИБЫЛА!** 🌟\n\n"
                f"Семья Ludoman приветствует {member.mention}!\n"
                "Готовь кости, начинается магия!",

                "🔥 **НОВАЯ ЭНЕРГИЯ В СЕМЬЕ!** 🔥\n\n"
                f"Все приветствуем {member.mention}!\n"
                "У нас пополнение! Готовьте напитки и удачу!",

                "🎲 **КОСТИ ЗВОНЯТ ТВОИМ ИМЕНЕМ!** 🎲\n\n"
                f"{member.mention} входит в игру!\n"
                "Пусть удача всегда будет на твоей стороне!",

                "💫 **МАГИЯ НАЧИНАЕТСЯ!** 💫\n\n"
                f"Приветствуем {member.mention} в нашем королевстве!\n"
                "Здесь рождаются легенды костей!",

                "🏆 **НОВЫЙ ИГРОК В КОМАНДЕ!** 🏆\n\n"
                f"Встречайте {member.mention}!\n"
                "Готовьтесь к незабываемым играм и победам!",

                "🎪 **ЦИРК КОСТЕЙ ОТКРЫТ!** 🎪\n\n"
                f"На арене появляется {member.mention}!\n"
                "Делайте ваши ставки, господа!",

                "✨ **СВЕТИЛО ВОШЛО В ЧАТ!** ✨\n\n"
                f"Приветствуем {member.mention}!\n"
                "Пусть каждый бросок будет удачным!",

                "🎭 **НОВЫЙ АКТЕР НА СЦЕНЕ!** 🎭\n\n"
                f"Встречайте {member.mention}!\n"
                "Готовьтесь к спектаклю удачи и азарта!",

                "⚡ **ЗАРЯД АЗАРТА ВОПЛОТИЛСЯ!** ⚡\n\n"
                f"Семья Ludoman встречает {member.mention}!\n"
                "Пусть кости благоволят тебе!"
            ]

            welcome_channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
            if welcome_channel:
                welcome_embed = discord.Embed(
                    description=random.choice(greetings),
                    color=random.choice([0x9b59b6, 0x3498db, 0xe74c3c, 0x2ecc71, 0xf1c40f])
                )
                welcome_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                welcome_embed.set_footer(text="Ludoman clnx • Добро пожаловать в семью!")

                await welcome_channel.send(embed=welcome_embed)

async def setup(bot):
    await bot.add_cog(EventsCog(bot))
