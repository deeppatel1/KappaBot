from tweety.bot import Twitter
from discord import RequestsWebhookAdapter, Webhook
from .WEBHOOKS import webhooks
from bs4 import BeautifulSoup
from .streamers_tracker import get_all_xqc_ow_updates_ids, add_to_xqc_ow_updates, get_who_to_at
import tweepy
import json
import logging
import requests
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Rotating Log")
handler = RotatingFileHandler('logs/xqc-live-check.log', maxBytes=7000000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z"))
logger.addHandler(handler)


with open('./configuration.json') as json_file :
    config = json.load(json_file)

WEBHOOK_URL = webhooks.XQC_TWEETS.value
TWITTER_NAME = "xQcUpdates"

consumer_key = 'tHmXWGs4qIxFxJyQ0un2IzehD'
consumer_secret = 'aCJ58c69LXZd9c34x7Ei5Gh1UOW2lXbcGtBygDEazkwZ9eE5gj'
access_token = '1615735502-edwxo7I3hHPVDcL8Sj9b50LsAzLkIKx8ZF8Gj19'
access_token_secret = 'X5lCv3peeS2mXx1Pe9JukirM1hfUQbXbKadMvRDJNUkQ4'


def post_alert_something_wrong(error_text):
    print(error_text)
    logger.info(error_text)

def sendWebhookMessage(body_to_post):
    webhook = Webhook.from_url(url = WEBHOOK_URL, adapter = RequestsWebhookAdapter())
    webhook.send(body_to_post, username="xQcUpdates",
                 avatar_url="https://upload.wikimedia.org/wikipedia/commons/9/99/Paul_denino_13-01-19.jpg")


def check_existing_twitter_ids(id):
    existing_ids = [id[0] for id in get_all_xqc_ow_updates_ids()]
    return id in existing_ids


def execute():
    app = Twitter(TWITTER_NAME)

    try:
        all_tweets = app.get_tweets()
    except:
        post_alert_something_wrong("Failed to get tweets!")
    if not all_tweets:
        post_alert_something_wrong("Failed to hit list, maybe not enough tweets!")

    first_tweet_id = all_tweets[0].id

    try:
        if not check_existing_twitter_ids(first_tweet_id):
            # confirm if id isn't already shared and post

            tweet_url = "http://twitter.com/xQcUpdates/status/" + first_tweet_id

            sendWebhookMessage(tweet_url)

            # add to db now
            add_to_xqc_ow_updates(first_tweet_id)


            h = {
                "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw"
            }

            with requests.post("https://api.twitter.com/1.1/guest/activate.json", headers=h) as r:
                guest_token = r.json()["guest_token"]
                h["x-guest-token"] = guest_token

                with requests.get(f"https://api.twitter.com/1.1/statuses/show/{first_tweet_id}.json", headers=h) as tr:
                    data = tr.json()
                    tweet_text = data.get('text')

                    if ("now live" in tweet_text.lower()) or ("is live" in tweet_text.lower()):
                        sendWebhookMessage(get_who_to_at("ragen"))

        else:
            post_alert_something_wrong("Tweet already exists in the DB")

    except Exception as e:
        post_alert_something_wrong(f"Woah!!!! HOLD ON failed to hit API {e}")
        sendWebhookMessage(e)


if __name__ == "__main__":
    execute()