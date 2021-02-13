import json, datetime
with open('./configuration.json') as json_file :
    config = json.load(json_file)
import sys
import os
from discord import Webhook, RequestsWebhookAdapter, Embed
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
from streamers_tracker import add_to_tweeter_tickers
from logging.handlers import RotatingFileHandler
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Rotating Log")
handler = RotatingFileHandler('logs/tweet-logs.log', maxBytes=7000000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z"))

logger.addHandler(handler)


atoken = config.get("twitterAccessToken")
asecret = config.get("twitterTokenSecret")
ckey = config.get("twitterApiKey")
csecret = config.get("twitterApiKeySecret")

people_to_follow = {
    "736784706486734852": "realiceposeidon",
    "344538810": "doublelift1",
    "4833803780": "loltyler1",
    "17301744": "imls",
    "934165701220282368": "macawcaw123",
    "1648029396": "c9perkz",
    "3291691": "chamath",
    "44196397": "elon"
}

stocks_peeps = {
    "1348999248151519233": "tradesew",
    "1308886171309813761": "neeqlix",
    "1251671451612131328": "davistrades",
    "1157015667842920450": "greenarrowtrade",
    "1281015843044970496": "jmoneystonks",
    "1290852657033338886": "thomascwatts",
    "332358429": "traderstewe",
    "52166809": "traderstewie",
    "1260551652479647745": "stockdweebs",
    "914627036081041408": "rebecca_trades",
    "748611168168644612": "walrustrades",
    "1329870719732379654": "sweatystonks",
    "83478764": "mohankonuru",
    "1300807912835690497": "taytrades11",
    "1290864917835390976": "tomikazi1",
    "1320043277001908227": "darkpoolcharts",
    "1310326298527571971": "Albert_Trades",
    "767561346275799045": "StockGodd",
    "897328204091871233": "PatternPlays",
    "906328017986899968" : "the_chart_life",
    "1302069535147687936" : "chartingoptions",
    "1196947949013684224" : "trader182",
    "1054561163843751936" : "ripster47" ,
    "1034036822081499141" : "gvstrader",
    "930177090971877377" :"87alwaysred",
    "887754279125221378" : "trendspider_j",
    "441248955" : "moon_shine15",
    "3410575617" : "johnscharts" ,
    "16851206" : "patternprofits", 
    "3083109892" : "avataraidan",
    "443292881" : "1charts6",
    "44366481" : "hulkcapital", 
    "40942576" : "thrackx",
    "1615735502": "solonoid12",
    "985721299078070272" : "thetaWarrior"
}

all_tweeters_to_follow = list(people_to_follow.keys()) + list(stocks_peeps.keys())

TWEETS_CHANNEL_WEBHOOK = config.get("tweets")
STOCKS_STUFF_WEBHOOK = config.get("stock-stuff")

NORMAL_TWEETS_CHANNELS = [config.get("tweets")]

# WANTED_CHARS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "~", "!", "@", "#", "%", "^", "&", "*", "(", ")", "<",">", ":", ";", "'", "\'"]
WANTED_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
UPPER_WANTED_CHARS = [a.upper for a in WANTED_CHARS]

def sendWebhookMessage(user_name, body_to_post, photo_pic_url, webhook_url):
    webhook = Webhook.from_url(url = webhook_url, adapter = RequestsWebhookAdapter())
    webhook.send(body_to_post, username=user_name, avatar_url=photo_pic_url)


class listener(StreamListener):
    def on_data(self, data):
        json_data = json.loads(data)
        # logger.info("---> Got data from: " + json_data.get("user").get("screen_name") + " " + json_data.get("created_at"))
        # take out replies
        # if json_data.get("in_reply_to_status_id"):
        #     logger.info("Taken out because it was a reply to status_id:")
        #     return
        # only use if original tweeter is 1 of the people we want
        id_str = json_data.get("user").get("id_str")
        if id_str not in all_tweeters_to_follow:
            # logger.info("---X----Taken out due to to id_str not being 1 to follow: " + id_str)
            return
        # now if this is 1 of the people we want to post to discord, do this
        if id_str in list(people_to_follow.keys()):
            logger.info("!!!!!------ Main person, posting to discord")
            logger.info(json_data)
            user = json_data.get("user").get("screen_name")
            id = json_data.get("id_str")
            url = "https://twitter.com/" + user + "/status/" + id
            profile_pic = json_data.get("user").get("profile_image_url_https")
            sendWebhookMessage(user, url, profile_pic, TWEETS_CHANNEL_WEBHOOK)
        # if its 1 of the stock people
        else:
            logger.info('!!!------ Stock person, maybe posting to discord')
            should_send_to_discord = False
            if json_data.get("truncated"):
                full_text = json_data.get("extended_tweet").get("full_text")
            else:
                full_text = json_data.get("text")
            logger.info(json_data.get("user").get("name"))
            logger.info(full_text)
            full_text_list = []
            c = full_text.split(" ")
            for a in c:
                full_text_list = full_text_list + a.split(" ")
            
            now = datetime.datetime.now()

            current_date_str = now.strftime("%Y-%m-%d")
            user = json_data.get("user").get("name")

            sc = set(WANTED_CHARS)
            for each_element in full_text_list:
                if "$" in each_element:
                    each_element = each_element[each_element.find("$"):]
                    each_element = ''.join([c for c in each_element if (c in WANTED_CHARS) or (c in UPPER_WANTED_CHARS)])
                    each_element = "$" + each_element
                    # remove everything before the dollar sign
                    if len(each_element) > 1:
                        # filter out unwanted chars
                        add_to_tweeter_tickers(user, each_element, current_date_str)
                        should_send_to_discord = True
                        logger.info(each_element + " added to db!")
            
            if should_send_to_discord:
                sendWebhookMessage(user, full_text, None, STOCKS_STUFF_WEBHOOK)

    def on_error(self, status):
        logger.info("!!!!! something happend GASP")
        logger.info(status)
        
        sendWebhookMessage(None, "420 420 420 420!!!! error in starting the tweet bot", None, STOCKS_STUFF_WEBHOOK)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
logger.info('---starting twitter checks')
twitterStream = Stream(auth, listener())
twitterStream.filter(follow=all_tweeters_to_follow, is_async=True)
