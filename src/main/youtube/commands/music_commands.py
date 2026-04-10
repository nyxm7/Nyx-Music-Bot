import discord
from discord.ext import commands
from discord import app_commands

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="skip", description="Will skip the current track!")
    async def skip(self,interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
            return

        voice_client = interaction.guild.voice_client
        queue = self.bot.song_queue

        if voice_client is None or not voice_client.is_playing():
            await interaction.response.send_message("There is nothing playing to skip!", ephemeral=True)
            return

        guild_id = str(interaction.guild.id)

        voice_client.stop()

        if guild_id not in queue or len(queue[guild_id]) == 0:
            await interaction.response.send_message("⏭️ Skipped! The queue is now empty.")
        else:
            await interaction.response.send_message("⏭️ Skipped! Loading the next track...")

    @app_commands.command(name="pause", description="Pauses the current track!")
    async def pause(self,interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
            return
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("⏸️ Audio paused.")
        else:
            await interaction.response.send_message("There is no audio playing right now!", ephemeral=True)

    @app_commands.command(name="resume", description="Resumes the current track!")
    async def resume(self,interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
            return
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("▶️ Audio resumed.")
        else:
            await interaction.response.send_message("The audio is not paused!", ephemeral=True)

    @app_commands.command(name="clear", description="Stops the audio and clears the queue")
    async def stop(self,interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
            return
        queue = self.bot.song_queue
        voice_client = interaction.guild.voice_client
        guild_id = str(interaction.guild.id)
        if guild_id in queue:
            queue[guild_id].clear()

        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            voice_client.stop()
            await interaction.response.send_message("⏹️ Audio stopped and queue cleared.")
        else:
            await interaction.response.send_message("There is no audio playing right now!", ephemeral=True)
async def setup(bot):
    await bot.add_cog(MusicCommands(bot))