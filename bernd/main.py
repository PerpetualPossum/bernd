import discord
import os
from bernd.translate import translate_from_german
import random

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    german_words = await translate_from_german(message.content)
    if len(german_words) > 0:
        # Pick a random word from the translated list
        random_word = random.choice(german_words)
        await message.channel.send(random_word)


client.run(DISCORD_TOKEN)
