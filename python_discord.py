import discord, json

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
            await message.channel.send(x)


client.run(config.get("discordclientlogin"))
