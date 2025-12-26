import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Modal, TextInput, Select
import asyncio
from datetime import datetime

# ID ролей для модерации
MOD_ROLES = [1454210800813346968, 1454210803472400404]

class ApplicationModal(Modal, title="📝 Заявка в семью Ludoman clnx"):
    nickname = TextInput(
        label="Ваш игровой ник",
        placeholder="Пример: Nick_Name",
        max_length=32,
        required=True
    )

    static_id = TextInput(
        label="Ваш Static ID",
        placeholder="Пример: 66666",
        max_length=10,
        required=True
    )

    age = TextInput(
        label="Ваш возраст (IRL)",
        placeholder="Пример: 18",
        max_length=2,
        required=True
    )

    real_name = TextInput(
        label="Как вас зовут в реальной жизни?",
        placeholder="Пример: Александр",
        max_length=32,
        required=True
    )

    playtime = TextInput(
        label="Сколько времени уделяете игре?",
        placeholder="Пример: 4-5 часов в день",
        max_length=50,
        required=True
    )

    discovery = TextInput(
        label="Откуда узнали о семье?",
        placeholder="Пример: TikTok / Маркет / Друзья",
        max_length=100,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        embed = discord.Embed(
            title="🎲 Новая заявка в Ludoman clnx",
            color=0x00ff00,
            timestamp=datetime.now()
        )

        embed.add_field(name="👤 Никнейм", value=self.nickname.value, inline=True)
        embed.add_field(name="🆔 Static ID", value=self.static_id.value, inline=True)
        embed.add_field(name="🎂 Возраст", value=self.age.value, inline=True)
        embed.add_field(name="📛 Реальное имя", value=self.real_name.value, inline=True)
        embed.add_field(name="⏰ Время в игре", value=self.playtime.value, inline=True)
        embed.add_field(name="📢 Откуда узнал", value=self.discovery.value, inline=True)
        embed.add_field(name="👤 Подавший", value=f"{interaction.user.mention} ({interaction.user.id})", inline=False)

        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.set_footer(text="Ludoman clnx • Заявка ожидает рассмотрения")

        # Кнопки для модерации
        view = ModerationView()
        view.application_data = {
            "user_id": interaction.user.id,
            "nickname": self.nickname.value,
            "static_id": self.static_id.value,
            "age": self.age.value,
            "real_name": self.real_name.value,
            "playtime": self.playtime.value,
            "discovery": self.discovery.value
        }

        # Отправка в канал заявок
        channel_id = interaction.client.application_channel.get(interaction.guild.id)
        if channel_id:
            channel = interaction.guild.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed, view=view)

        await interaction.followup.send("✅ Ваша заявка успешно отправлена!", ephemeral=True)

class ModerationView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.application_data = {}

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Проверяем, есть ли у пользователя нужные роли
        user_roles = [role.id for role in interaction.user.roles]
        return any(role in MOD_ROLES for role in user_roles)

    @discord.ui.button(label="📞 Вызвать на обзвон", style=discord.ButtonStyle.blurple, custom_id="call_interview")
    async def call_interview(self, interaction: discord.Interaction, button: Button):
        embed = interaction.message.embeds[0]
        embed.color = 0x3498db
        embed.set_footer(text="Ludoman clnx • Вызван на обзвон")

        # Отправляем уведомление пользователю
        user = interaction.guild.get_member(self.application_data["user_id"])
        if user:
            try:
                notify_embed = discord.Embed(
                    title="📞 Вызов на обзвон",
                    description=f"**Вы вызваны на обзвон в семью Ludoman clnx!**\n\n"
                              f"Пожалуйста, зайдите в любой открытый голосовой канал.\n"
                              f"Ожидайте подключения модератора.",
                    color=0x3498db
                )
                notify_embed.set_footer(text="Ludoman clnx • Удачи на собеседовании!")
                await user.send(embed=notify_embed)
            except:
                pass

        await interaction.message.edit(embed=embed)
        await interaction.response.send_message("✅ Пользователь вызван на обзвон!", ephemeral=True)

    @discord.ui.button(label="✅ Одобрено", style=discord.ButtonStyle.success, custom_id="approve")
    async def approve(self, interaction: discord.Interaction, button: Button):
        embed = interaction.message.embeds[0]
        embed.color = 0x2ecc71
        embed.set_footer(text="Ludoman clnx • Заявка одобрена")

        # Отправляем уведомление пользователю
        user = interaction.guild.get_member(self.application_data["user_id"])
        if user:
            try:
                notify_embed = discord.Embed(
                    title="🎉 Поздравляем!",
                    description=f"**Ваша заявка в семью Ludoman clnx одобрена!**\n\n"
                              f"Добро пожаловать в нашу семью!\n"
                              f"Ожидайте дальнейших инструкций от администрации.",
                    color=0x2ecc71
                )
                notify_embed.set_footer(text="Ludoman clnx • Рады видеть тебя в семье!")
                await user.send(embed=notify_embed)
            except:
                pass

        # Отключаем все кнопки
        for child in self.children:
            child.disabled = True
        self.stop()

        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.send_message("✅ Заявка одобрена!", ephemeral=True)

    @discord.ui.button(label="❌ Отказано", style=discord.ButtonStyle.danger, custom_id="deny")
    async def deny(self, interaction: discord.Interaction, button: Button):
        # Модальное окно для указания причины отказа
        modal = DenyModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.reason.value:
            embed = interaction.message.embeds[0]
            embed.color = 0xe74c3c
            embed.add_field(name="📝 Причина отказа", value=modal.reason.value, inline=False)
            embed.set_footer(text="Ludoman clnx • Заявка отклонена")

            # Отправляем уведомление пользователю
            user = interaction.guild.get_member(self.application_data["user_id"])
            if user:
                try:
                    notify_embed = discord.Embed(
                        title="😔 Заявка отклонена",
                        description=f"**К сожалению, ваша заявка в семью Ludoman clnx отклонена.**\n\n"
                                  f"**Причина:** {modal.reason.value}\n\n"
                                  f"Вы можете подать новую заявку через 30 дней.",
                        color=0xe74c3c
                    )
                    notify_embed.set_footer(text="Ludoman clnx • Удачи в будущем!")
                    await user.send(embed=notify_embed)
                except:
                    pass

            # Отключаем все кнопки
            for child in self.children:
                child.disabled = True
            self.stop()

            await interaction.message.edit(embed=embed, view=self)

