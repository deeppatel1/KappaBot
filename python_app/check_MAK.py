import requests
import pprint
import json
from discord import RequestsWebhookAdapter, Webhook
with open('./configuration.json') as json_file :
    config = json.load(json_file)
from dateutil import parser
from python_app.streamers_tracker import check_post_id_mak_usama, add_to_mak_usama
from python_app.WEBHOOKS import webhooks
from datetime import datetime, timezone
import pytz

# from streamers_tracker import check_post_id_mak_usama, add_to_mak_usama

relevant_channels_dict = {
    "934280148147142686": "swing_trading",
    "912756512429068329": "trading_floor",
}

relevant_people_dict = {
    "714337095552073760": "MAK_Usama",
    "751564764244869282": "MrMonroe",
    "173611085671170048": "Deep"
}


# relevant_channels_dict = {
#     "306941063497777152": "twitter",
# }

# relevant_people_dict = {
#     "173611085671170048": "deep",
#     "173610714433454084": "ragen"
# }

RELEVANT_CHANNELS = relevant_channels_dict.keys()
RELEVANT_PEOPLE = relevant_people_dict.keys()

HOW_MANY_POSTS_TO_GET_PER_10_SECONDS = 20

headers = {
  'authorization': config.get("discord_direct_auth_key"),
  'authority': 'discord.com',
  'accept': '*/*'
}

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def init_discord_checks():
    # every 10 seconds, get 20 messages
    for channel in RELEVANT_CHANNELS:
        url = f"https://discord.com/api/v9/channels/{channel}/messages?limit={HOW_MANY_POSTS_TO_GET_PER_10_SECONDS}"
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            for post in response.json():
                # check if post already exists in the checked db, if so, exit
                post_id = post.get("id")
                db_resp = check_post_id_mak_usama(post_id)

                print(db_resp)
                # exit since this id was already recorded
                if db_resp:
                    print("Post already exists in db")
                    break
                
                print("New Post")
                who_posted_id = post.get('author').get('id')
                who_posted_name = post.get('author').get('username')
                who_posted_pic_id = post.get('author').get('avatar')
                when_posted = post.get('timestamp')

                when_posted_datetime_string = utc_to_local(parser.parse(when_posted)).strftime("%m/%d, %H:%M:%S")

                who_posted_pic_link = f'https://cdn.discordapp.com/avatars/{who_posted_id}/{who_posted_pic_id}.webp'

                if who_posted_id in RELEVANT_PEOPLE:
                    # post to discord, important person!
                    add_to_mak_usama(post_id)
                    print("Posted to discord and saved to db")
                    sendWebhookMessage(who_posted_name, when_posted_datetime_string + "      " + post.get("content"), who_posted_pic_link, webhooks.MULA_BABY.value)
        else:
            print("API CALL FAILED")
            print(response.text)
            sendWebhookMessage("API CALL FAILED", response.text, "https://t4.ftcdn.net/jpg/00/60/88/79/360_F_60887942_CcOarL81d2GCQRKbxd4DAc3dIUrBr7fu.jpg", webhooks.MULA_BABY.value)

def sendWebhookMessage(user_name, body_to_post, photo_pic_url, webhook_url):
    webhook = Webhook.from_url(url = webhook_url, adapter = RequestsWebhookAdapter())
    webhook.send(body_to_post, username=user_name, avatar_url=photo_pic_url)


if __name__ == "__main__":
    init_discord_checks()