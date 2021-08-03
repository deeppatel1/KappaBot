import discord, json
import requests
import yfinance as yf
import datetime
# import maya
import time
from bs4 import BeautifulSoup
from python_app.streamers_tracker import (
    get_platform_streamers,
    get_everyone_online,
)


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
        # if name == "ice":
        #     viewer_count = get_live_viewers(channel_id)
        #     update_viewer_count(name, str(viewer_count))


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

        try:
            todays_data = ticker_info.history(period='1d')
            # print('todays data')
            # print(todays_data)


        except Exception as error:
            print("Error?")
            print(error)
            continue


        if ticker.upper() not in ["$SPY", "$QQQ"]:
            if len(todays_data) > 0:
                todays_close = todays_data['Close'][0]
                todays_open = todays_data['Open'][0]
                percent_change = ((todays_close - todays_open)/todays_open)
                
                percent_change = "{:.2f}".format(percent_change * 100) + "%"

                embed.add_field(name=f'**{ticker.upper()}**', value=f'```> Tweeted by count: {times_mentioned}\n> Today\'s Change: {percent_change}   Open: {"{:.2f}".format(todays_open)}   Close: {"{:.2f}".format(todays_close)}\n> Tweeted by: {tweeter_str}```',inline=False)
            else:

                embed.add_field(name=f'**{ticker.upper()}**', value=f'```> Tweeted by count: {times_mentioned}```', inline=False)

    
    return embed


def get_ticker_embed(ticker_resp):
    ticker = ticker_resp[0][1]
    embed=discord.Embed(title=ticker, color=0x00ff00)

    for tweet in ticker_resp:
        tweeter_name = tweet[0]
        date_time = tweet[2]
        text = tweet[3]
        link = tweet[4]

        if text:
            if link:
                field_value = '[' + text + '](' + link + ')'
            else:
                field_value = text
            
            embed.add_field(name="```" + str(date_time) + " " + tweeter_name + "```", value = field_value)

    return embed


def pumped_ticker_embed(ticker_resp, date):
    
    embed=discord.Embed(title='Most Pumped after ' + str(date), color=0x00ff00)

    for tweet in ticker_resp:
        if tweet[1].upper() not in ["$INTEREST", "$DAILY", "$SECTOR", "$BIDASK"]:
            tweeter_name = tweet[0]
            ticker = tweet[1]
            count = tweet[2]
            percent_change = 'test'
            data = yf.download(ticker[1:], start=date)
            if len(data) > 0:
                start_value = data['Open'][0]
                end_value = data['Close'][-1]
                        
                percent_change = ((end_value - start_value)/start_value)   
                percent_change = "{:.2f}".format(percent_change * 100) + "%"
                field_value = tweeter_name + "  --  " + str(count) + " times"    
            
            embed.add_field(name="```" + ticker.upper() +  "```", value=f'```> Tweeted by count: {count}\n> Overall Change: {percent_change}   Start: {"{:.2f}".format(start_value)}   End: {"{:.2f}".format(end_value)}\n> Tweeted by: {tweeter_name}```',inline=False)

            # embed.add_field(name="```" + ticker.upper() +  "```", value=f'```> Tweeted by count: {count}\n> Tweeted by: {tweeter_name}```',inline=False)

    embed.set_footer(text="Since " + date)
    return embed


def get_all_live_embed():
    embed = discord.Embed(colour=discord.Colour(12320855))
    is_anyone_online = False
    update_youtube_view_count()
    for streamer in get_everyone_online():
        is_anyone_online = True
        name = streamer[0]
        viewer_count = streamer[4]
        stream_start_time_string = streamer[9]
        stream_title = streamer[10]
        game = streamer[11]

        # slang_string = maya.parse(stream_start_time_string).slang_time()
        game_date_time = datetime.datetime.strptime(stream_start_time_string, "%Y-%m-%dT%H:%M:%S%z")

        game_date_time = game_date_time - datetime.timedelta(hours=4)

        since_string = "since " + "<t:" + str(int(time.mktime(game_date_time.timetuple()))) + ":R>"
        
        embed.add_field(name= "```> " + name + " <```", value="`" + stream_title + "`" + "\n" + "[" + viewer_count + " watching](https://twitch.tv/" + name + ") " + since_string + " " + " on " + game)
    if not is_anyone_online:
        embed = discord.Embed(tite="no ones online...")
        embed.add_field(name="no one online", value="...")
    return embed
