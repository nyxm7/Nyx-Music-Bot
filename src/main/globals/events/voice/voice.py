import discord
from discord.ext import commands
import asyncio
class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.bot.user.id:
            return

        voice_client = member.guild.voice_client
        if voice_client is None:
            return
        if len(voice_client.channel.members) == 1:
            await asyncio.sleep(60)
            # Check again after 60 seconds
            if voice_client.channel and len(voice_client.channel.members) == 1:
                await voice_client.disconnect()
async def setup(bot):
    await bot.add_cog(voice(bot))

async def join_in(guild: discord.Guild, user_voice: discord.VoiceChannel):
    if user_voice is None:
        return None
    voice_client = guild.voice_client
    if voice_client is None:
        voice_client = await user_voice.connect()
    elif voice_client.channel != user_voice:
        voice_client = await voice_client.move_to(user_voice)
    return voice_client
