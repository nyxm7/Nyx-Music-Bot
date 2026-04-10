from discord.ext import commands
class ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.tree.sync()
            print(f'Successfully connected as {self.bot.user}')
        except Exception as e:
            print(f"Error: {e}")
async def setup(bot):
    await bot.add_cog(ready(bot))