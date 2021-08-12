import json, sched, time, requests
from discord import RequestsWebhookAdapter, Webhook
from streamers_tracker import get_platform_streamers, update_stream_start_time, update_streamer_online_status, update_viewer_count, update_viewer_count, get_who_to_at, update_stream_title, update_game_played
with open('./configuration.json') as json_file :
    config = json.load(json_file)
import logging
from logging.handlers import RotatingFileHandler
from WEBHOOKS import webhooks

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Rotating Log")
handler = RotatingFileHandler('logs/get-twitch-live.log', maxBytes=7000000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z"))
logger.addHandler(handler)

WEBHOOKS_TO_POST = [webhooks.TWITCH.value]


def get_auth_token():
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.get("twitchClientId") + "&client_secret=" + config.get("twitchClientSecret") + "&grant_type=client_credentials"

    resp = requests.post(url)

    if resp.status_code != 200:
        logger.info("Failed to get auth token...")
        logger.info(url)
        return None
    
    resp_body = resp.json()

    return resp_body["access_token"]


def check_streamer_live(streamer):

    streamer_name = streamer[0]
    streamer_id = streamer[1]
    online_status = streamer[3]
    filters = streamer[6]
    who_to_at = streamer[7]
    should_it_post_to_twitch_channel = streamer[8]

    auth_token = get_auth_token()

    if not auth_token:
        return

    API_CALL_HEADERS = {
        "Client-ID": config.get("twitchClientId"),
        "Authorization": "Bearer " + str(auth_token)
    }


    streamer_resp = requests.get("https://api.twitch.tv/helix/streams?user_id=" + streamer_id, headers=API_CALL_HEADERS)

    print(streamer_resp.content)

    if streamer_resp.status_code != 200:
        logger.info("Streamer check failed, got auth token but failed on getting data from the API")
        return

    resp = streamer_resp.json()
    should_post_to_discord = False
    if "data" in resp and len(resp.get("data")) > 0:
        logger.info("streamer " + streamer_name + " is ONLINE current status " + str(online_status))

        if not online_status:
            # check if filters exist, than if filter exists, that filter must exist in the title.
            title = resp.get("data")[0].get("title")
            title = "#lcsCoStream"
            if filters:
                logger.info(filters)
                filters_list = filters.split(",")
                for filter in filters_list:
                    logger.info(filter)
                    logger.info("checking for filter " + filter)
                    if filter.lower() in title.lower():
                        logger.info("filter found, posting to discord")
                        should_post_to_discord = True
                        break
                    else:
                        logger.info("filter not found, moving on")

            else:
                logger.info("no filters found, posting to discord anyway")
                should_post_to_discord = True

            if should_post_to_discord and should_it_post_to_twitch_channel:
                url = "https://twitch.tv/" + streamer_name
                who_to_at = get_who_to_at(who_to_at)
                discord_post = streamer_name + " IS LIVE " + who_to_at + " " + url
                if filters:
                    discord_post = discord_post + " " + str(filters)
                sendWebhookMessage(discord_post)

        # Update the db now
        print("Updating streamer " + streamer_name)
        update_streamer_online_status(streamer_name, "TRUE")
        update_viewer_count(streamer_name,  str(resp.get("data")[0]["viewer_count"]))
        update_stream_start_time(streamer_name, str(resp.get("data")[0]["started_at"]))
        update_stream_title(streamer_name, str(resp.get("data")[0]["title"]))
        update_game_played(streamer_name, str(resp.get("data")[0]["game_name"]))

    else:
        logger.info("streamer " + streamer_name + " is offline")
        # Update the db now
        update_streamer_online_status(streamer_name, "FALSE")
        update_viewer_count(streamer_name,  "0")
        update_stream_start_time(streamer_name, "never")
        update_stream_title(streamer_name, "nothing")
        update_game_played(streamer_name, "nothing")

def check_all_streamers(scheduler):
    # First, get all twitch streamers saved in the db
    all_twitch_streamers = []
    streamer_infos = get_platform_streamers("twitch")
    for streamer in streamer_infos:
        logger.info("--- Twitch Live Check for " + streamer[0])
        check_streamer_live(streamer)

    scheduler.enter(600, 1, check_all_streamers, (scheduler,))


def start_checks():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, check_all_streamers, (s,))
    s.run()


def sendWebhookMessage(body_to_post):
    webhook = Webhook.from_url(url = webhooks.TWITCH.value, adapter = RequestsWebhookAdapter())
    webhook.send(body_to_post, username="twitch live bot", avatar_url="https://media-exp1.licdn.com/dms/image/C560BAQHm82ECP8zsGw/company-logo_200_200/0/1593628073916?e=2159024400&v=beta&t=89u72cg5KzjSQ1qwB9xPZYhWvr7jFkD_9mUyFdNFnVw")


start_checks()
