import asyncio
import os
from globals.bot import bot
from dotenv import load_dotenv

INITIAL_EXTENSIONS = [
    'globals.connection.ready',
    'globals.events.voice.voice',
    'globals.events.message.on_message',
    'youtube.commands.music_commands',
    'youtube.core.song_core'
]
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

async def load_extensions():
    for extension in INITIAL_EXTENSIONS:
        try:
            await bot.load_extension(extension)
            print(f"Successfully loaded: {extension}")
        except Exception as e:
            print(f"Failed to load {extension}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass