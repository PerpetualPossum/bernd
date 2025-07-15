import random

import discord
from bernd.constants import DISCORD_TOKEN
from bernd.translate import translate_from_german

from discord import app_commands
from bernd.constants import DATABASE
from bernd.database.models import GuildSetting


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)


@tree.command(name="ping", description="Replies with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@tree.command(name="response_mode", description="Set the response mode for the bot")
@app_commands.choices(
    mode=[
        app_commands.Choice(name="single", value="single"),
        app_commands.Choice(name="full", value="full"),
    ]
)
async def response_mode(
    interaction: discord.Interaction, mode: app_commands.Choice[str]
):
    if not interaction.guild or not interaction.guild.id:
        await interaction.response.send_message(
            "This command can only be used in a server."
        )
        return
    try:
        with DATABASE.atomic():
            user, _ = GuildSetting.get_or_create(guild_id=interaction.guild.id)
            user.response_mode = mode.value
            user.save()
        await interaction.response.send_message(f"Response mode set to {mode.name}.")
    except Exception as e:
        await interaction.response.send_message(
            f"Error setting response mode, please let viv know"
        )
        print(f"Error setting response mode: {e}")


@tree.command(name="chaos_level", description="Set the chaos level for the bot")
@app_commands.choices(
    level=[
        app_commands.Choice(name="1", value=1),
        app_commands.Choice(name="2", value=2),
        app_commands.Choice(name="3", value=3),
    ]
)
async def chaos_level(
    interaction: discord.Interaction, level: app_commands.Choice[int]
):
    if not interaction.guild or not interaction.guild.id:
        await interaction.response.send_message(
            "This command can only be used in a server."
        )
        return
    try:
        with DATABASE.atomic():
            user, _ = GuildSetting.get_or_create(guild_id=interaction.guild.id)
            user.chaos_level = level.value
            user.save()
        await interaction.response.send_message(f"Chaos level set to {level.name}.")
    except Exception as e:
        await interaction.response.send_message(
            f"Error setting chaos level, please let viv know"
        )
        print(f"Error setting chaos level: {e}")


@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.author.bot:
        return
    if not message.guild or not message.guild.id:
        return
    try:
        guild_setting = GuildSetting.get(guild_id=message.guild.id)
    except GuildSetting.DoesNotExist:  # type: ignore
        guild_setting = GuildSetting.create(guild_id=message.guild.id)

    german_words = await translate_from_german(message.content, guild_setting)
    if len(german_words) > 0:
        if guild_setting.response_mode == "single":
            # Pick a random word from the translated list
            random_word = random.choice(german_words)
            await message.channel.send(random_word)
        elif guild_setting.response_mode == "full":
            await message.channel.send(" ".join(german_words))


def start_bot():
    print("Starting bot...")
    client.run(DISCORD_TOKEN)
