from enum import Enum
import json

with open('./configuration.json') as json_file :
    config = json.load(json_file)

class webhooks(Enum):
    MAIN_SERVER = config.get("main-server-webhook")
    TWEETS = config.get("tweets")
    YOUTUBE_VIDS = config.get("youtube-videos")
    XQC_YOUTUBE_VIDS = config.get("xqc-youtube-channel")
    TWITCH = config.get("twitch-webhook")
    MULA_BABY = config.get("stock-calls")
    MAC_TWEETS = config.get("mac-tweets-channel")
    XQC_TWEETS = config.get("xqc-tweets-channel")
    ELON_TWEETS = config.get("elon-channel")
    M1_CHANNEL = config.get("m1-checker")
    M1_CONNECT = config.get("m1-connect")
    SPECIAL_MAK_SERVER = config.get("mak-private-server")
    MAK_SERVER_MAIN_BUYS_SELLS = config.get("mak-private-sever-main-buys-sells")
    CHAMPIONS_QUEUE = config.get("champions-queue")
    SIU = config.get("siu")
    CLIPS = config.get("clips")