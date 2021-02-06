import json
with open('./configuration.json') as json_file :
    config = json.load(json_file)
import sys
from discord import Webhook, RequestsWebhookAdapter, Embed
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener

atoken = config.get("twitterAccessToken")
asecret = config.get("twitterTokenSecret")
ckey = config.get("twitterApiKey")
csecret = config.get("twitterApiKeySecret")

people_to_follow = {
    "1615735502": "solonoid12",
    "736784706486734852": "realiceposeidon",
    "344538810": "doublelift1",
    "4833803780": "loltyler1",
    "17301744": "imls",
    "934165701220282368": "macawcaw123",
    "1648029396": "c9perkz",
    "3291691": "chamath"
}


NORMAL_TWEETS_CHANNELS = [config.get("tweets")]


def sendWebhookMessage(user_name, body_to_post, photo_pic_url):
    for webhook in NORMAL_TWEETS_CHANNELS:
        webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())

    webhook.send(body_to_post, username=user_name, avatar_url=photo_pic_url)


class listener(StreamListener):
    def on_data(self, data):
        json_data = json.loads(data)
        id = json_data.get("user").get("id_str")
        if id in people_to_follow.keys() and not json_data.get("in_reply_to_user_id"):
            user = json_data.get("user").get("screen_name")
            id = json_data.get("id_str")
            url = "https://twitter.com/" + user + "/status/" + id
            profile_pic = json_data.get("user").get("profile_image_url_https")
            sendWebhookMessage(user, url, profile_pic)

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(follow=list(people_to_follow.keys()))
