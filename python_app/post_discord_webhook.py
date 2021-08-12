from discord import RequestsWebhookAdapter, Webhook
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


WEBHOOKS_TO_POST = [webhooks.MAIN_SERVER.value]

def sendWebhookMessage(username: str, avatar_url: str, content=None, wait=False):
    for webhook in WEBHOOKS_TO_POST:
        print("Sending to Webhook " +  str(webhook) + " content: " + str(content))
        send_the_message(username, avatar_url, webhook, content=content, wait=wait)


def sendWebhookListEmbeds(username: str, avatar_url: str, embeds, content=None, wait=False):
    for webhook in WEBHOOKS_TO_POST:
        print("Sending an embed to " + str(webhook))
        send_the_message(username, avatar_url, webhook, content=None, embeds=embeds, wait=wait)


def send_the_message(username, avatar_url, webhook, content=None, embeds=None, wait=False):
    
    try:
        if content and not embeds:
            print("sending to webhook " + webhook)
            webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())
            print("Sending to Webhook " +  str(webhook) + " content: " + str(content))
            
            if wait:
                return webhook.send(content, username=username, avatar_url=avatar_url, wait=wait)
            else:
                webhook.send(content, username=username, avatar_url=avatar_url)
        else:
            if not content:
                content = ""

            if not avatar_url:
                avatar_url = "https://media.discordapp.net/attachments/306941063497777152/792210065523998740/image.pn"

            print(webhook)
            webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())
            print("Sending to Webhook content: " + str(content))

            if wait:
               return webhook.send(content=content, embeds=embeds, username=username, avatar_url=avatar_url, wait=wait)
            else:
                webhook.send(content=content, embeds=embeds, username=username, avatar_url=avatar_url)

    except:
        pass



if __name__ == "__main__":
    a =  "https://discordapp.com/api/webhooks/795476109164412948/RnGxDxa7rIkMZJGQiUOxWS6JdjaWrMdDeqN937d1Vo-ISKpet4nY0lkhbnxv4mzQ3s4J"
    print(send_the_message("aa", "https://i.imgur.com/c7EbcqP.jpeg", webhook=a, content="test", wait=True))