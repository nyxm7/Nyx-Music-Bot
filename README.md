# Nyx Bot
A Discord bot developed to play music and playlists directly from YouTube. The bot utilizes Discord's modern interface through Slash Commands.

## Features
**YouTube Playback:** Support for playing music directly from YouTube links or searches.

**Playlist Support:** Ability to load and queue complete YouTube playlists.

**Slash Commands:** Native interaction with Discord by typing /, which makes it easy to view available commands without the need for custom prefixes.

**Music Queue:** Queue management system (skip, pause, resume, stop).

## Dependencies
For the bot to work properly, download audio, and transmit it to voice channels, you must install the following tools in your environment.

### Python Libraries
Open your terminal and use the pip package manager to install the Discord API and the YouTube audio extractor (yt-dlp):

```
pip install discord.py yt-dlp
```
**FFmpeg**
FFmpeg is a mandatory external software to encode and process the audio track before sending it to Discord's voice servers. It must be installed directly on your operating system:

**Windows:** 
```
Download the binary files from the official FFmpeg website.
Extract the contents and add the path to the bin folder to your system's Environment Variables (PATH).
```
**Linux (Debian/Ubuntu):** 

```
sudo apt update
sudo apt install ffmpeg
```
**macOS (Homebrew):** 

```
brew install ffmpeg
```
## How to Configure and Use
Follow the steps below to register your bot on Discord, configure the credentials, and run it on your server.

### 1. Create the Bot on the Discord Developer Portal
For the bot to work, you need a registered application on Discord.

Access the Discord Developer Portal.

Click the New Application button in the top right corner.

Give your bot a name, accept the terms, and click Create.

In the left side menu, go to the Bot tab.

(Optional, but recommended) In the Privileged Gateway Intents section, enable the Message Content Intent and Server Members Intent options, then save the changes.

In the Token section, click Reset Token and then Copy to copy your bot's key. Never share this key publicly.

### 2. Invite the Bot to your Server
You need to generate an invite link with the correct permissions to add the bot to your server.

Still in the Developer Portal, go to the OAuth2 tab and then URL Generator in the side menu.

In the Scopes section, check the following boxes:
```
bot
applications.commands (Essential for Slash Commands to work)
```
A new section called Bot Permissions will appear just below. Check the minimum necessary permissions:
```
Text Permissions: Send Messages, Read Message History, Use Slash Commands.
Voice Permissions: Connect, Speak.
```
Copy the URL generated at the bottom of the page.

Paste the URL into your browser, select the desired server, and authorize the bot.

### 3. Configure the .env File
With the bot on the server and the Token in hand, configure the local development environment.

Clone this repository to your local machine.

In the root of the project folder, create a file named exactly .env.

Open the .env file and add the following line, pasting the token you copied in Step 1:
```
DISCORD_TOKEN="your_bot_key_here"
```
### 4. Run the Bot
With the environment variables configured, you can now start the system.

Make sure you have installed the necessary project dependencies.

Run the main application file.

```
python main.py
```
