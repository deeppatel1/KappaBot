import discord, json
from discord.ext import commands
import subprocess
import os
import requests
import yfinance as yf
import importlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, SoupStrainer
from python_app.get_animes_and_mangas import all_embeds, load_all_embeds
from python_app.get_league_matches import get_future_league_games
from python_app.streamers_tracker import get_platform_streamers, get_everyone_online, update_viewer_count, get_top_stocks
from python_app.post_discord_webhook import sendWebhookMessage, sendWebhookListEmbeds, send_the_message

client = discord.Client()
bot = commands.Bot(command_prefix='$')

with open('configuration.json') as json_file :
    config = json.load(json_file)

def create_webhook_url(id, token):
    return "https://discordapp.com/api/webhooks/" + str(id) + "/" + str(token)

def update_youtube_view_count():     
    """
    Used for the !live command, get and update the live youtubers!
    """

    def get_live_viewers(channel_id):
        url = "https://www.youtube.com/channel/" + channel_id
        content = requests.get(url).text
        soup = BeautifulSoup(content)
        raw = soup.findAll('script')

        if len(raw) <= 28:
            return 0

        try:
            main_json_str = str(raw[27])[59:-10]
            main_json = json.loads(main_json_str)
        except:
            return 0 # return 0 if processing viewers failed

        if "channelFeaturedContentRenderer" not in main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]:
            # if it gets to here, user is live, need to get their URL
            return 0
        
        viewer_count = main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0]["videoRenderer"]["shortViewCountText"]["runs"][0]["text"]

        return viewer_count

    for streamer in get_platform_streamers("youtube"):
        name = streamer[0]
        channel_id = streamer[1]
        if name == "ice":
            viewer_count = get_live_viewers(channel_id)
            update_viewer_count(name, str(viewer_count))


def create_stock_embed(stock_prices_list, from_date=None, to_date=None):

    embed=discord.Embed(title="Ticker mention frequency", color=0x00ff00)

    footer_str = ""
    if not from_date and not to_date:
        footer_str = "All time stats"
    if from_date and not to_date:
        footer_str = "Stats after " + from_date
    if not from_date and to_date:
        footer_str = "Stats before " + to_date
    if from_date and to_date:
        footer_str = "Stats after " + from_date + " and before " + to_date
    

    embed.set_footer(text=footer_str)

    for stock in stock_prices_list:
        ticker = stock[0]
        tweeeters = stock[1]
        tweeter_str = ', '.join(tweeeters)
        times_mentioned = stock[2]
        ticker_without_dollar = ticker[1:]
        ticker_info = yf.Ticker(ticker_without_dollar)

        todays_data = ticker_info.history(period='1d')

        if len(todays_data) > 0:
            todays_close = todays_data['Close'][0]
            todays_open = todays_data['Open'][0]
            percent_change = ((todays_close - todays_open)/todays_open)
            
            percent_change = "{:.2f}".format(percent_change * 100) + "%"

            embed.add_field(name=f'**{ticker.upper()}**', value=f'```> Tweeted by count: {times_mentioned}\n> Today\'s Change: {percent_change}   Open: {"{:.2f}".format(todays_open)}   Close: {"{:.2f}".format(todays_close)}\n> Tweeted by: {tweeter_str}```',inline=False)
        else:
            embed.add_field(name=f'**{ticker.upper()}**', value=f'```> Tweeted by count: {times_mentioned}```', inline=False)


    return embed


@bot.command()
async def zclean(client):
    print('entere dzClean')
    known_names = ["python_discord.py", "live_youtube_check.py", "get_twitch_live.py", "post_anime_episode_updates.py", "tweet_posts.py"]

    for python_script in known_names:
        #pkill -9 -f script.py
        output = subprocess.run(["sudo", "pkill", "-9", "-f", python_script], capture_output=True).stdout.decode('UTF-8')

    os.system('cd /home/kapp/KappaBot/KappaBot/ && python3 python_discord.py')
    await client.send("done")

@client.event
async def on_message(message):
    if message.content.startswith('!weeb'):
        load_all_embeds()
        channels = await message.channel.webhooks()
        send_the_message(username="anime updates", \
            webhook=create_webhook_url(channels[0].id, channels[0].token), \
            avatar_url="https://media.discordapp.net/attachments/306941063497777152/792210065523998740/image.png", \
            embeds=all_embeds)

        all_embeds.clear()

    if message.content.startswith('!league'):
        future_games, future_embeds = get_future_league_games()
        for x in range(0, len(future_games)):
            if x < 5:
                await message.channel.send(future_games[x])
                await message.channel.send(embed=future_embeds[x])

    if message.content.startswith('!live'):

        embed = discord.Embed(colour=discord.Colour(12320855))
        is_anyone_online = False

        update_youtube_view_count()

        for streamer in get_everyone_online():
            is_anyone_online = True
            name = streamer[0]
            viewer_count = streamer[4]
            embed.add_field(name=name, value="[" + viewer_count + " viewers](https://twitch.tv/" + name + ")")

        if not is_anyone_online:
            embed = discord.Embed(tite="no ones online...")

        await message.channel.send(embed=embed)

    if message.content.startswith("!stocks"):
        msg = message.content
        msg_array = msg.split(" ")
        from_date = None
        to_date = None
        if len(msg_array) == 2:
            from_date = msg_array[1]
        if len(msg_array) == 3:
            to_date = msg_array[2]

        # if no FROM DATE supplied, use 1 that is 2 days ago

        if not from_date:
            now = datetime.today() - timedelta(days=2)
            year =  now.year
            month = now.month
            day = now.day

            from_date = str(year) + "-" + str(month) + "-" + str(day)

        top_stocks = get_top_stocks(from_date, to_date)
        await message.channel.send(embed=create_stock_embed(top_stocks, from_date, to_date))
        # channels = await message.channel.webhooks()
        # send_the_message(username="pop tickers", \
        #     webhook=create_webhook_url(channels[0].id, channels[0].token), \
        #     avatar_url=None, \
        #     content=top_stocks)

        # await message.channel.send(top_stocks)

    if message.content.startswith('!test'):
        await message.channel.send("hello")

    if message.content.startswith('!logstocks'):
        for file_path in os.listdir("logs/"):
            file = discord.File("logs/" + file_path)
            await message.channel.send(file=file)

# youtube_checks = open("logs/live-youtube-checks-logs.txt", "a+")
# twitch_live = open("logs/get-twitch-live-logs.txt", "a+")
# anime_updates = open("logs/post-anime-episodes-updates.txt", "a+")
# yt_vod_check = open("logs/live-youtube-checks-logs.txt", "a+")
# tweets = open("logs/tweets-logs.txt", "a+")

# subprocess.Popen(["python3","python_app/live_youtube_check.py"], stdout=yt_vod_check)
# subprocess.Popen(["python3","python_app/get_twitch_live.py"], stdout=twitch_live)
# subprocess.Popen(["python3","python_app/post_anime_episode_updates.py"], stdout=anime_updates)

subprocess.Popen(["python3","python_app/reset_twitter_script.py"])

client.run(config.get("discordclientlogin"))
