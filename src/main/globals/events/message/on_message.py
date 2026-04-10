import discord
from discord.ext import commands
from discord import app_commands
class on_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user_text = message.content.lower()

        if 'hello' in user_text:
            await message.channel.send('i hate you')
        if 'why' in user_text:
            await message.channel.send('you have taken everything from me')
        if 'paralelepipedo' in user_text:
            await message.channel.send('pq vc e assim')

    @app_commands.command(name="ping", description="Checks the bot's current latency")
    async def latency(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"My current latency is {round(self.bot.latency * 1000)} ms")

    @app_commands.command(name="test", description="The bot will say hello to you!")
    @app_commands.describe(name="Who are we saying hello to?")
    async def hello(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"Hello there, {name}!")
async def setup(bot):
    await bot.add_cog(on_message(bot))