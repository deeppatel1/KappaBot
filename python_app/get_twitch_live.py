import json
import requests
from discord import Webhook, RequestsWebhookAdapter, Embed
import sched, time

with open('../configuration.json') as json_file :
    config = json.load(json_file)

STREAMERS_TO_CHECK = {
    "loltyler1": "51496027"
}

STREAMERS_LIVE = []
WEBHOOKS_TO_POST = ["https://discordapp.com/api/webhooks/529864369824071691/7Wa0N516n6nMPdaJB78ex85PWi2loPq18IWij3LCUugVhOwMR8h8I_ROokrPIQShyxgs"]

def get_auth_token():
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.get("twitchClientId") + "&client_secret=" + config.get("twitchClientSecret") + "&grant_type=client_credentials"

    resp = requests.post(url)

    if resp.status_code != 200:
        print("Failed to get auth token...")
        print(url)
        return None
    
    resp_body = resp.json()

    return resp_body["access_token"]


def check_streamer_live(streamer_name, streamer_id):

    auth_token = get_auth_token()
    if not auth_token:  
        return

    headers = {
        "Client-ID": config.get("twitchClientId"),
        "Authorization": "Bearer " + str(auth_token)
    }
    
    streamer_resp = requests.get("https://api.twitch.tv/helix/streams?user_id=" + streamer_id, headers=headers)

    if streamer_resp.status_code != 200:
        print("Streamer check failed, got auth token but failed on getting data from the API")
        return

    resp = streamer_resp.json()

    if "data" in resp and len(resp.get("data")) > 0:
        print("streamer " + streamer_name + " is ONLINE")

        if streamer_name not in STREAMERS_LIVE:
            url = "https://twitch.tv/" + streamer_name
            sendWebhookMessage(url)
            STREAMERS_LIVE.append(streamer_name)

    else:
        print("streamer " + streamer_name + " is offline")
        if streamer_name in STREAMERS_LIVE:
            STREAMERS_LIVE.remove(streamer_name)


def check_all_streamers(scheduler):
    for streamer in STREAMERS_TO_CHECK:
        print("--- Twitch Live Check for " + streamer)
        check_streamer_live(streamer, STREAMERS_TO_CHECK.get(streamer))

    scheduler.enter(10, 1, check_all_streamers, (scheduler,))


def start_checks():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, check_all_streamers, (s,))
    s.run()


def sendWebhookMessage(body_to_post):
    for webhook in WEBHOOKS_TO_POST:
        webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())


    webhook.send(body_to_post, username="twitch live bot", avatar_url="https://media-exp1.licdn.com/dms/image/C560BAQHm82ECP8zsGw/company-logo_200_200/0/1593628073916?e=2159024400&v=beta&t=89u72cg5KzjSQ1qwB9xPZYhWvr7jFkD_9mUyFdNFnVw")



start_checks()