import discord, json
import subprocess
from python_app.get_animes_and_mangas import all_embeds, load_all_embeds
from python_app.get_league_matches import get_games

client = discord.Client()

with open('configuration.json') as json_file :
    config = json.load(json_file)


@client.event
async def on_message(message):
    if message.content.startswith('!weeb'):
        load_all_embeds()
        for embed in all_embeds:
            await message.channel.send(embed=embed)
        all_embeds.clear()

    if message.content.startswith('!league'):
        future_games = get_games(8)
        for x in future_games:
            await message.channel.send(embed=x)

    if message.content.startswith('!test'):
        await message.channel.send("hello")

subprocess.Popen(["python3","python_app/live_youtube_check.py"])
subprocess.Popen(["python3","python_app/get_twitch_live.py"])
subprocess.Popen(["python3","python_app/post_anime_episode_updates.py"])
    
client.run(config.get("discordclientlogin"))
