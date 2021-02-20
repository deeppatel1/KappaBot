import discord
from discord.ext import commands
import subprocess
import json

from discord.ext.commands.bot import Bot

with open('configuration.json') as json_file :
    config = json.load(json_file)

bot = commands.Bot(command_prefix="$")

@bot.command()
async def zclean(client):
    print('entere dzClean')
    known_names = ["python_discord.py", "live_youtube_check.py", "get_twitch_live.py", "post_anime_episode_updates.py", "tweet_posts.py"]

    for python_script in known_names:
        #pkill -9 -f script.py
        output = subprocess.run(["sudo", "pkill", "-9", "-f", python_script], capture_output=True).stdout.decode('UTF-8')

    os.system('cd /home/kapp/KappaBot/KappaBot/ && python3 python_discord.py')
    await client.send("done")

bot.run(config.get("discordclientlogin"))