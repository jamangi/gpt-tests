from demo import generate
from decouple import config
from interactions import listen
import interactions
import discord
from discord.ext import commands
from session_manager import SessionManager
from decider import Decider

bot = commands.Bot(command_prefix=None, intents=discord.Intents.all())
decider = Decider()
conversation = []
session_manager = SessionManager(decider, conversation)


@bot.event
async def on_ready():
    print("ready")


@bot.event
async def on_message(message):
    # print(f"message received: {message}")
    # print(message.content)
    if message.author == bot.user:
        session_manager.process_bot_message(message.content)
    else:
        username = message.author.name
        content = f'[{username}] {message.content}'
        result = session_manager.process_user_message(content)
        if result:
            await message.channel.send(result)



if __name__ == "__main__":
    # intents = discord.Intents.default()
    # intents.message_content = True
    # bot = interactions.Client(token=config("BOT_TOKEN"), intents=intents)
    bot.run(token=config("BOT_TOKEN"))

# print(generate("How are you?"))