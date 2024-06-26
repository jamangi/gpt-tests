from decouple import config
import discord
from discord.ext import commands
from session_manager import SessionManager
from decider import Decider
from time import sleep
from discord.member import Member

bot = commands.Bot(command_prefix=None, intents=discord.Intents.all())
decider = Decider()
conversation = [{"role": "user", "content": f'[Raspberry Kitten] Are you there {config("NAME")}?'},
                {"role": "assistant", "content": "Yes I'm here!"},]
session_manager = SessionManager(decider, conversation)


@bot.event
async def on_ready():
    print("ready")


@bot.event
async def on_message(message):
    # print(f"message received: {message}")
    # print(message.content)
    if message.author == bot.user or message.author.bot:
        session_manager.process_bot_message(message.content)
    else:
        username = getattr(message.author, 'display_name', message.author.name)
        content = f'{message.content}'
        if decider.name.lower() in content.lower():
            content = f'{username}: {message.content}'
            result = session_manager.process_user_message(content)
            if result and not message.reference and (not message.mentions or bot.user in message.mentions):
                sleep(3)
                await message.channel.send(result)
        else:
            session_manager.conversation.append({"role": "user", "content": content})



if __name__ == "__main__":
    # intents = discord.Intents.default()
    # intents.message_content = True
    # bot = interactions.Client(token=config("BOT_TOKEN"), intents=intents)
    bot.run(token=config("BOT_TOKEN"))

