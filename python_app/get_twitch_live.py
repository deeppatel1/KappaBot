import json
import requests
from live_youtube_check import sendWebhookMessage
import sched, time

with open('../configuration.json') as json_file :
    config = json.load(json_file)

STREAMERS_TO_CHECK = {
    "loltyler1": "51496027"
}

STREAMERS_LIVE = []

def get_auth_token():
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.get("twitchClientId") + "&client_secret=" + config.get("twitchClientSecret") + "&grant_type=client_credentials"

    resp = requests.get(url)

    if resp != 200:
        return None
    
    resp_body = resp.json

    return resp_body["access_token"]


def check_streamer_live(streamer_name, streamer_id):

    auth_token = get_auth_token()
    if not auth_token:  
        return

    headers = {
        "Client-ID": config.get("twitchClientId"),
        "Authorization": "Bearer " + auth_token
    }
    
    streamer_resp = requests.get("https://api.twitch.tv/helix/streams?user_id=" + streamer_id, headers=headers)

    if streamer_resp.status_code != 200:
        return

    resp = streamer_resp.json

    if "data" in resp and len(resp.get("data") != 0):
       # is online

        if streamer_name not in STREAMERS_LIVE:
            url = "https://twitch.tv/" + streamer_name
            sendWebhookMessage(url)
            STREAMERS_LIVE.append(streamer_name)

    else:
        STREAMERS_LIVE.remove(streamer_name)


def check_all_streamers(scheduler):
    for streamer in STREAMERS_TO_CHECK:
        check_streamer_live(streamer, STREAMERS_TO_CHECK.get(streamer))

    scheduler.enter(10, 1, check_all_streamers, (scheduler,))


def start_checks():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, check_all_streamers, (s,))
    s.run()


start_checks()