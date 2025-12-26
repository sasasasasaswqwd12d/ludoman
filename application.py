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
            title="🎲 НОВАЯ ЗАЯВКА В LUDOMAN CLNX",
            color=0x00ff00,
            timestamp=datetime.now()
        )

        embed.add_field(name="👤 Никнейм", value=f"```{self.nickname.value}```", inline=True)
        embed.add_field(name="🆔 Static ID", value=f"```{self.static_id.value}```", inline=True)
        embed.add_field(name="🎂 Возраст", value=f"```{self.age.value}```", inline=True)
        embed.add_field(name="📛 Реальное имя", value=f"```{self.real_name.value}```", inline=True)
        embed.add_field(name="⏰ Время в игре", value=f"```{self.playtime.value}```", inline=True)
        embed.add_field(name="📢 Откуда узнал", value=f"```{self.discovery.value}```", inline=True)
        embed.add_field(name="👤 Подавший", value=f"{interaction.user.mention}\nID: {interaction.user.id}", inline=False)

        if interaction.user.avatar:
            embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.set_footer(text="Ludoman clnx • Заявка ожидает рассмотрения")

        # Кнопки для модерации
        view = ModerationView()
        view.application_data = {
            "user_id": interaction.user.id,
            "user": interaction.user,
            "nickname": self.nickname.value,
            "static_id": self.static_id.value,
            "age": self.age.value,
            "real_name": self.real_name.value,
            "playtime": self.playtime.value,
            "discovery": self.discovery.value
        }

        # Отправка в канал для заявок (из сохраненного в команде /набор)
        bot = interaction.client
        channel_id = bot.applications_target_channel.get(interaction.guild.id)

        if channel_id:
            target_channel = interaction.guild.get_channel(channel_id)
            if target_channel:
                message = await target_channel.send(embed=embed, view=view)
                view.message_id = message.id

        await interaction.followup.send("✅ Ваша заявка успешно отправлена на рассмотрение!", ephemeral=True)

