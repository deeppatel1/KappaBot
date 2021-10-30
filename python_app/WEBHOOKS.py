from enum import Enum
import json

with open('./configuration.json') as json_file :
    config = json.load(json_file)

class webhooks(Enum):
    MAIN_SERVER = config.get("main-server-webhook")
    TWEETS = config.get("tweets")
    YOUTUBE_VIDS = config.get("youtube-videos")
    TWITCH = config.get("twitch-webhook")
    MULA_BABY = config.get("stock-calls")
    MAC_TWEETS = config.get("mac-tweets-channel")
    XQC_TWEETS = config.get("xqc-tweets-channel")
    ELON_TWEETS = config.get("elon-channel")
    M1_CHANNEL = config.get("m1-checker")