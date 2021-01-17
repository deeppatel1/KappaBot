import requests
# from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter, Embed
import sched, time
from bs4 import BeautifulSoup, SoupStrainer
import re
import json


url = "https://www.youtube.com/channel/UCbLj9QP9FAaHs_647QckGtg"
url2 = "https://www.youtube.com/channel/UCv9Edl_WbtbPeURPtFDo-uA"



def check_youtube_live(channel_id):
    url = "https://www.youtube.com/channel/" + channel_id
    content = requests.get(url).text
    soup = BeautifulSoup(content)
    raw = soup.findAll('script')

    if len(raw) < 29:
        return False
    
    main_json_str = raw[27].text[20:-1]
    main_json = json.loads(main_json_str)

    if "channelFeaturedContentRenderer" not in main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]:
        # if it gets to here, user is live, need to get their URL
        return False
    
    live_url = main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0]["videoRenderer"]["videoId"]
        
    return True, live_url

def get_live_viewers(channel_id):
    url = "https://www.youtube.com/channel/" + channel_id
    content = requests.get(url).text
    soup = BeautifulSoup(content)
    raw = soup.findAll('script')

    if len(raw) < 29:
        return 0
    
    main_json_str = raw[27].text[20:-1]
    main_json = json.loads(main_json_str)

    if "channelFeaturedContentRenderer" not in main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]:
        # if it gets to here, user is live, need to get their URL
        return 0
    
    viewer_count = main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0]["videoRenderer"]["shortViewCountText"]["runs"][0]["text"]
        
    return viewer_count

print(check_youtube_live("UCbLj9QP9FAaHs_647QckGtg"))
print(get_live_viewers("UCbLj9QP9FAaHs_647QckGtg"))

# req = requests.get(url)
# content = req.text
# # print(content)
# soup = BeautifulSoup(content)
# raw = soup.findAll('script')
# main_json_str = raw[27].text[20:-1]
# main_json = json.loads(main_json_str)

# # For live people, this should say {"text": " watching"}
# print(main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0]["videoRenderer"]["shortViewCountText"]["runs"][1])





# req = requests.get(url2)
# content = req.text
# # print(content)
# soup = BeautifulSoup(content)
# raw = soup.findAll('script')
# main_json_str = raw[27].text[20:-1]
# main_json = json.loads(main_json_str)

# # For live people, this should say {"text": " watching"}
# print(main_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelFeaturedContentRenderer"]["items"][0]["videoRenderer"]["shortViewCountText"]["runs"][1])



