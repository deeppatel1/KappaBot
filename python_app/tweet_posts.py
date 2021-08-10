import json, datetime
with open('./configuration.json') as json_file :
    config = json.load(json_file)
from discord import RequestsWebhookAdapter, Webhook
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from streamers_tracker import add_to_tweeter_tickers
from logging.handlers import RotatingFileHandler
from WEBHOOKS import webhooks
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
    "44196397": "elon",
    "273519109": "ls",
    "1947617514": "grossie_gore",
    "2790180781": "Alphari",
    "1615735502": "solonoid12",
    "936128517460201473": "SpicaLoL",
    "785651770697523200": "xQc",
    "1282068738959749120": "xQCOWUpdates"
}

stocks_peeps = {
    "1308886171309813761": "neeqlix",
    "1251671451612131328": "davistrades",
    "1157015667842920450": "greenarrowtrade",
    "1281015843044970496": "jmoneystonks",
    "1290852657033338886": "thomascwatts",
    "52166809": "traderstewie",
    "1260551652479647745": "stockdweebs",
    "914627036081041408": "rebecca_trades",
    "748611168168644612": "walrustrades",
    "83478764": "mohankonuru",
    "1300807912835690497": "taytrades11",
    "1290864917835390976": "tomikazi1",
    "1310326298527571971": "Albert_Trades",
    "767561346275799045": "StockGodd",
    "897328204091871233": "PatternPlays",
    "3410575617" : "johnscharts" ,
    "16851206" : "patternprofits", 
    "3083109892" : "avataraidan",
    "1615735502": "solonoid12",
    "985721299078070272" : "thetaWarrior",
    "427693716": "PandaOptions",
    "728291846": "d_pavlos",
    "150094848": "sssvenky",
    "1014726871911714816": "dougie_dee",
    "1118235493030866944": "yatesinvesting",
    "1007420368288714754": "tradingthomas3",
    "373620043": "mrzackmorris",
    "888225282334871553": "pj_matlock",
    "946470689367842816" : "hugh_Henne",
    "89517375": "ultra_calls",
    "758386485846544384": "realwillmeade",
    "1054661392119283712": "thestockguytv",
    "1243273376023621639": "puppytrades",
    "1243680071304404993": "hawkstocks",
    "1208632009817354241": "the_trade_journey",
    "83150642": "thelioncom",
    "204531012": "data168",
    "1231876668865695744": "iTradeContracts",
    "1240151681851146247": "pKdayTrading1",
    "1285245919609462786": "TheATMTrades",
    "345525945": "TicTockTik",
    "1018324467758465024": "EliteOptions2"
}


calls_people = {
    "52166809": "traderstewie",
    "1615735502": "solonoid12",
    "748611168168644612": "walrustrades",
    "3083109892" : "avataraidan",
    "1231876668865695744": "iTradeContracts",
    "1240151681851146247": "pKdayTrading1",
    "1285245919609462786": "TheATMTrades",
    "345525945": "TicTockTik",
    "1007420368288714754": "tradingthomas3",
    "1310326298527571971": "Albert_Trades",
    "1300807912835690497": "taytrades11",
    "1018324467758465024": "EliteOptions2"
}


all_tweeters_to_follow = list(people_to_follow.keys()) + list(stocks_peeps.keys())


# WANTED_CHARS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "~", "!", "@", "#", "%", "^", "&", "*", "(", ")", "<",">", ":", ";", "'", "\'"]
WANTED_CHARS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
UPPER_WANTED_CHARS = [a.upper() for a in WANTED_CHARS]

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
            profile_pic = json_data.get("user").get("profile_image_url_https")

            is_reply = True if json_data.get("in_reply_to_status_id") else False


            if str(user) == "macaiyla":
                discord_channel_to_post = webhooks.MAC_TWEETS.value
            elif str(user) == "xQc" or str(user) == "xQCOWUpdates":
                discord_channel_to_post = webhooks.XQC_TWEETS.value
            else:
                discord_channel_to_post = webhooks.TWEETS.value

            print("Posting it at " + str(discord_channel_to_post))
            if is_reply:
                replied_to_user_name = json_data.get("in_reply_to_screen_name")
                replied_to_id = json_data.get("in_reply_to_status_id")
                url = "https://twitter.com/" + str(replied_to_user_name) + "/status/" + str(replied_to_id)
                sendWebhookMessage(user, url, profile_pic, discord_channel_to_post)

            id = json_data.get("id_str")
            url = "https://twitter.com/" + user + "/status/" + id

            if is_reply:
                url = "REPLY TO ABOVE " + url
            print("DISCORD CHANNEL TO POST")
            print(discord_channel_to_post)
            sendWebhookMessage(user, url, profile_pic, discord_channel_to_post)
        # if its 1 of the stock people
        else:
            logger.info('!!!------ Stock person, maybe posting to discord')
            should_send_to_discord = False
            screen_name = json_data.get('user').get('screen_name')
            id = json_data.get('id')
            url = 'https://twitter.com/' + screen_name + '/status/' + str(id)
            if json_data.get("truncated"):
                full_text = json_data.get("extended_tweet").get("full_text")
            else:
                full_text = json_data.get("text")
            # logger.info(json_data.get("user").get("name"))
            # logger.info(full_text)
            full_text_list = []
            c = full_text.split(" ")
            for a in c:
                full_text_list = full_text_list + a.split(" ")
            
            now = datetime.datetime.now()

            current_date_str = now.strftime("%Y-%m-%d")
            user = json_data.get("user").get("name")

            current_date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

            sc = set(WANTED_CHARS)
            for each_element in full_text_list:
                if "$" in each_element:
                    each_element = each_element[each_element.find("$"):]
                    each_element = ''.join([c for c in each_element if (c in WANTED_CHARS) or (c in UPPER_WANTED_CHARS)])
                    each_element = "$" + each_element
                    # remove everything before the dollar sign
                    if len(each_element) > 2 and len(each_element) < 6:
                        # filter out unwanted chars
                        add_to_tweeter_tickers(user, each_element, current_date_str, current_date_time_str, full_text, url)
                        should_send_to_discord = True
                        logger.info(each_element + " added to db!")

            if should_send_to_discord:
                # sendWebhookMessage(user, full_text, None, webhooks.MULA_BABY)          
                # If the tweeter poster is posting a option (right now, we've hardcoded 2 people who post options)
                if str(id_str) in calls_people.keys():
                    sendWebhookMessage(user, url, None, webhooks.MULA_BABY)

    def on_error(self, status):
        logger.info("!!!!! something happend GASP")
        logger.info(status)
        
        # sendWebhookMessage(None, "420 420 420 420!!!! error in starting the tweet bot", None, webhooks.MULA_BABY)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
logger.info('---starting twitter checks')
twitterStream = Stream(auth, listener())
twitterStream.filter(follow=all_tweeters_to_follow, is_async=True)