class DenyModal(Modal, title="Укажите причину отказа"):
    reason = TextInput(
        label="Причина отказа",
        placeholder="Пример: Не подходит по возрасту / Недостаточный опыт",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

class ApplicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.application_channel = {}

    @app_commands.command(name="набор", description="Открыть набор в семью")
    @app_commands.describe(channel="Канал для отправки заявок")
    async def setup_applications(self, interaction: discord.Interaction, channel: discord.TextChannel):
        # Проверка ролей
        user_roles = [role.id for role in interaction.user.roles]
        if not any(role in MOD_ROLES for role in user_roles):
            embed = discord.Embed(
                title="❌ Ошибка доступа",
                description="У вас недостаточно прав для использования этой команды!",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Сохраняем ID канала для заявок
        self.bot.application_channel[interaction.guild.id] = channel.id

        # Создаем красивое меню заявок
        embed = discord.Embed(
            title="🎲 **ОТКРЫТ НАБОР В LUDOMAN CLNX** 🎲",
            description="",
            color=0x9b59b6
        )

        embed.add_field(
            name="🌟 **ПОЧЕМУ МЫ?**",
            value="""```diff
+ 🎭 Здоровый коллектив без токсичности
+ 🎮 Постоянный контент и ивенты
+ 🎲 Профессиональные игроки в кости
+ 🎁 Регулярные розыгрыши и подарки
+ 👥 Активное комьюнити 24/7
+ 💼 Поддержка и развитие игроков```""",
            inline=False
        )

        embed.add_field(
            name="📋 **ТРЕБОВАНИЯ:**",
            value="""```yaml
• Возраст: 16+
• Микрофон: Обязательно
• Активность: 3+ часа в день
• Адекватность: 100%
• Уважение к другим```""",
            inline=False
        )

        embed.add_field(
            name="🎯 **ЧТО МЫ ПРЕДЛАГАЕМ:**",
            value="""```fix
✓ Стабильный заработок в игре
✓ Помощь опытных игроков
✓ Защиту и поддержку семьи
✓ Участие в ивентах
✓ Карьерный рост в семье```""",
            inline=False
        )

        embed.set_thumbnail(url="https://i.imgur.com/3JQ2p8A.png")
        embed.set_image(url="https://i.imgur.com/VkQXwzG.png")
        embed.set_footer(text="Ludoman Family • Создатель: Mason")

        # Создаем кнопку для подачи заявки
        class ApplicationButton(Button):
            def __init__(self):
                super().__init__(label="📝 Подать заявку", style=discord.ButtonStyle.primary, custom_id="apply_button")

            async def callback(self, interaction: discord.Interaction):
                modal = ApplicationModal()
                await interaction.response.send_modal(modal)

        view = View()
        view.add_item(ApplicationButton())

        await channel.send(embed=embed, view=view)

        # Подтверждение
        confirm_embed = discord.Embed(
            title="✅ Набор открыт!",
            description=f"Система заявок настроена в канале {channel.mention}",
            color=0x2ecc71
        )
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ApplicationCog(bot))
