import json
import asyncio
import discord
import subprocess
import pytz
from discord.ext import commands, tasks
from pandas.tseries.offsets import BDay
from datetime import date, datetime, timedelta
from python_app.get_animes_and_mangas import all_embeds, load_all_embeds
from python_app.get_league_matches import get_future_league_games
from python_app.streamers_tracker import (
    get_top_stocks,
    get_specific_tickers,
    get_most_pumped,
    get_last_twitch_id,
    delete_all_values_in_twitch_last_live,
    update_twitch_id_field,
    get_last_m1_check_message,
    update_m1_last_live_field,
    delete_all_values_in_m1_last_posted
)
from python_app.post_discord_webhook import send_the_message
from python_app.get_latest_mangas_notif import all_fun_manga_check
from python_helpers import (
    create_webhook_url,
    create_stock_embed,
    get_ticker_embed,
    pumped_ticker_embed,
    get_all_live_embed,
)
from python_app.mbp_alerter import check_all_models_avaliability, get_all_current_status_embed
from collections import OrderedDict
from operator import itemgetter

bot = commands.Bot(command_prefix="!")

with open("configuration.json") as json_file:
    config = json.load(json_file)


@bot.event
async def on_ready():

    TWITCH_CHANNEL_ID = 813935859002900500
    M1_CHANNEL_ID = 904122267049545749
    REFRESH_WHOS_LIVE_SECONDS = 300

    while True:
        embed = get_all_live_embed()
        channel = bot.get_channel(TWITCH_CHANNEL_ID)

        #
        # get previous twitch id
        #

        id = get_last_twitch_id()
        if id:
            msg = await channel.fetch_message(str(id))
            await msg.delete()
            delete_all_values_in_twitch_last_live()

        sent_message = await channel.send(embed=embed)
        print("--- id of message that will be deleted later")
        print(sent_message.id)
        update_twitch_id_field(str(sent_message.id))

        # 
        # the mbp alerter logic goes here, not being used no longer! disabling
        # 

        # check_all_models_avaliability()
        # channel = bot.get_channel(M1_CHANNEL_ID)
        
        # m1_check_embed = get_all_current_status_embed()
        # id = get_last_m1_check_message()
        # print('///')
        # print(id)
        # if id:
        #     msg = await channel.fetch_message(str(id))
        #     await msg.delete()
        #     delete_all_values_in_m1_last_posted()
        #     # delete
        
        # sent_message = await channel.send(embed=m1_check_embed)
        # print("---- id of the message to be deleted")
        # print(sent_message.id)
        # update_m1_last_live_field(str(sent_message.id))


        await asyncio.sleep(REFRESH_WHOS_LIVE_SECONDS)


@bot.command(name="weeb", brief="Prints episode info about latest stored animes")
async def weeb(ctx):
    print("started")
    dict_embeds = {}
    load_all_embeds()
    channels = await ctx.channel.webhooks()
    # print(all_embeds)
    # aa = sorted(all_embeds, key = lambda i: i['datetime'])
    for embed in all_embeds:
        embed_dict = embed.to_dict()
        dict_embeds[embed] = embed_dict.get("timestamp", "")
    dict_embeds = OrderedDict(
        sorted(dict_embeds.items(), key=itemgetter(1), reverse=True)
    )
    send_the_message(
        username="anime updates",
        webhook=create_webhook_url(channels[0].id, channels[0].token),
        avatar_url="https://media.discordapp.net/attachments/306941063497777152/792210065523998740/image.png",
        embeds=dict_embeds.keys(),
    )
    all_embeds.clear()


