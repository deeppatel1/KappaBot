import sched, time, schedule, discord
from datetime import datetime, timedelta
from get_animes_and_mangas import call_anilist_api
from post_discord_webhook import sendWebhookListEmbeds, sendWebhookMessage

import logging
from logging.handlers import RotatingFileHandler
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Rotating Log")
handler = RotatingFileHandler('logs/post-anime-episodes-updates.log', maxBytes=7000000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z"))
logger.addHandler(handler)

class AnimeObject:
    def __init__(self, title, status, image, thumbnail, total_episodes, next_airing_episode, next_airing_date, four_anime_url):
        self.title = title
        self.status = status
        self.image = image
        self.thumbnail = thumbnail
        self.total_episodes = total_episodes
        self.next_airing_episode = next_airing_episode
        self.next_airing_date = next_airing_date
        self.four_anime_url = four_anime_url


def post_anime_episodes():

    with open("animeList.txt") as fp:
        line = fp.readline()
        cnt = 1
        while line:
            line_info = line.split(',')
            anilist_id = line_info[1].strip('\n')
            anime_name = line_info[0]

            anilist_resp = call_anilist_api(anilist_id)
            anime_object = get_next_airing_date(anilist_resp, anime_name)
            
            if anime_object:
                do_reminders(anime_object)


            line = fp.readline()
            cnt += 1


def do_reminders(anime_object):
    airing_date = anime_object.next_airing_date
    airing_datetime = datetime.fromtimestamp(airing_date)

    anime_title = anime_object.title
    episode = anime_object.next_airing_episode
    total_episodes = anime_object.total_episodes
    four_anime_url = anime_object.four_anime_url
    thumbnail_url = anime_object.thumbnail
    image = anime_object.image

    if (airing_datetime - datetime.now()).days == 0:
        airing_datetime = airing_datetime + timedelta(minutes=30)
        hours = airing_datetime.hour
        minutes = airing_datetime.minute

        if hours < 10:
            hours = "0" + str(hours)
        if minutes < 10:
            minutes = "0" + str(minutes)

        hour_minutes_str = str(hours) + ":" + str(minutes)

        logger.info("!!! TODAYS THE BIG DAY Scheduling anime " + anime_title + " for time " + str(airing_datetime))
        # schedule.every(2).seconds.do(set_reminder, airing_datetime, anime_title, episode, total_episodes,  four_anime_url, thumbnail_url, image)
        schedule.every().day.at(hour_minutes_str).do(set_reminder, airing_datetime, anime_title, episode, total_episodes,  four_anime_url, thumbnail_url, image)


def set_reminder(airing_datetime, anime_title, episode, total_episodes, four_anime_url_name, thumbnail, image):

    message = "Episode " + str(episode) + "/" + str(total_episodes) + " has aired! CLICK TO WATCH"

    if episode < 10:
        episode_str = "0" + str(episode)
    else:
        episode_str = str(episode)

    url = "https://4anime.to/" + four_anime_url_name + "-episode-" + episode_str

    embed = discord.Embed(title=message, url=url, timestamp=airing_datetime)
    embed.set_image(url=image)
    embed.set_footer(text="Aired")

    sendWebhookMessage(username=anime_title, avatar_url=avatar_url, content="@everyone")
    sendWebhookListEmbeds(username=anime_title, avatar_url=thumbnail, embeds=[embed])
    
    return


def get_next_airing_date(anilist_resp, four_anime_url):
    response = anilist_resp
    if response.status_code == 200:
        response = response.json()
        if response.get("data") and response.get("data").get("Media"):
            type = response.get("data").get("Media").get("type")
            if type == "ANIME":
                next_airing_date = None
                logger.info(response.get('data').get('Media').get('title').get('romaji') + " WILL AIR AT " + str(response.get('data').get('Media').get('nextAiringEpisode')))
                
                next_episode_dict = response.get('data').get('Media').get('nextAiringEpisode')
                if next_episode_dict and isinstance(next_episode_dict, dict):
                    title = response.get('data').get('Media').get('title').get('romaji')
                    status = response.get('data').get('Media').get('status')
                    image = response.get('data').get('Media').get('bannerImage')
                    thumbnail = response.get('data').get('Media').get('coverImage').get('medium')
                    total_episodes = response.get('data').get('Media').get('episodes')

                    next_episode_dict = response.get('data').get('Media').get('nextAiringEpisode')

                    if next_episode_dict and isinstance(next_episode_dict, dict):
                        episode = next_episode_dict.get("episode")
                        next_airing_date = next_episode_dict.get("airingAt")

                        anime_obj = AnimeObject(title = title, status = status, image = image, thumbnail = thumbnail, total_episodes = total_episodes, next_airing_episode = episode, next_airing_date= next_airing_date, four_anime_url = four_anime_url)
                        return anime_obj

    return None


def set_manual_manga_reminder(anime_name, day_of_month, manga_url):
    # manually puts up manga reminders... for now, naruto and super on the 20th at 12 pm

    text_to_show = anime_name + " new manga chapter should be released... click :point_right: " + manga_url
    time_to_post = "12:00"
    todays_date = datetime.now()
    todays_day_of_month = todays_date.day

    if todays_day_of_month == day_of_month:
        logger.info("scheduling for " + text_to_show + " at time " + time_to_post)
        schedule.every().day.at(time_to_post).do(post_manual_discord_reminder, text_to_show)


def post_manual_discord_reminder(text):
    text = "@everyone " + text
    sendWebhookMessage("manga updater", "https://i.ytimg.com/vi/e_bhsQyU3V4/maxresdefault.jpg", text)


# At startup, run these once:
post_anime_episodes()
set_manual_manga_reminder("naruto", 20, "https://www.viz.com/shonenjump/chapters/boruto")
set_manual_manga_reminder("dragon ball super", 20, "https://www.viz.com/shonenjump/chapters/dragon-ball-super")

while 1:
    schedule.run_pending()
    time.sleep(900)
