import json, requests, sched, time, logging
# from bs4 import BeautifulSoup
from discord import RequestsWebhookAdapter, Webhook
from bs4 import BeautifulSoup
from .WEBHOOKS import webhooks
from .streamers_tracker import add_utube_link, does_utube_link_exist, get_platform_streamers, get_video_id, update_video_id, get_who_to_at, update_streamer_online_status, update_viewer_count, update_streamer_is_annouced
from logging.handlers import RotatingFileHandler
import googleapiclient.discovery
import tweepy
import moment
from datetime import datetime, timedelta
import pprint

with open('./configuration.json') as json_file :
    config = json.load(json_file)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

    
logger = logging.getLogger("Rotating Log")
handler = RotatingFileHandler('logs/live-youtube-check.log', maxBytes=7000000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z"))
logger.addHandler(handler)

# -------------
# -------------
# -------------
AWAKE_VIDEO_CUTOFF = 1300
# -------------
# -------------
# -------------
ANNOUCED_VIDEO_CUTOFF = 2800
# -------------
# -------------
# -------------


CLIPS_CHANNELS = ["tyler1clips", "xqcclips", "scuffedcentral", "icepissshorts", "xyzah"]

DEVELOPER_KEY = config.get("gKey")
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

API_KEY = config.get("twitterApiKey")
API_KEY_SECRET = config.get("twitterApiKeySecret")

ACCESS_TOKEN = config.get("twitterAccessToken")
ACCESS_TOKEN_SECRET = config.get("twitterTokenSecret")


auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def get_latest_video_in_channel(channel_id):
    api_key = config.get("gKey")

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet&order=date&maxResults=1'

    logger.info(first_url)

    video_links = []
    url = first_url

    try:

        resp = requests.get(url)

        if resp.status_code == 200:
            
            resp = json.dumps(resp.json())
            resp = json.loads(resp)
            pprint.pprint(resp)

            first_item = resp["items"][0]

            title = first_item.get("snippet", {}).get("title", None)
            first_url = first_item.get("id", {}).get("videoId", None)

            return (title, first_url)
    except Exception as e:
        print(f'Exception encountered {e}') 
        pass

    return None, None


def get_filtered_video(channel_name, channel_id, filter_str):
    
    [name, url] = get_latest_video_in_channel(channel_id)
    
    print(f'Filtering video name: {name} and url {url}')

    if not name or not url:
        return None

    if filter_str:
        filters = filter_str.split(",")
    else:
        filters = None

    if not filters:
        url = "https://www.youtube.com/watch?v=" + url
        return url

    
    if name[0] == "E":
        url = "https://www.youtube.com/watch?v=" + url
        return url

    for filter in filters:
        if filter.lower() in name.lower():
            url = "https://www.youtube.com/watch?v=" + url
            return url

    return None


def check_if_url_in_db(channel_name, last_video_id):
    saved_video_id = get_video_id(channel_name)

    if saved_video_id != last_video_id:
        return False

    return True


def get_live_viewcount(video_id):
  youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  request = youtube.videos().list(
    part='liveStreamingDetails',
    id=video_id
  )
  response = request.execute()

  # Check if the video is a live stream
  if 'liveStreamingDetails' in response['items'][0]:
    # Get the concurrent viewers of the live stream
    return int(response['items'][0]['liveStreamingDetails']['concurrentViewers'])
  else:
    # The video is not a live stream
    return 0


def get_live_video_id_and_concurrent_viewers(channel_id):
    # Make a GET request to the YouTube Data API
    url = f'https://www.googleapis.com/youtube/v3/search?key={DEVELOPER_KEY}&channelId={channel_id}&part=snippet,id&eventType=live&type=video'
    print(url)
    response = requests.get(url)
    # Parse the response as JSON
    data = json.loads(response.text)
    # Get the most recent live stream video ID
    if not 'items' in data or len(data['items']) == 0:
        return None, 0, None

    video_id = data['items'][0]['id']['videoId']
    # Get the number of concurrent viewers
    url = f'https://www.googleapis.com/youtube/v3/videos?key={DEVELOPER_KEY}&id={video_id}&part=liveStreamingDetails'
    response = requests.get(url)
    data = json.loads(response.text)
    concurrent_viewers = data['items'][0]['liveStreamingDetails']['concurrentViewers']
    # Print the video ID and number of concurrent viewers
    print(f'Video ID: {video_id}')
    print(f'Concurrent Viewers: {concurrent_viewers}')
    start_time_obj = datetime.strptime(data['items'][0]['liveStreamingDetails']['actualStartTime'], '%Y-%m-%dT%H:%M:%SZ')

    return video_id, concurrent_viewers, start_time_obj


def check_youtube_live(channel_id):
    api_key = config.get("gKey")

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=1&type=video&eventType=live'.format(api_key, channel_id)

    logger.info(first_url)

    video_links = []
    url = first_url

    resp = requests.get(url)

    if resp.status_code == 200:
        
        resp = json.dumps(resp.json())
        resp = json.loads(resp)

        first_url = resp["items"][0]["id"]["videoId"]
        title = resp["items"][0]["snippet"]["title"]

    else:

        logger.info('!!!!')
        logger.info(resp.status_code)
        logger.info(resp.text)
        return None, None

    logger.info('got title, first_url' )
    logger.info(title)
    logger.info(first_url)
    return (title, first_url)


def start_youtube_checks():

    print('start youtube checks start_youtube_checks')

    youtubers = get_platform_streamers("youtube")

    print(youtubers)

    for streamer in youtubers:
        time.sleep(.5)
        logger.info("  Streamer info loaded: " + str(streamer))
        name = streamer[0]
        channel_id = streamer[1]
        last_video_id = streamer[2]
        is_online = streamer[3]
        viewer_count = streamer[4]
        filter_str = streamer[6]
        who_to_at_str = streamer[7]

        is_annouced = streamer[12]

        if channel_id:
            # IF ITS ICE, we take BETTER PRECAUTIONS!!!!!!!!!!!!!!! or dip
            if channel_id == "UCv9Edl_WbtbPeURPtFDo-uA" or channel_id == "UCakgsb0w7QB0VHdnCc-OVEA":
            #  or channel_id == "UC3Nlcpu-kbLmdhph_BN7OwQ":
                logger.info("BEGINNING ICE CHECKS")
                logger.info("BEGINNING ICE CHECKS")
                logger.info("BEGINNING ICE CHECKS")

                new_vid_id, live_viewers, start_time_obj = get_live_video_id_and_concurrent_viewers(channel_id)

                print(f'new vid info:::: {new_vid_id} {live_viewers} {start_time_obj}')


                update_viewer_count(name, str(live_viewers))


                if start_time_obj:

                    # we only care if the stream has been live for atleast 7 mins, to remove all cases where the stream needed to restart!
                    now = datetime.now()
                    time_diff = now - start_time_obj
                    minutes_diff = int(time_diff.total_seconds() / 60)

                    if minutes_diff > 7:
                        if new_vid_id:
                            update_video_id(name, new_vid_id)
                            # update_streamer_online_status(name, "TRUE")
                        else:
                            update_video_id(name, "NULL")
                            # update_streamer_online_status(name, "FALSE")

                        if new_vid_id:
                            logger.info("ICE is online! with URL : " + new_vid_id)

                            # 
                            # logic to message on twitter and discord that hes awake with > AWAKE_VIDEO_CUTOFF viewers
                            # 
                            if ((int(live_viewers)) > AWAKE_VIDEO_CUTOFF) & (not is_online):
                                post_discord_message(webhooks.SIU.value, new_vid_id, live_viewers)
                            if ((int(live_viewers)) <= AWAKE_VIDEO_CUTOFF) & (is_online):
                                post_discord_message(webhooks.SIU.value, new_vid_id, live_viewers, is_awake=False)


                            if ((int(live_viewers) > AWAKE_VIDEO_CUTOFF)):
                                update_streamer_online_status(name, "TRUE")
                            else:
                                update_streamer_online_status(name, "FALSE")


                            #
                            # logic to message on tiwtter and discord that THERES CONTENT with > annouced_video_cutoff viewers
                            # 


                            if ((int(live_viewers)) > ANNOUCED_VIDEO_CUTOFF) & (not is_annouced):
                                post_discord_message_that_theres_content(webhooks.SIU.value, new_vid_id, live_viewers)
                            if ((int(live_viewers)) <= ANNOUCED_VIDEO_CUTOFF) & (is_annouced):
                                post_discord_message_that_theres_content(webhooks.SIU.value, new_vid_id, live_viewers, is_content=False)


                            if ((int(live_viewers) > ANNOUCED_VIDEO_CUTOFF)):
                                update_streamer_is_annouced(name, "TRUE")
                            else:
                                update_streamer_is_annouced(name, "FALSE")

            else:
                last_youtube_video = get_filtered_video(name, channel_id, filter_str)
                if last_youtube_video and last_youtube_video != last_video_id and not does_utube_link_exist(last_youtube_video):
                    if name == "xqc":
                        sendWebhookMessage(webhooks.XQC_YOUTUBE_VIDS.value , name, last_youtube_video)
                    elif name in CLIPS_CHANNELS:
                        sendWebhookMessage(webhooks.CLIPS.value , name, last_youtube_video)
                    else:
                        who_to_at_discord_ats = get_who_to_at(who_to_at_str)
                        sendWebhookMessage(webhooks.YOUTUBE_VIDS.value, name, last_youtube_video + " " + who_to_at_discord_ats)

                    # print("output")
                    # print(does_utube_link_exist(last_youtube_video))
                    # if not does_utube_link_exist(last_youtube_video):
                    add_utube_link(last_youtube_video)
                    update_video_id(name, last_youtube_video)


def sendWebhookMessage(webhook, name, body_to_post):
    print(f'Posting body:{body_to_post} to webhook URL:{webhook}')
    webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())
    webhook.send(body_to_post, username=name, avatar_url="https://upload.wikimedia.org/wikipedia/commons/9/99/Paul_denino_13-01-19.jpg")