class ModerationView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.application_data = {}
        self.message_id = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Проверяем, есть ли у пользователя нужные роли
        user_roles = [role.id for role in interaction.user.roles]
        return any(role in MOD_ROLES for role in user_roles)

    @discord.ui.button(label="📞 Вызвать на обзвон", style=discord.ButtonStyle.blurple, custom_id="call_interview", emoji="📞")
    async def call_interview(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()

        embed = interaction.message.embeds[0]
        embed.color = 0x3498db
        embed.set_footer(text="Ludoman clnx • Вызван на обзвон")

        # Отправляем уведомление пользователю
        user = self.application_data.get("user")
        if user:
            try:
                notify_embed = discord.Embed(
                    title="📞 ВЫЗОВ НА ОБЗВОН",
                    description=f"**Приветствуем, {self.application_data['nickname']}!**\n\n"
                              f"🎯 **Ты вызван на обзвон в семью Ludoman clnx!**\n\n"
                              f"**📍 Что нужно сделать:**\n"
                              f"• Зайди в любой открытый голосовой канал\n"
                              f"• Ожидай подключения модератора\n"
                              f"• Будь готов ответить на вопросы\n\n"
                              f"**⏰ Время ожидания:** до 15 минут\n"
                              f"**🎙️ Микрофон:** обязателен",
                    color=0x3498db
                )
                notify_embed.set_footer(text="Ludoman Family • Удачи на собеседовании! 🎲")
                await user.send(embed=notify_embed)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю: {e}")
                await interaction.followup.send(f"⚠️ Не удалось отправить уведомление пользователю {user.mention}", ephemeral=True)

        await interaction.message.edit(embed=embed)

        success_embed = discord.Embed(
            title="✅ Вызов отправлен!",
            description=f"Пользователь {user.mention if user else 'Unknown'} вызван на обзвон.",
            color=0x3498db
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)

    @discord.ui.button(label="✅ Одобрено", style=discord.ButtonStyle.success, custom_id="approve", emoji="✅")
    async def approve(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()

        embed = interaction.message.embeds[0]
        embed.color = 0x2ecc71
        embed.set_footer(text="Ludoman clnx • Заявка одобрена ✅")

        # Отправляем уведомление пользователю
        user = self.application_data.get("user")
        if user:
            try:
                notify_embed = discord.Embed(
                    title="🎉 ПОЗДРАВЛЯЕМ! ЗАЯВКА ОДОБРЕНА! 🎉",
                    description=f"**Дорогой {self.application_data['real_name']},**\n\n"
                              f"🌟 **Твоя заявка в семью Ludoman clnx одобрена!**\n\n"
                              f"**📋 Дальнейшие шаги:**\n"
                              f"1. Ожидай приглашения в семью\n"
                              f"2. Получи роли и доступы\n"
                              f"3. Ознакомься с правилами\n"
                              f"4. Присоединяйся к игре\n\n"
                              f"**🎲 Добро пожаловать в семью!**\n"
                              f"Готовь кости, начинается магия!",
                    color=0x2ecc71
                )
                notify_embed.set_footer(text="Ludoman Family • Рады видеть тебя в семье! 💫")
                await user.send(embed=notify_embed)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю: {e}")
                await interaction.followup.send(f"⚠️ Не удалось отправить уведомление пользователю {user.mention}", ephemeral=True)

        # Отключаем все кнопки
        for child in self.children:
            child.disabled = True

        await interaction.message.edit(embed=embed, view=self)

        success_embed = discord.Embed(
            title="✅ Заявка одобрена!",
            description=f"Пользователь {user.mention if user else 'Unknown'} принят в семью.",
            color=0x2ecc71
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)

    @discord.ui.button(label="❌ Отказано", style=discord.ButtonStyle.danger, custom_id="deny", emoji="❌")
    async def deny(self, interaction: discord.Interaction, button: Button):
        # Модальное окно для указания причины отказа
        modal = DenyModal()
        await interaction.response.send_modal(modal)

        # Ждем завершения модального окна
        if await modal.wait():
            return

        embed = interaction.message.embeds[0]
        embed.color = 0xe74c3c
        embed.add_field(name="📝 Причина отказа", value=f"```{modal.reason.value}```", inline=False)
        embed.set_footer(text="Ludoman clnx • Заявка отклонена ❌")

        # Отправляем уведомление пользователю
        user = self.application_data.get("user")
        if user:
            try:
                notify_embed = discord.Embed(
                    title="😔 ЗАЯВКА ОТКЛОНЕНА",
                    description=f"**Дорогой {self.application_data['real_name']},**\n\n"
                              f"К сожалению, твоя заявка в семью Ludoman clnx была отклонена.\n\n"
                              f"**📌 Причина отказа:**\n"
                              f"```{modal.reason.value}```\n\n"
                              f"**🔄 Что дальше?**\n"
                              f"• Ты можешь подать новую заявку через 30 дней\n"
                              f"• Исправь указанные недостатки\n"
                              f"• Удачи в будущем!",
                    color=0xe74c3c
                )
                notify_embed.set_footer(text="Ludoman Family • Не расстраивайся, всё получится! 💪")
                await user.send(embed=notify_embed)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю: {e}")
                await interaction.followup.send(f"⚠️ Не удалось отправить уведомление пользователю {user.mention}", ephemeral=True)

        # Отключаем все кнопки
        for child in self.children:
            child.disabled = True

        await interaction.message.edit(embed=embed, view=self)

class DenyModal(Modal, title="📝 Укажите причину отказа"):
    reason = TextInput(
        label="Причина отказа",
        placeholder="Пример: Не подходит по возрасту / Недостаточный опыт игры / Не отвечал на вопросы",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Ошибка! Что-то пошло не так.', ephemeral=True)

class ApplicationButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📝 ПОДАТЬ ЗАЯВКУ", style=discord.ButtonStyle.primary, custom_id="apply_button", emoji="📝")
    async def apply_button(self, interaction: discord.Interaction, button: Button):
        modal = ApplicationModal()
        await interaction.response.send_modal(modal)

class ApplicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.applications_target_channel = {}  # Канал КУДА отправлять заявки

    @app_commands.command(name="набор", description="Открыть набор в семью Ludoman clnx")
    @app_commands.describe(target_channel="Канал КУДА будут отправляться заявки")
    async def setup_applications(self, interaction: discord.Interaction, target_channel: discord.TextChannel):
        # Проверка ролей
        user_roles = [role.id for role in interaction.user.roles]
        if not any(role in MOD_ROLES for role in user_roles):
            error_embed = discord.Embed(
                title="🚫 ДОСТУП ЗАПРЕЩЕН",
                description="**У вас недостаточно прав для использования этой команды!**\n\n"
                          "Требуемые роли:\n"
                          f"• <@&1454210800813346968>\n"
                          f"• <@&1454210803472400404>",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        # Сохраняем ID канала КУДА отправлять заявки
        self.bot.applications_target_channel[interaction.guild.id] = target_channel.id

        # Создаем красивое меню заявок в ТЕКУЩЕМ канале (где написана команда)
        embed = discord.Embed(
            title="🎲 **ОТКРЫТ НАБОР В LUDOMAN CLNX** 🎲",
            description="*Добро пожаловать в самую азартную семью на проекте!*\n",
            color=0x9b59b6
        )

        embed.add_field(
            name="🌟 **ПРЕИМУЩЕСТВА НАШЕЙ СЕМЬИ:**",
            value="""```diff
+ 🎭 Здоровый коллектив без токсичности
+ 🎮 Постоянный контент и ивенты
+ 🎲 Профессиональные игроки в кости
+ 🎁 Регулярные розыгрыши и подарки
+ 👥 Активное комьюнити 24/7
+ 💼 Поддержка и развитие игроков
+ 🏆 Турниры и соревнования
+ 🛡️ Защита и безопасность```""",
            inline=False
        )

        embed.add_field(
            name="📋 **ТРЕБОВАНИЯ К КАНДИДАТАМ:**",
            value="""```yaml
Возраст: 16+ лет
Микрофон: Обязательно
Активность: 3+ часа в день
Адекватность и уважение
Готовность учиться
Следование правилам```""",
            inline=False
        )

        embed.add_field(
            name="🎯 **ПРОЦЕСС ОТБОРА:**",
            value="""1️⃣ **Подача заявки** (форма ниже)\n"""
                 """2️⃣ **Проверка анкеты** модераторами\n"""
                 """3️⃣ **Обзвон** в голосовом канале\n"""
                 """4️⃣ **Принятие решения**\n"""
                 """5️⃣ **Вступление в семью**""",
            inline=False
        )

        embed.add_field(
            name="📊 **СТАТИСТИКА СЕМЬИ:**",
            value="""• **Активных игроков:** 50+\n"""
                 """• **Онлайн ежедневно:** 20-30\n"""
                 """• **Средний заработок:** 100к+ в день\n"""
                 """• **Успешных заявок:** 85%\n"""
                 """• **Время рассмотрения:** 1-24 часа""",
            inline=False
        )

        embed.add_field(
            name="📝 **КАК ПОДАТЬ ЗАЯВКУ:**",
            value="**Нажми кнопку ниже** и заполни анкету. Будь честен и подробен в ответах!",
            inline=False
        )

        embed.set_footer(text="Ludoman Family • Создатель: Mason • Заявки отправляются в отдельный канал")

        # Создаем кнопку для подачи заявки
        view = ApplicationButtonView()

        # Отправляем в ТЕКУЩИЙ канал
        await interaction.response.send_message("✅ Система заявок настроена!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=view)

        # Логирование
        print(f"[НАБОР] Набор открыт в канале {interaction.channel.name}")
        print(f"[НАБОР] Заявки будут отправляться в {target_channel.name}")

async def setup(bot):
    await bot.add_cog(ApplicationCog(bot))
