from typing import List
import requests
from discord import Embed
import string
import datetime

from python_app.post_discord_webhook import sendWebhookListEmbeds, sendWebhookMessage
from python_app.streamers_tracker import check_reddit_manga_link_exists, add_chapter, get_all_mangas, get_who_to_at

# specific filters
FILTER_OUT = ["vigilantes", "comikey.com"]

class ChapterInfo:
    def __init__(self, manga_chapter, manga_chapter_thumbnail, manga_chapter_hyperlink, manga_chapter_reddit_link):  
        self.manga_chapter = manga_chapter
        self.manga_chapter_thumbnail = manga_chapter_thumbnail
        self.manga_chapter_hyperlink = manga_chapter_hyperlink
        self.manga_chapter_reddit_link = manga_chapter_reddit_link

def similar(a, b):
    # a is a string; title name with characters seperated with _
    # b is a string from reddit.

    # all words in "a" must be part of "b" in some capacity.
    # "a" from the database should be kept simple like "god_highschool"

    a_list = a.lower().split("_")
    b_list = b.lower().split(" ")

    how_many_similar = 0
    how_many_not_similar = 0

    for a_word in a_list:
        if a_word in b_list:
            how_many_similar = how_many_similar + 1
            b_list.remove(a_word)
        else:
            how_many_not_similar = how_many_not_similar + 1


    if len(b_list) > 7:
        how_many_not_similar = how_many_not_similar + 8

    return float(how_many_similar/(how_many_similar + how_many_not_similar))

    # custom similarity mechanism.

def make_api_call(manga_name):
    
    def is_too_old(epoch_datetime):
        now = datetime.datetime.now()
        when_was_post_created = datetime.datetime.fromtimestamp(epoch_datetime)
        if (now - datetime.timedelta(days=14) < when_was_post_created):
            return True
        return False
    
    query_url = f'https://www.reddit.com/r/manga/search.json?q=%5Bdisc%5D{manga_name}&limit=1&sort=new&restrict_sr=on&t=week'

    print(f'[->] Querying {manga_name}: {query_url}')

    resp = requests.get(query_url, headers = {'User-agent': 'kappabot'})

    if not resp.status_code == 200:
        print(f'[x] Failed to query reddit with status code {resp.status_code} at url: {query_url}')
        return None

    if resp.json().get("data").get("dist") == 0:
        print('[x] No results found in past week, returning Nothing!')
        return None

    data = resp.json().get("data").get("children")[0].get("data")

    manga_chapter = data.get("title")
    manga_created_datetime = is_too_old(data.get('created'))

    if manga_created_datetime and is_too_old(manga_created_datetime):
        print(f'[X] Manga {manga_name} is too old, created at epoch {manga_created_datetime}')
        return None

    if "weekly manga live" in manga_chapter.lower() or "guide" in manga_chapter:
        print(f'[X] Invalid title: {data.get("title")}')
        return None

    manga_chapter = manga_chapter.replace("[DISC] ", "")
    manga_chapter = manga_chapter.replace("[DISC]", "")

    # remove punctuation
    manga_chapter = manga_chapter.translate(str.maketrans('', '', string.punctuation))

    # guestimate how close the title of the retrieved result from reddit is similar to the wanted manga
    similarity = similar(manga_name.lower(), manga_chapter.lower())
    if similarity < 0.70:
        print(f"[X] Similarity between {manga_chapter} and {manga_name} is too low at: {similarity}")
        return None

    manga_chapter_thumbnail = data.get("thumbnail", "")
    manga_chapter_hyperlink = data.get("url")
    manga_chapter_reddit_link = data.get("permalink")

    # remove unwanted mangas, based on bad websites or the wrong chapter title
    for filter_key in FILTER_OUT:
        if filter_key in manga_chapter.lower() or filter_key in manga_chapter_hyperlink.lower():
            print(f"[X] hit filter {filter_key} in {manga_chapter} or {manga_chapter_hyperlink}")
            return None

    return ChapterInfo(manga_chapter, manga_chapter_thumbnail, manga_chapter_hyperlink, manga_chapter_reddit_link)


def is_old_chapter(manga_chapter : ChapterInfo):
    # return true if it is an old url so we dont neeed to do anything
    # return false if new url. processing needs to be done
    resp = check_reddit_manga_link_exists(manga_chapter.manga_chapter_hyperlink)
    print(f'[..] Checking if manga exists in db: {resp}')
    return bool(resp)


def add_chapter_logic(manga_chapter : ChapterInfo):
    add_chapter(manga_chapter.manga_chapter_hyperlink, manga_chapter.manga_chapter, manga_chapter.manga_chapter_thumbnail, manga_chapter.manga_chapter_reddit_link)


def send_discord_embed(manga_object, who_to_at):
    embed = Embed(title=manga_object.manga_chapter , description="New Chapter is out!", url=manga_object.manga_chapter_hyperlink)

    print("---- thumbnail")
    print(manga_object.manga_chapter_thumbnail)

    if "http" in manga_object.manga_chapter_thumbnail:
        embed.set_thumbnail(url=manga_object.manga_chapter_thumbnail)

    sendWebhookMessage(username="uwu", avatar_url="https://c.tenor.com/AR8p1LHTOFEAAAAC/discord-uwu-sweat.jpeg", content=get_who_to_at(who_to_at))
    sendWebhookListEmbeds(username="uwu", avatar_url="https://c.tenor.com/AR8p1LHTOFEAAAAC/discord-uwu-sweat.jpeg", embeds=[embed])


def init_manga_notifications():
    all_mangas = get_all_mangas()
    for manga in all_mangas:
        name = manga[0]
        who_to_at = manga[3]

        # call reddit, get latest chapter info
        manga_chapter_obj = make_api_call(name)

        # if cant for some reason, quit
        if not manga_chapter_obj:
            continue
    
        # if its an old chapter, quit
        if is_old_chapter(manga_chapter_obj):
            continue

        # add new chapter to db
        add_chapter_logic(manga_chapter_obj)
        
        # send to discord
        send_discord_embed(manga_chapter_obj, 'who_to_at_str')


init_manga_notifications()
