import json, datetime
from re import L
with open('./configuration.json') as json_file :
    config = json.load(json_file)
from discord import RequestsWebhookAdapter, Webhook
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from streamers_tracker import add_to_tweeter_tickers, get_who_to_at
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
    "1282068738959749120": "xQCOWUpdates",
    "234644705": "TLCoreJJ",
    "1063379936856002560": "C9Summit",
    "1462144869233614854": "C9Berserker",
    "932465106709082114": "blaber",
    "741755662384910336": "vulcan",
    "3092505395": "bwipo",
    "2460445795": "hanssama",
    "18208354": "joerogan",
    "1029142980": "bjergsen",
    "2431173637": "jensen",
    "61868550": "closerlol",
    "1105221963075805184": "jojopyunlol",


    "1338693158536945665": "ChampionsQueue",
    "1505406256151883779": "ChampQueueBot"
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
    "1300807912835690497": "taytrades11",
    "1290864917835390976": "tomikazi1",
    "1310326298527571971": "Albert_Trades",
    "767561346275799045": "StockGodd",
    "897328204091871233": "PatternPlays",
    "3410575617" : "johnscharts" ,
    "16851206" : "patternprofits", 
    "3083109892" : "avataraidan",
    "1615735502": "solonoid12",
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
    "1018324467758465024": "EliteOptions2",
    "964529942": "JohnsCharts",
    "1072667998966743041": "optionsprochick",
    "985721299078070272": "ThetaWarrior",
    "1345256608901828612": "prophitcy",
    "1293683312960188416": "PBInvesting",
    "1075907037438115842": "RealJuicyTradez",
    "1428534232108961794": "TSDR_trading",
    "1250830691824283648": "STOCKMKTNewz",
    "1320043277001908227": "darkpoolcharts",
    "1140440713185787904": "nicabanding",
    "1461904538793873414": "huncheauxtrades",
    "4706746513": "spartantrading",
    "1448129133142290438": "SnB_Trading",
    "3690023483": "ryan11d",
    "1418644403334357004": "the10_percent",
    "1054561163843751936": "ripster47",
    "2248020090": "spyhatesme",
    "1358630527495000065": "xentreT",
    "706723368939065344": "korinek_trades",
    "1176866458933981184": "froggytrade",
    "1263277845549367296": "justDapper",
    "1226895349039714307": "itzSqueazy",
    "1095443643358339073": "kliphten",
    "887754279125221378": "Jake__Wujastyk",

    # people from https://twitter.com/chikatrades/status/1474821633130909698

    "1546222940": "dampedspring",
    "199170156" : "jam_croissant",
    "102869127" : "mayhem4markets",
    "4858859837" : "squeezemetrics",
    "1243218465982480386" : "annaoftheorder",
    "1156656695038357504" : "spotgamma",
    "14740370" : "kerberos007",
    "129960718" : "sanu_kiii",
    "1187026065660792832" : "strizzij",
    "1256262531569651712" : "sanntrades",
    "1279813859348566016" : "nlckstocks",
    "729435789411618817" : "adammancini4",
    "1271899909675859968" : "mrfourtoeight",
    "1161703589942878208" : "garyblack00",
    "1095931832" : "tricky_ow",
    "1056178693385711617" : "smashelito",
    "1437743290489585673" : "aevitas_momo",
    "1061650783333040129" : "superluckeee",
    "940789829243195393" : "gr8fuldaytrader",
    "1240400274977460224" : "zhangstatrades",
    "2192456106" : "jtraderco",
    "1599911502" : "_ms_izzy",
    "992461210556579840" : "redbentrader",
    "718182886" : "ksidiii",
    "1022137281719746560" : "vwaptrader1",
    "17094120" : "xtrends",
    "31468297" : "yodaflo"
}


calls_people = {
    "52166809": "traderstewie",
    "1615735502": "solonoid12",
    "1231876668865695744": "iTradeContracts",
    "1240151681851146247": "pKdayTrading1",
    "1007420368288714754": "tradingthomas3",
    "1310326298527571971": "Albert_Trades",
    "1300807912835690497": "taytrades11",
    "1018324467758465024": "EliteOptions2",
    "1072667998966743041": "optionsprochick",
    "985721299078070272": "ThetaWarrior",
    "1140440713185787904": "nicabanding",
    "1461904538793873414": "huncheauxtrades"
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
        if "delete" in json_data:
            return
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


            if str(user).lower() == "macaiyla":
                discord_channel_to_post = webhooks.MAC_TWEETS.value
            elif str(user).lower() == "xqc" or str(user).lower() == "xqcowupdates":
                discord_channel_to_post = webhooks.XQC_TWEETS.value
            elif str(user).lower() == "elonmusk":
                discord_channel_to_post = webhooks.ELON_TWEETS.value
            elif str(user).lower() == "championsqueue":
                discord_channel_to_post = webhooks.CHAMPIONS_QUEUE.value
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


            if json_data.get("truncated"):
                full_text = json_data.get("extended_tweet").get("full_text")
            else:
                full_text = json_data.get("text")

            # special case, if "now live" exists in an xqc updates tweet, ragen is @ ed
            if str(user).lower() == "xqcowupdates":
                if ("now live" in full_text) or ("is live" in full_text):
                    sendWebhookMessage("xQc is LIVE", get_who_to_at("ragen"), profile_pic, discord_channel_to_post)




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

            # if should_send_to_discord:
            #     if str(id_str) in calls_people.keys():
            #         sendWebhookMessage(user, url, None, webhooks.MULA_BABY.value)

    def on_error(self, status):
        logger.info("!!!!! something happend GASP")
        logger.info(status)
        if status != 200:
            discord_to_message = "TWITTER STUFF STOPPED WORKING FIX ASAP AHHHHHHH ERROR CODE !: " + str(status) + " Check for details https://developer.twitter.com/en/docs/twitter-ads-api/response-codes"
            sendWebhookMessage("error", discord_to_message, "https://exploringtm1.com/wp-content/uploads/2021/07/TM1-TI-Error-Codes.jpg", webhooks.TWEETS.value)
            return False

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
logger.info('---starting twitter checks')
twitterStream = Stream(auth, listener())
twitterStream.filter(follow=all_tweeters_to_follow, is_async=True)
