import requests
# from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter, Embed
import sched, time
from bs4 import BeautifulSoup, SoupStrainer
import re

LIVE_STREAMS = [
    {
        "channelName": "ICE",
        "channelTrueName": "IcePoseidon",
        "channelId": "UCv9Edl_WbtbPeURPtFDo-uA"
    },
    {
        "channelName": "UC3Nlcpu-kbLmdhph_BN7OwQ",
        "channelTrueName": "UC3Nlcpu-kbLmdhph_BN7OwQ",
        "channelId": "UC3Nlcpu-kbLmdhph_BN7OwQ"
    }
]

WEBHOOKS_TO_POST = ["https://discordapp.com/api/webhooks/529864369824071691/7Wa0N516n6nMPdaJB78ex85PWi2loPq18IWij3LCUugVhOwMR8h8I_ROokrPIQShyxgs"]

CURRENTLY_LIVE = []

def youtube_live_and_post_check(scheduler):
    print("###")
    print("Currently Live " + str(CURRENTLY_LIVE))
    for stream in LIVE_STREAMS:
        channel_name = stream.get("channelName")
        channel_true_name = stream.get("channelTrueName")
        channel_id = stream.get("channelId")
        print("----Youtube Live Check: " + channel_true_name)
        resp = requests.get("https://www.youtube.com/c/" + channel_true_name + "/videos?view=2&live_view=501")
        if resp.status_code == 200:
            if "Live now" in resp.text:
                print(channel_true_name + " IS LIVE")
                # person is live, post now
                if channel_name not in CURRENTLY_LIVE:
                    link = get_youtube_stream_link(channel_id)
                    sendWebhookMessage("<@173610714433454084> <@173611085671170048> " + channel_name + " IS LIVE " + link)
                    CURRENTLY_LIVE.append(channel_name)
            else:
                print(channel_true_name + " IS NOT LIVE")
                try:
                    CURRENTLY_LIVE.remove(channel_name)
                except ValueError:
                    pass
    
    scheduler.enter(10, 1, youtube_live_and_post_check, (scheduler,))


def sendWebhookMessage(body_to_post):
    for webhook in WEBHOOKS_TO_POST:
        webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())

    webhook.send(body_to_post, avatar_url="https://upload.wikimedia.org/wikipedia/commons/9/99/Paul_denino_13-01-19.jpg")


def start_live_checks():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, youtube_live_and_post_check, (s,))
    s.run()


def get_youtube_stream_link(channel_id):
    r = requests.get("https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id).text
    soup = BeautifulSoup(r, "lxml")

    return soup.find_all("entry")[0].find_all("link")[0]["href"]


start_live_checks()


# resp = requests.get()
# text = resp.text

# soup = BeautifulSoup(text)

# print(soup.find('a', id="video-title"))


# print(resp.status_code)
# print("Live now" in resp.text)
# print("<meta itemprop=\"videoId\" content=" in resp.text)
