import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
from collections import deque

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
SONG_QUEUE = {}


# --- YT-DLP Helper Functions ---
async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))


def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)


# --- Events ---
@bot.event
async def on_ready():
    print(f'Successfully connected as {bot.user}')
    try:
        sync = await bot.tree.sync()
    except Exception as e:
        print(f"Error: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_text = message.content.lower()

    if 'hello' in user_text:
        await message.channel.send('i hate you')
    if 'why' in user_text:
        await message.channel.send('you have taken everything from me')
    if 'paralelepipedo' in user_text:
        await message.channel.send('pq vc e assim')
    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        return

    voice_client = member.guild.voice_client
    if voice_client is None:
        return
    if len(voice_client.channel.members) == 1:
        await asyncio.sleep(60)
        # Check again after 60 seconds
        if voice_client.channel and len(voice_client.channel.members) == 1:
            await voice_client.disconnect()

def play_next(guild: discord.Guild, text_channel: discord.TextChannel):
    guild_id = str(guild.id)

    voice_client = guild.voice_client

    if voice_client and guild_id in SONG_QUEUE and len(SONG_QUEUE[guild_id]) > 0:
        audio_url, title = SONG_QUEUE[guild_id].popleft()

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_on_network_error 1',
            'options': '-vn -loglevel warning'
        }

        source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)

        voice_client.play(source, after=lambda e: play_next(guild, text_channel))

        coro = text_channel.send(f"🎶 Now playing: **{title}**")

        #coroutine to the bot's background loop
        asyncio.run_coroutine_threadsafe(coro, bot.loop)


@bot.tree.command(name="ping", description="Checks the bot's current latency")
async def latency(interaction: discord.Interaction):
    await interaction.response.send_message(f"My current latency is {round(bot.latency * 1000)} ms")


@bot.tree.command(name="play", description="Plays your desired song (Youtube link required)")
@app_commands.describe(song_query="Youtube link please !")
async def play_song(interaction: discord.Interaction, song_query: str):
    if interaction.user.voice is None:
        await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
        return

    user_voice = interaction.user.voice.channel

    await interaction.response.defer()
    voice_client = await join_in(interaction.guild, user_voice)
    if voice_client is None:
        await interaction.followup.send("Error connecting to voice channel")
        return

    ydl_options = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False
    }

    query = "ytsearch1: " + song_query

    res = await search_ytdlp_async(query, ydl_options)
    songs = res.get("entries", [])

    if not songs:
        await interaction.followup.send("No songs found. Bruh")
        return

    first_song = songs[0]
    audio_url = first_song["url"]
    title = first_song.get("title", "untitled")
    guild_id = str(interaction.guild.id)
    await interaction.followup.send(f"🔎 Searching for:{title}")
    if SONG_QUEUE.get(guild_id) is None:
        SONG_QUEUE[guild_id] = deque()

    SONG_QUEUE[guild_id].append((audio_url, title))
    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"✅ Added to queue: **{title}**")
    else:
        play_next(interaction.guild, interaction.channel)



async def join_in(guild: discord.Guild, user_voice: discord.VoiceChannel):
    if user_voice is None:
        return None
    voice_client = guild.voice_client
    if voice_client is None:
        voice_client = await user_voice.connect()
    elif voice_client.channel != user_voice:
        voice_client = await voice_client.move_to(user_voice)
    return voice_client



@bot.tree.command(name="test", description="The bot will say hello to you!")
@app_commands.describe(name="Who are we saying hello to?")
async def hello(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello there, {name}!")


@bot.tree.command(name="skip", description="Will skip the current track!")
async def skip(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
        return

    voice_client = interaction.guild.voice_client

    if voice_client is None or not voice_client.is_playing():
        await interaction.response.send_message("There is nothing playing to skip!", ephemeral=True)
        return

    guild_id = str(interaction.guild.id)

    voice_client.stop()

    if guild_id not in SONG_QUEUE or len(SONG_QUEUE[guild_id]) == 0:
        await interaction.response.send_message("⏭️ Skipped! The queue is now empty.")
    else:
        await interaction.response.send_message("⏭️ Skipped! Loading the next track...")
@bot.tree.command(name="pause", description="Pauses the current track!")
async def pause(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
        return
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("⏸️ Audio paused.")
    else:
        await interaction.response.send_message("There is no audio playing right now!", ephemeral=True)
@bot.tree.command(name="resume", description="Resumes the current track!")
async def resume(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
        return
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("▶️ Audio resumed.")
    else:
        await interaction.response.send_message("The audio is not paused!", ephemeral=True)
@bot.tree.command(name="clear", description="Stops the audio and clears the queue")
async def stop(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("You are not connected to a voice channel !!", ephemeral=True)
        return

    voice_client = interaction.guild.voice_client
    guild_id = str(interaction.guild.id)
    if guild_id in SONG_QUEUE:
        SONG_QUEUE[guild_id].clear()

    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
        await interaction.response.send_message("⏹️ Audio stopped and queue cleared.")
    else:
        await interaction.response.send_message("There is no audio playing right now!", ephemeral=True)

bot.run('lmao')
