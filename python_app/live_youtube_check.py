import requests, sched, time, re, json
# from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter, Embed
from bs4 import BeautifulSoup, SoupStrainer
from streamers_tracker import get_platform_streamers, update_streamer_online_status, update_viewer_count, update_video_id
with open('./configuration.json') as json_file :
    config = json.load(json_file)


WEBHOOKS_TO_POST = [config.get("main-server-webhook")]


def check_youtube_live(channel_id):
    url = "https://www.youtube.com/channel/" + channel_id
    content = requests.get(url).text
    soup = BeautifulSoup(content)
    raw = soup.findAll('script')

    if len(raw) < 29:
        return False
    main_json_str = str(raw[27])[59:-10]
    main_json = json.loads(main_json_str)

    if "channelFeaturedContentRenderer" not in main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]:
        # if it gets to here, user is live, need to get their URL
        return False
    
    live_url = main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0]["videoRenderer"]["videoId"]
        
    return live_url


def start_youtube_checks(scheduler):

    for streamer in get_platform_streamers("youtube"):
        print("  Streamer info loaded: " + str(streamer))
        name = streamer[0]
        channel_id = streamer[1]
        is_online = streamer[3]
        viewer_count = streamer[4]

        if channel_id:
            live_url = check_youtube_live(channel_id)
            
            if live_url:
                update_video_id(name, live_url)
                if not is_online:
                    sendWebhookMessage("<@173610714433454084> <@173611085671170048> " + name + " IS LIVE " + "https://www.youtube.com/watch?v=" + live_url)
                update_streamer_online_status(name, "TRUE")
            if not live_url:
                update_streamer_online_status(name, "FALSE")
                update_video_id(name, "NULL")

    scheduler.enter(45, 1, start_youtube_checks, (scheduler,))


def sendWebhookMessage(body_to_post):
    for webhook in WEBHOOKS_TO_POST:
        webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())

    webhook.send(body_to_post, avatar_url="https://upload.wikimedia.org/wikipedia/commons/9/99/Paul_denino_13-01-19.jpg")


def start_live_checks():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(4, 1, start_youtube_checks, (s,))
    s.run()


start_live_checks()


def update_youtube_view_count():
    for streamer in get_platform_streamers("youtube"):
        print(stream)
        name = streamer[0]
        channel_id = streamer[1]

        viewer_count = get_live_viewers(channel_id)
        update_viewer_counts(name, viewer_count)        
        # stream["viewer_count"] = viewer_count



# old code

# resp = requests.get()
# text = resp.text

# soup = BeautifulSoup(text)

# print(soup.find('a', id="video-title"))



# def get_youtube_stream_link(channel_id):
#     r = requests.get("https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id).text
#     soup = BeautifulSoup(r, "lxml")

#     return soup.find_all("entry")[0].find_all("link")[0]["href"]

# print(resp.status_code)
# print("Live now" in resp.text)
# print("<meta itemprop=\"videoId\" content=" in resp.text)


# start_youtube_checks()

# def youtube_live_and_post_check(scheduler):
#     print("###")
#     print("Currently Live " + str(CURRENTLY_LIVE))
#     for stream in LIVE_STREAMS:
#         channel_name = stream.get("channelName")
#         channel_true_name = stream.get("channelTrueName")
#         channel_id = stream.get("channelId")
#         print("----Youtube Live Check: " + channel_true_name)
#         resp = requests.get("https://www.youtube.com/c/" + channel_true_name + "/videos?view=2&live_view=501")
#         if resp.status_code == 200:
#             if "Live now" in resp.text:
#                 print(channel_true_name + " IS LIVE")
#                 # person is live, post now
#                 if channel_name not in CURRENTLY_LIVE:
#                     link = get_youtube_stream_link(channel_id)
#                     sendWebhookMessage("<@173610714433454084> <@173611085671170048> " + channel_name + " IS LIVE " + link)
#                     CURRENTLY_LIVE.append(channel_name)
#             else:
#                 print(channel_true_name + " IS NOT LIVE")
#                 try:
#                     CURRENTLY_LIVE.remove(channel_name)
#                 except ValueError:
#                     pass
    
#     scheduler.enter(10, 1, youtube_live_and_post_check, (scheduler,))