DEFAULT_NUMBER_OF_GAMES_TO_RETURN = 10
@bot.command(name="league", brief="Prints upcoming league schedule. Add name of league to only include that league. Ex: !league lcs")
async def league(ctx, arg=None, arg2=DEFAULT_NUMBER_OF_GAMES_TO_RETURN):
    future_games, future_embeds = get_future_league_games(arg2, league=arg)
    final_string_to_send = ""

    for game in future_games:
        final_string_to_send = final_string_to_send + "\n" + game
    
    await ctx.send(final_string_to_send)


    # for x in range(0, len(future_embeds)):
    #     if x < arg2:
    #         await ctx.send(future_games[x])
    #         # await ctx.send(embed=future_embeds[x])


@bot.command(name="live", brief="Prints live streamers")
async def live(ctx):
    embed = get_all_live_embed()
    await ctx.send(embed=embed)


@bot.command(name="stocks", brief="Lists top mentioned stocks by furus in the past 2 days")
async def stocks(ctx, arg1=None, arg2=None):
    from_date = None
    to_date = None
    source_time_zone = pytz.timezone('US/Eastern')
    if arg1:
        from_date = arg1
    if arg2:
        to_date = arg2

    # if no FROM DATE supplied, use 1 that is 2 days ago
    if not from_date:
        # BDay is business date
        right_now_datetime = datetime.now(source_time_zone)
        now = right_now_datetime.now(source_time_zone)
        
        now = datetime(now.year, now.month, now.day, 22)
        only_todays_date = datetime(now.year, now.month, now.day)

        if right_now_datetime.weekday() < 5 and right_now_datetime.hour > 16:
            now = only_todays_date + timedelta(hours=16)
        elif right_now_datetime.weekday() < 5 and right_now_datetime.hour > 9:
            now = only_todays_date + timedelta(hours=9)
        else:
            now = only_todays_date - BDay(1) + timedelta(hours=16)

        print("Getting stocks after ")
        print(now)

        year = now.year
        month = now.month
        day = now.day
 
        hours = now.hour
        minutes = now.minute


        from_date = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hours) + ":" + str(minutes) + ":00"

    top_stocks = get_top_stocks(from_date, to_date)
    await ctx.send(embed=create_stock_embed(top_stocks, from_date, to_date))
    # channels = await ctx.webhooks()
    # send_the_message(username="pop tickers", \
    #     webhook=create_webhook_url(channels[0].id, channels[0].token), \
    #     avatar_url=None, \
    #     content=top_stocks)
    # await ctx.send(top_stocks)


@bot.command(name="ticker", brief="Prints latest tweets from furus")
async def ticker(ctx, arg=None):
    if not arg:
        await ctx.send("enter a ticker")
    ticker = arg
    print("!!! input ticker " + ticker)
    ticker_info = get_specific_tickers(ticker)
    if not ticker_info:
        await ctx.send("no tweets for this ticker found")
    ticker_embed = get_ticker_embed(ticker_info)
    if not ticker_embed:
        await ctx.send("no tweets for this ticker")
    await ctx.send(embed=ticker_embed)


@bot.command(name="pumped", brief="Check which stocks are pumped")
async def pumped(ctx):
    # msg = message.content
    # msg_array = msg.split(" ")
    from_date = None
    to_date = None

    # if len(msg_array) == 2:
    #     from_date = msg_array[1]
    #     ticker = msg_array[0]

    # else:
    #     from_date = None
    #     ticker = message.content

    if not from_date:
        now = datetime.today() - timedelta(days=3)
        year = now.year
        month = now.month
        day = now.day
        from_date = str(year) + "-" + str(month) + "-" + str(day)

    resp = get_most_pumped(from_date)
    embed = pumped_ticker_embed(resp, from_date)
    await ctx.send(embed=embed)


@tasks.loop(hours = 1)
async def check_fun_manga():
    all_fun_manga_check()
    # work

check_fun_manga.start()



subprocess.Popen(["python3", "python_app/reset_twitter_script.py"])
bot.run(config.get("discordclientlogin"))



# @client.event
# async def on_message(message):
#     if message.content.startswith('!logstocks'):
#         for file_path in os.listdir("logs/"):
#             file = discord.File("logs/" + file_path)
#             await ctx.send(file=file)
