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
    "EDISON": "08837"
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

                # before posting to discord, check existing status of inventory

                checking_avaliability = get_model_avaliability(max_model_number, area)
                older_avaliability = checking_avaliability[0][2]


                if older_avaliability != avaliability:
                    # status has changed, update and tell discord
                    print("status has changed!")
                    sendWebhookMessage(f'{macbook_max_color} {avaliability} -at- {store} @everyone')


                update_model_avaliablity(max_model_number, area, avaliability)

                print(macbook_max_color + " " + avaliability + " at " + store)

    # scheduler.enter(300, 1, check_all_models_avaliability, (scheduler,))

def sendWebhookMessage(body_to_post):
    webhook = Webhook.from_url(url = webhooks.M1_CHANNEL.value, adapter = RequestsWebhookAdapter())
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

    # is_anyone_online = False
    # update_youtube_view_count()
    # for streamer in get_everyone_online():
    #     is_anyone_online = True
    #     name = streamer[0]
    #     viewer_count = streamer[4]
    #     stream_start_time_string = streamer[9]
    #     stream_title = streamer[10]
    #     game = streamer[11]

    #     # slang_string = maya.parse(stream_start_time_string).slang_time()
    #     game_date_time = datetime.datetime.strptime(stream_start_time_string, "%Y-%m-%dT%H:%M:%S%z")

    #     game_date_time = game_date_time - datetime.timedelta(hours=4)

    #     since_string = "since " + "<t:" + str(int(time.mktime(game_date_time.timetuple()))) + ":R>"
        
    #     embed.add_field(name= name, value="> " + stream_title + "" + "\n" + " > [" + viewer_count + " watching](https://twitch.tv/" + name + ") " + since_string + " " + " on " + game)
    # if not is_anyone_online:
    #     embed = discord.Embed(tite="no ones online...")
    #     embed.add_field(name="no one online", value="...")
    # return embed

# def start_checks():
#     s = sched.scheduler(time.time, time.sleep)
#     s.enter(10, 1, check_all_models_avaliability, (s,))
#     s.run()


# start_checks()
