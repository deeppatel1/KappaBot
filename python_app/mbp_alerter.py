import requests
import discord, json
import json, sched, time, requests
from python_app.WEBHOOKS import webhooks
from python_app.streamers_tracker import get_model_avaliability, update_model_avaliablity, get_all_m1_status
from discord import RequestsWebhookAdapter, Webhook

URL = "https://www.apple.com/shop/retail/pickup-message"

MACBOOK_MODELS = {
    "White M1 Max": 'MK1H3LL/A',
    "Gray M1 Max": 'MK1A3LL/A'
}

MACBOOK_MODEL_TO_NAME = {v: k for k, v in MACBOOK_MODELS.items()}

LOCATIONS = {
    "BRIDGEWATER": "08844",
    "CHRISTIANA MALL": "19702",
    "QUAKER BRIDGE": "08648",
    "EDISON": "08837",
    "CHICAGO": "60611"
}

def check_all_models_avaliability():

    for macbook_max_color, max_model_number in MACBOOK_MODELS.items():
        for area, zip_code in LOCATIONS.items():
            params = {
                "location": zip_code,
                "parts.0": max_model_number
            }

            resp = requests.get(URL, params=params)

            if resp.status_code == 200:
                resp = resp.json()

                details = resp.get("body").get("stores")[0]

                store = details.get("storeName")
                avaliability = details.get("partsAvailability").get(max_model_number).get("pickupSearchQuote")
                state = details.get("state")

                # before posting to discord, check existing status of inventory

                checking_avaliability = get_model_avaliability(max_model_number, area)
                older_avaliability = checking_avaliability[0][2]


                if older_avaliability != avaliability:
                    # status has changed, update and tell discord
                    print("status has changed!")
                    if "NJ" not in state:
                        sendWebhookMessage(f'{macbook_max_color} {avaliability} -at- {store} @everyone', webhooks.M1_CONNECT.value)
                    else:
                        sendWebhookMessage(f'{macbook_max_color} {avaliability} -at- {store} @everyone', webhooks.M1_CHANNEL.value)


                update_model_avaliablity(max_model_number, area, avaliability)

                print(macbook_max_color + " " + avaliability + " at " + store)

    # scheduler.enter(300, 1, check_all_models_avaliability, (scheduler,))

def sendWebhookMessage(body_to_post, webhook_url):
    webhook = Webhook.from_url(url = webhook_url, adapter = RequestsWebhookAdapter())
    webhook.send(body_to_post, username="jobs disciple", avatar_url="https://images-na.ssl-images-amazon.com/images/I/41dKkez-1rL._SX326_BO1,204,203,200_.jpg")


def get_all_current_status_embed():
    
    all_status = get_all_m1_status()
    
    embed = discord.Embed(colour=discord.Colour(12320855))

    for status in all_status:
        model_number = status[0]
        location = status[1]
        avaliability = status[2]

        model_name = MACBOOK_MODEL_TO_NAME.get(model_number)

        embed.add_field(name=model_name, value=f'`{avaliability}` at {location}')

    return embed
