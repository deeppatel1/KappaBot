import datetime
import time
import discord
import requests
from bs4 import BeautifulSoup
import datetime
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Rotating Log")
handler = RotatingFileHandler('logs/get-league-matches.log', maxBytes=7000000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z"))
logger.addHandler(handler)

GAMEPEDIA_URL = "https://lol.fandom.com/wiki/Special:RunQuery/MatchCalendarExport?pfRunQueryFormName=MatchCalendarExport&MCE%5B1%5D=LCS%2F2022+Season%2FLock+In%2CLEC%2F2022+Season%2FSpring+Season%2CLCS%2F2022+Season%2FSpring+Season&wpRunQuery=Run+query&pf_free_text="


relevant_teams = [
    "TSM",
    "GGS",
    "C9",
    "CLG",
    "TL",
    "EG",
    "100",
    "IMT",

    "G2",
    "FNC",
    "RGE",
    "VIT",

    "DK",
    "T1",
    "HLE",

    # "RNG",
    # "PSG",
    # "UOL",
    # "INF",
    # "IW",
    # "PNG",
    # "DFM",
    # "PGG"
]

class game:
    def __init__(self, datetime, full_line):
        self.datetime = datetime
        self.full_line = full_line

emoji_id = {
    "lcs": 799520852990754818,
    "lck": 804921471335661588,
    "msi": 836447489749155860,
    "worlds": 896978680847409162,

    "vs": 729131117436731403,

    "c9": 728503911765246013,
    "tsm": 729060542693638276,
    "fly": 729060542861410459,
    "eg": 729060542404362322,
    "tl": 729060542995497076,
    "imt": 729060542765072436,
    "dig": 729060542819467284,
    "100t": 729060542873862155,
    "clg": 729060542848958595,
    "gg": 729060543113068554,

    "bro": 804915045045239839,
    "ns": 804915044591599636,
    "af": 729109817398001765,
    "dk": 804915043539484702,
    "lsb": 804915043048620092,


    "sp": 729109817016451113,
    "dyn": 729109817011994724,
    "kt": 729109816710267054,
    "dwg": 729109815460233246,
    "hle": 729109815451713636,
    "gen": 729109815409770496,
    "t1": 729109815543988224,
    "drx": 729109815384604753,

    "fnc": 799522187803361300,
    "g2": 799522170346668054,
    "mad": 804913457916411934,
    "msf": 804913457115037756,
    "vit": 804913456414588978,
    "rge": 804913455965405185,
    "sk": 804913215737036801,
    "xl": 804912661652832326,
    "s04": 804912620918407189,
    "ast": 804912367283994664,

    "rng": 836479419081555990,

    "lec": 802762920168521738
}


def generate_embeds(list_of_games, how_many_games_to_return):
    versus_strings = []
    all_embeds = []
    for game in list_of_games:
        
        game_data = game.full_line.split(",")
       
        tourney_and_competitors = game_data[0].split(" - ")
        date_time_str = game_data[1] + "-" + game_data[2] + "-" + game_data[3] + " " + game_data[4] + ":" + game_data[5]


        full_string = game.full_line
        game_info = full_string.split(',')
        league_and_versus = game_info[0]

        for team in relevant_teams:
            if team.lower() in full_string.lower() and len(all_embeds) < how_many_games_to_return:

                date = game_info[1]
                # time = game_info[2]

                league = ''

                if "lcs".lower() in league_and_versus.lower():
                    league = 'lcs'
                
                if "lec".lower() in league_and_versus.lower():
                    league = 'lec'
                
                if "lck".lower() in league_and_versus.lower():
                    league = 'lck'

                if "msi".lower() in league_and_versus.lower():
                    league = 'msi'

                league_emoji = "<:" + league + ":" + str(emoji_id.get(league)) + ">"

                left_team = league_and_versus.split(" ")[-3]
                right_team = league_and_versus.split(" ")[-1]

                left_team_og_string = left_team
                right_team_og_string = right_team

                if str(left_team) == "100":
                    left_team = "100t"

                if str(right_team) == "100":
                    right_team = "100t"

                left_team_emoji = left_team.lower()
                right_team_emoji = right_team.lower()

                if emoji_id.get(left_team_emoji):
                    left_team_emoji = "<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">"
                else:
                    left_team_emoji = left_team_emoji.upper()

                if emoji_id.get(right_team_emoji):
                    right_team_emoji = "<:" + right_team_emoji + ":" + str(emoji_id.get(right_team_emoji)) + ">"
                else:
                    right_team_emoji = right_team_emoji.upper()
                
                vs_emoji = "<:versus:" + str(emoji_id.get("vs")) + ">"

                versus_strig = league_emoji + "\t\t" + left_team_emoji + vs_emoji + right_team_emoji + " "

                game_date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                
                # convert to UTC time for the hover time !

                game_date_time = game_date_time - datetime.timedelta(hours=5)

                versus_strig = versus_strig + "  " + "<t:" + str(int(time.mktime(game_date_time.timetuple()))) + ":R>"


                # , title="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">", description="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + "> test"
                #embed = discord.Embed(timestamp=game_date_time, description=league_emoji + "     " + left_team_emoji + " vs " + right_team_emoji)
                # left_team_og_string.upper() + " vs " + right_team_og_string.upper()
                embed = discord.Embed(description=versus_strig)
                #embed.set_thumbnail(url="https://am-a.akamaihd.net/image/?resize=120:&f=http%3A%2F%2Fstatic.lolesports.com%2Fleagues%2F1592516205122_LCK-01-FullonDark.png")
                #embed.add_field(name="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">", value=".")
                #embed.add_field(name="<:" + right_team_emoji + ":" + str(emoji_id.get(right_team_emoji)) + ">", value=".")
                
                versus_strings.append(versus_strig)
                all_embeds.append(embed)
                break

    print(all_embeds)
    return versus_strings, all_embeds



def get_future_league_games(how_many_games_to_return, league=None):
    schedule = requests.get(GAMEPEDIA_URL).text
    soup = BeautifulSoup(schedule, 'html.parser')

    content = soup.find(id='mw-content-text').get_text()
    # logger.info(content)
    list_content = content.split("\n")
    all_matches_after_now = []

    games = []


    if league:
        if league.upper() == "LEC":
            league = "LEC 2022"
        elif league.upper() == "LCK":
            league = "LCK 2022"
        for k in list_content:
            if league.upper() in k.upper():
                games.append(k)

    else:

        for k in list_content:
            if "LCK 2022" in k:
                games.append(k)
            elif "LCS" in k:
                games.append(k)
            elif "LEC 2022" in k:
                games.append(k)
            elif "MSI" in k:
                games.append(k)

    now = datetime.datetime.now()
    for game_line in games:
        game_data = game_line.split(",")
        tourney_and_competitors = game_data[0].split(" - ")

        date_time_str = game_data[1] + "-" + game_data[2] + "-" + game_data[3] + " " + game_data[4] + ":" + game_data[5]
        date_time = datetime.datetime.strptime(date_time_str.strip('\n'),'%Y-%m-%d %H:%M')

        tourney = tourney_and_competitors[0]
        competitors =  tourney_and_competitors[1]    

        now = datetime.datetime.utcnow()
        list_counter = 0
        if date_time > now:
            game_obj = game(date_time + datetime.timedelta(hours=3), game_line.strip("\n"))
            all_matches_after_now.append(game_obj)    
            list_counter = list_counter + 1  

    all_matches_after_now.sort(key=lambda r: r.datetime)
    return generate_embeds(all_matches_after_now, how_many_games_to_return)



if __name__ == "__main__":
    [b, a] = get_future_league_games()
    for a in range(0,5):
        logger.info(b[a])