import requests
import discord
import MangaDexPy

from .streamers_tracker import get_all_mangas, update_manga_chapter, get_who_to_at
from .post_discord_webhook import sendWebhookListEmbeds, sendWebhookMessage


cli = MangaDexPy.MangaDex()

# 
# 
# Call https://www.reddit.com/r/manga/search.json?q=[disc]solo_leveling&limit=1&sort=new&restrict_sr=on
# 
# check if the URL is in the database, if it is, don't do anything
# if it isnt, add it to DB, along with chapter name, chapter link, and chapter number
# 


def all_fun_manga_check():

    all_mangas = get_all_mangas()
    
    for manga_info in all_mangas:
        manga_name = manga_info[0]
        fun_manga_url = manga_info[1]
        last_chapter = int(manga_info[2])
        who_to_at = manga_info[3]
        mangadex_id = manga_info[4]

        next_chapter_number = last_chapter + 1

        new_chapter_out_wow = check_if_chapter_exists(manga_name, fun_manga_url, next_chapter_number)

        if new_chapter_out_wow:
            
            title = get_official_manga_title(mangadex_id)
            cover_url = get_last_cover(mangadex_id)
            embed = create_embed(manga_name, mangadex_id, next_chapter_number, fun_manga_url, title, cover_url)
            
            who_to_at_str = get_who_to_at(who_to_at)

            sendWebhookMessage(manga_name, cover_url, content=who_to_at_str)
            sendWebhookListEmbeds(username=manga_name, avatar_url=cover_url, embeds=[embed], content=None)
            update_manga_chapter(manga_name, next_chapter_number)


def check_if_chapter_exists(manga_name, manga_url, chapter_number):

    url = "https://www.funmanga.com/" + manga_url + "/" + str(chapter_number)
    print("Checking URL " + url)
    resp = requests.get(url)

    if resp.status_code == 200 and not "is not available yet" in str(resp.content):
        print("Chapter is out")
        return True    

    else:
        print("chapter is not out")
        return False


def create_embed(manga_name, mangadex_id, chapter_number, fun_manga_url, title, cover_url):

    url_of_chapter = "https://www.funmanga.com/" + fun_manga_url + "/" + str(chapter_number)
    
    embed=discord.Embed(title="Chapter " + str(chapter_number) + " is out, click to read", url=url_of_chapter)
    embed.set_author(name=title)
    embed.set_thumbnail(url=cover_url)
    
    return embed


def get_last_cover(mangadex_id):
    
    manga = cli.get_manga(mangadex_id)
    covers = manga.get_covers()
    
    if covers:
        return covers[-1].url

    return None


def get_official_manga_title(mangadex_id):
    manga = cli.get_manga(mangadex_id)
    title = manga.title

    return title.get("en")


# all_fun_manga_check()