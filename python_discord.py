import discord, json
import subprocess
import requests
from bs4 import BeautifulSoup, SoupStrainer
from python_app.get_animes_and_mangas import all_embeds, load_all_embeds
from python_app.get_league_matches import get_future_league_games
from python_app.streamers_tracker import ice, deep, tt
from python_app.post_discord_webhook import sendWebhookMessage, sendWebhookListEmbeds, send_the_message

client = discord.Client()

with open('configuration.json') as json_file :
    config = json.load(json_file)

def create_webhook_url(id, token):
    return "https://discordapp.com/api/webhooks/" + str(id) + "/" + str(token)

@client.event
async def on_message(message):
    if message.content.startswith('!weeb'):
        load_all_embeds()
        channels = await message.channel.webhooks()
        send_the_message(username="anime updates", \
            webhook=create_webhook_url(channels[0].id, channels[0].token), \
            avatar_url="https://media.discordapp.net/attachments/306941063497777152/792210065523998740/image.png", \
            embeds=all_embeds)

        # sendWebhookListEmbeds(username="Anime Updates", \
        #     avatar_url="https://media.discordapp.net/attachments/306941063497777152/792210065523998740/image.png", \
        #     embeds=all_embeds)
        # for embed in all_embeds:
        #     await message.channel.send(embed=embed)
        all_embeds.clear()

    if message.content.startswith('!league'):
        future_games, future_embeds = get_future_league_games()
        for x in range(0, len(future_games)):
            if x < 5:
                await message.channel.send(future_games[x])
                await message.channel.send(embed=future_embeds[x])
        # future_games = get_games(8)
        # print(future_games)
        # channels = await message.channel.webhooks()
        # send_the_message(username="tip top league gameplay", \
        #     webhook=create_webhook_url(channels[0].id, channels[0].token), \
        #     avatar_url="https://media.discordapp.net/attachments/306941063497777152/792210065523998740/image.png", \
        #     embeds=future_games)

        # for x in future_games:
        #     await message.channel.send(embeds=x)

    if message.content.startswith('!live'):
        update_viewer_counts()
        
        streamers_to_post_about = [ice, deep]

        for streamer in streamers_to_post_about:
            status = "online" if streamer["online"] else "offline"
            url = None
            if streamer["online"]:
                url = streamer["youtube.com/watch?v="] + streamer["video_id"]
            await message.channel.send(streamer["name"] + " is " + status + ", with " + streamer["viewer_count"] + " viewers " + url)

    if message.content.startswith('!test'):
        await message.channel.send("hello")

# subprocess.Popen(["python3","python_app/live_youtube_check.py"])
# subprocess.Popen(["python3","python_app/get_twitch_live.py"])
# subprocess.Popen(["python3","python_app/post_anime_episode_updates.py"])
    
client.run(config.get("discordclientlogin"))




STREAMS_TO_CHECK = [ice, deep]

def get_live_viewers(channel_id):
    url = "https://www.youtube.com/channel/" + channel_id
    content = requests.get(url).text
    soup = BeautifulSoup(content)
    raw = soup.findAll('script')

    if len(raw) < 29:
        return 0
    
    main_json_str = raw[27].text[20:-1]
    main_json = json.loads(main_json_str)

    if "channelFeaturedContentRenderer" not in main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]:
        # if it gets to here, user is live, need to get their URL
        return 0
    
    viewer_count = main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0]["videoRenderer"]["shortViewCountText"]["runs"][0]["text"]
        
    return viewer_count


def update_viewer_counts():
    for stream in STREAMS_TO_CHECK:
        print(stream)
        channel_id = stream.get("channel_id")

        viewer_count = get_live_viewers(channel_id)
        
        stream["viewer_count"] = viewer_count