def post_discord_message(url, video_id, viewcount, is_awake=True):
    print(f'Attempting to post to url: {url}')
    if is_awake:
        content = f'https://youtube.com/watch?v={video_id} @REALIcePoseidon is AWAKE! at {moment.utcnow().timezone("Asia/Tokyo").format("h:mm:ss A")} with {viewcount} viewers.'
    else:
        content = f'Ice is probably sleeping now at {moment.utcnow().timezone("Asia/Tokyo").format("h:mm:ss A")} with {viewcount} viewers'

    payload = {
        'username': "crack head",
        'avatar_url': "https://upload.wikimedia.org/wikipedia/commons/9/99/Paul_denino_13-01-19.jpg",
        'content': (content + ' @everyone') if is_awake else (content)
    }

    api.update_status(content)
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(response)
    print(response.text)
    if response.status_code != 204:
        print(f'Error posting message to Discord: {response.content}')

    

def post_discord_message_that_theres_content(url, video_id, viewcount, is_content=True):
    print(f'Attempting to post to url: {url}')
    if is_content:
        content = f'https://youtube.com/watch?v={video_id} @REALIcePoseidon is PROBABLY DOING CONTENT! at {moment.utcnow().timezone("Asia/Tokyo").format("h:mm:ss A")} with {viewcount} viewers.'
    else:
        content = f'No content on ice stream @ {moment.utcnow().timezone("Asia/Tokyo").format("h:mm:ss A")} with {viewcount} viewers'

    payload = {
        'username': "crack head",
        'avatar_url': "https://upload.wikimedia.org/wikipedia/commons/9/99/Paul_denino_13-01-19.jpg",
        'content': (content + ' @everyone') if is_content else (content)
    }

    api.update_status(content)
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(response)
    print(response.text)
    if response.status_code != 204:
        print(f'Error posting message to Discord: {response.content}')


if __name__ == "__main__":
    # api.update_status("lll")
    start_youtube_checks()
    # logger.info(check_youtube_live("UCv9Edl_WbtbPeURPtFDo-uA"))

