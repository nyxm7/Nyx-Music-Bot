import discord
from discord.ext import commands
from src.main.youtube.ydl.ydl_helper import search_ytdlp_async
from src.main.globals.events.voice.voice import join_in
import asyncio
from discord import app_commands
from collections import deque
SONG_QUEUE = {}

class song_core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play", description="Plays your desired song (Youtube link required)")
    @app_commands.describe(song_query="Youtube link please !")
    async def play_song(self, interaction: discord.Interaction, song_query: str):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
            return

        user_voice = interaction.user.voice.channel
        await interaction.response.defer()

        voice_client = await join_in(interaction.guild, user_voice)
        if voice_client is None:
            await interaction.followup.send("Error connecting to voice channel")
            return

        # 1. FLAT EXTRACTION
        ydl_options = {
            'format': 'bestaudio/best',
            'extract_flat': 'in_playlist',
            'noplaylist': False,
            'ignoreerrors': True,
        }

        if song_query.startswith("http"):
            query = song_query
        else:
            query = f"ytsearch1:{song_query}"

        res = await search_ytdlp_async(query, ydl_options)

        if "entries" in res:
            songs = [s for s in res["entries"] if s is not None]
        else:
            songs = [res] if res else []

        if not songs:
            await interaction.followup.send("No song or playlist found. Bruh")
            return

        guild_id = str(interaction.guild.id)
        if SONG_QUEUE.get(guild_id) is None:
            SONG_QUEUE[guild_id] = deque()

        add_count = 0
        for s in songs:
            video_url = s.get("url")
            if video_url and not video_url.startswith("http"):
                video_url = f"https://www.youtube.com/watch?v={s.get('id', video_url)}"

            title = s.get("title", "untitled")

            if video_url:
                SONG_QUEUE[guild_id].append((video_url, title))
                add_count += 1

        if add_count == 1:
            await interaction.followup.send(f"✅ Added to queue: **{songs[0].get('title', 'untitled')}**")
        else:
            playlist_title = res.get("title", "Playlist")
            await interaction.followup.send(f"📑 Added **{add_count}** songs from **{playlist_title}** to the queue!")

        if not voice_client.is_playing() and not voice_client.is_paused():
            asyncio.run_coroutine_threadsafe(self.async_play_next(interaction.guild, interaction.channel),
                                             self.bot.loop)

    # 2. ASYNC PLAYER
    async def async_play_next(self, guild: discord.Guild, text_channel: discord.TextChannel):
        guild_id = str(guild.id)
        voice_client = guild.voice_client

        if voice_client and guild_id in SONG_QUEUE and len(SONG_QUEUE[guild_id]) > 0:
            video_url, title = SONG_QUEUE[guild_id].popleft()

            # Fetch the actual heavy audio stream URL for just this one song
            ydl_opts_single = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True
            }

            try:
                res = await search_ytdlp_async(video_url, ydl_opts_single)
                audio_stream_url = res['url']

                ffmpeg_options = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_on_network_error 1',
                    'options': '-vn -loglevel warning'
                }

                source = discord.FFmpegPCMAudio(audio_stream_url, **ffmpeg_options)


                def after_playing(error):
                    if error:
                        print(f"Player error: {error}")
                    asyncio.run_coroutine_threadsafe(self.async_play_next(guild, text_channel), self.bot.loop)

                voice_client.play(source, after=after_playing)
                await text_channel.send(f"🎶 Now playing: **{title}**")

            except Exception as e:
                await text_channel.send(f"⚠️ Error playing **{title}**. Skipping to next...")
                print(f"Extraction error: {e}")
                asyncio.run_coroutine_threadsafe(self.async_play_next(guild, text_channel), self.bot.loop)


async def setup(bot):
    await bot.add_cog(song_core(bot))