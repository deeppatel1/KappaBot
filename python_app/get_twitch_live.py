import json, sched, time, requests
from discord import Webhook, RequestsWebhookAdapter, Embed
from streamers_tracker import get_platform_streamers, update_viewer_count, update_streamer_online_status, update_viewer_count, get_everyone_online
with open('./configuration.json') as json_file :
    config = json.load(json_file)

WEBHOOKS_TO_POST = [config.get("main-server-webhook")]


def get_auth_token():
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.get("twitchClientId") + "&client_secret=" + config.get("twitchClientSecret") + "&grant_type=client_credentials"

    resp = requests.post(url)

    if resp.status_code != 200:
        print("Failed to get auth token...")
        print(url)
        return None
    
    resp_body = resp.json()

    return resp_body["access_token"]


def check_streamer_live(streamer):

    streamer_name = streamer[0]
    streamer_id = streamer[1]
    online_status = streamer[3]

    auth_token = get_auth_token()

    if not auth_token:
        return

    API_CALL_HEADERS = {
        "Client-ID": config.get("twitchClientId"),
        "Authorization": "Bearer " + str(auth_token)
    }


    streamer_resp = requests.get("https://api.twitch.tv/helix/streams?user_id=" + streamer_id, headers=API_CALL_HEADERS)

    if streamer_resp.status_code != 200:
        print("Streamer check failed, got auth token but failed on getting data from the API")
        return

    resp = streamer_resp.json()
    if "data" in resp and len(resp.get("data")) > 0:
        print("streamer " + streamer_name + " is ONLINE")

        if not online_status:
            url = "https://twitch.tv/" + streamer_name
            discord_post = streamer_name + " IS LIVE <@173610714433454084> <@173611085671170048> " + url
            sendWebhookMessage(discord_post)

        # Update the db now
        update_streamer_online_status(streamer_name, "TRUE")
        update_viewer_count(streamer_name,  str(resp.get("data")[0]["viewer_count"]))

    else:
        print("streamer " + streamer_name + " is offline")
        # Update the db now
        update_streamer_online_status(streamer_name, "FALSE")
        update_viewer_count(streamer_name,  "0")


def check_all_streamers(scheduler):

    # First, get all twitch streamers saved in the db
    all_twitch_streamers = []
    streamer_infos = get_platform_streamers("twitch")
    for streamer in streamer_infos:
        print("--- Twitch Live Check for " + streamer[0])
        check_streamer_live(streamer)

    scheduler.enter(180, 1, check_all_streamers, (scheduler,))


def start_checks():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, check_all_streamers, (s,))
    s.run()


def sendWebhookMessage(body_to_post):
    for webhook in WEBHOOKS_TO_POST:
        webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())

    webhook.send(body_to_post, username="twitch live bot", avatar_url="https://media-exp1.licdn.com/dms/image/C560BAQHm82ECP8zsGw/company-logo_200_200/0/1593628073916?e=2159024400&v=beta&t=89u72cg5KzjSQ1qwB9xPZYhWvr7jFkD_9mUyFdNFnVw")


start_checks()
