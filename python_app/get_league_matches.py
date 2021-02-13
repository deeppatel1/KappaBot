import glob
import datetime
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

relevant_teams = [
    "TSM",
    "FLY",
    "C9",
    "CLG",
    "TL",
    "EG",
    "100",
    "G2",
    "FNC",
    "DK",
    "T1",
    "HLE"
]

class game:
    def __init__(self, datetime, full_line):
        self.datetime = datetime
        self.full_line = full_line

emoji_id = {
    "lcs": 799520852990754818,
    "lck": 804921471335661588,

    "vs": 729131117436731403,

    "c9": 728503911765246013,
    "tsm": 729060542693638276,
    "fly": 729060542861410459,
    "eg": 729060542404362322,
    "tl": 729060542995497076,
    "imt": 729060542765072436,
    "dig": 729060542819467284,
    "100~1:": 729060542873862155,
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


    "100": "test",
    "lec": 802762920168521738
}


def generate_embeds(list_of_games):
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
            if team.lower() in full_string.lower():

                date = game_info[1]
                time = game_info[2]

                league = ''

                if "lcs".lower() in league_and_versus.lower():
                    league = 'lcs'
                
                if "lec".lower() in league_and_versus.lower():
                    league = 'lec'
                
                if "lck".lower() in league_and_versus.lower():
                    league = 'lck'
                
                league_emoji = "<:" + league + ":" + str(emoji_id.get(league)) + ">" 

                left_team = league_and_versus.split(" ")[-3]
                right_team = league_and_versus.split(" ")[-1]

                if left_team != "100":
                    left_team_emoji = left_team.lower()
                else:
                    left_team_emoji = "100~1"
                
                if right_team != "100":
                    right_team_emoji = right_team.lower()
                else:
                    right_team_emoji = "100~1"

                left_team_emoji = "<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">"
                right_team_emoji = "<:" + right_team_emoji + ":" + str(emoji_id.get(right_team_emoji)) + ">"
                vs_emoji = "<:versus:" + str(emoji_id.get("vs")) + ">"
                
                if left_team_emoji == "<:100~1:None>":
                    left_team_emoji = ":100:"
                if right_team_emoji == "<:100~1:None>":
                    right_team_emoji = ":100:"

                versus_strig = league_emoji + "       " + left_team_emoji + vs_emoji + right_team_emoji

                game_date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                # , title="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">", description="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + "> test"
                #embed = discord.Embed(timestamp=game_date_time, description=league_emoji + "     " + left_team_emoji + " vs " + right_team_emoji)
                embed = discord.Embed(timestamp=game_date_time)
                #embed.set_thumbnail(url="https://am-a.akamaihd.net/image/?resize=120:&f=http%3A%2F%2Fstatic.lolesports.com%2Fleagues%2F1592516205122_LCK-01-FullonDark.png")
                #embed.add_field(name="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">", value=".")
                #embed.add_field(name="<:" + right_team_emoji + ":" + str(emoji_id.get(right_team_emoji)) + ">", value=".")
                versus_strings.append(versus_strig)
                all_embeds.append(embed)
                break

    return versus_strings, all_embeds



def get_future_league_games():
    schedule = requests.get("https://lol.gamepedia.com/Special:RunQuery/MatchCalendarExport?pfRunQueryFormName=MatchCalendarExport&MCE%5B1%5D=LCK%2F2021+Season%2FSpring+Season%2CLCS%2F2021+Season%2FLock+In%2CLEC%2F2021+Season%2FSpring+Season%2CLCS%2F2021+Season%2FSpring+Season&wpRunQuery=Run+query&pf_free_text=").text
    soup = BeautifulSoup(schedule, 'html.parser')

    content = soup.find(id='mw-content-text').get_text()
    # logger.info(content)
    list_content = content.split("\n")
    all_matches_after_now = []

    games = []

    for k in list_content:
        if "LCK 2021" in k:
            games.append(k)
        elif "LCS" in k:
            games.append(k)
        elif "LEC 2021" in k:
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
    return generate_embeds(all_matches_after_now)



if __name__ == "__main__":
    [b, a] = get_future_league_games()
    for a in range(0,5):
        logger.info(b[a])

"""
old code
def get_games(count_games_to_return):

    all_games_to_return = []

    schedule = requests.get("https://lol.gamepedia.com/Special:RunQuery/MatchCalendarExport?MCE%5B1%5D=LCS%2F2021+Season%2FLock+In&pfRunQueryFormName=MatchCalendarExport").text
    soup = BeautifulSoup(schedule, 'html.parser')

    content = soup.find(id='mw-content-text').get_text()
    list_content = content.split("\n")

    games = [k for k in list_content if "LCS" in k]

    now = datetime.datetime.now()

    for game in games:
        if game:
            logger.info(game)
            game_data = game.split(",")
            tourney_and_competitors = game_data[0].split(" - ")
            tourney = tourney_and_competitors[0]
            competitors =  tourney_and_competitors[1]

            left_team = ":" + competitors.split(" vs ")[0] + ":"
            right_team = ":" + competitors.split(" vs ")[1] + ":"

            if left_team != "100":
                left_team_emoji = left_team.lower()
            else:
                left_team_emoji = "100~1"
            
            if right_team != "100":
                right_team_emoji = right_team.lower()
            else:
                right_team_emoji = "100~1"

            left_team_emoji = "<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">"
            right_team_emoji = "<:" + right_team_emoji + ":" + str(emoji_id.get(right_team_emoji)) + ">"
            vs_emoji = "<:versus:" + str(emoji_id.get("vs")) + ">"
            
            if left_team_emoji == "<:100~1:None>":
                left_team_emoji = ":100:"
            if right_team_emoji == "<:100~1:None>":
                right_team_emoji = ":100:"

            versus_strig = left_team_emoji + vs_emoji + right_team_emoji

            date_time = game_data[-5:]
            date_time_obj = datetime.datetime(int(date_time[0]), int(date_time[1]), int(date_time[2]), int(date_time[3]), int(date_time[4]))

            # match_string = team1 + " vs " + team2

            if date_time_obj > now and len(all_games_to_return) < count_games_to_return:
                seconds_till = (date_time_obj-now).total_seconds()

                day = seconds_till // (24 * 3600)
                
                time = seconds_till % (24 * 3600)
                hour = time // 3600
                time %= 3600
                minutes = time // 60
                time %= 60

                time_until = "in %d days %d hours %d minutes" % (day, hour, minutes)

                embed = discord.Embed(colour=discord.Colour(0xc7cf39), description=versus_strig, timestamp=date_time_obj)

                # all_games_to_return.append(tourney_and_competitors + " --- " + date_time_obj.strftime("%d-%b-%Y %H:%M") + " --- " + time_until)
                all_games_to_return.append(embed)

    return all_games_to_return

get_future_league_games()

def get_future_league_games():

    list_of_files = glob.glob('python_app/league_schedule/*.csv')  # create the list of file
    all_matches_after_now = []
    list_counter = 0
    for file_name in list_of_files:
        FI = open(file_name, 'r')
        for line in FI:
            game_info_list = line.split(',')

            date = game_info_list[1]
            time = game_info_list[2]

            date_time_str = date + ' ' + time
            date_time = datetime.datetime.strptime(date_time_str.strip('\n'),'%Y-%m-%d %H:%M')

            now = datetime.datetime.now()

            if date_time > now:
                game_obj = game(date_time + datetime.timedelta(hours=3), line.strip('\n'))
                all_matches_after_now.append(game_obj)    
                list_counter = list_counter + 1        
        
        FI.close()

    all_matches_after_now.sort(key=lambda r: r.datetime)
    return generate_embeds(all_matches_after_now)


emoji_id = {
    "lcs": 729112464834166824,
    "lck": 729112464775446628,

    "vs": 729131117436731403,

    "c9": 728503911765246013,
    "tsm": 729060542693638276,
    "fly": 729060542861410459,
    "eg": 729060542404362322,
    "tl": 729060542995497076,
    "imt": 729060542765072436,
    "dig": 729060542819467284,
    "100~1:": 729060542873862155,
    "clg": 729060542848958595,
    "gg": 729060543113068554,

    "af": 729109817398001765,
    "sp": 729109817016451113,
    "dyn": 729109817011994724,
    "kt": 729109816710267054,
    "dwg": 729109815460233246,
    "hle": 729109815451713636,
    "sb": 729109815439261696,
    "gen": 729109815409770496,
    "t1": 729109815543988224,
    "drx": 729109815384604753
}

class game:
    def __init__(self, datetime, full_line):
        self.datetime = datetime
        self.full_line = full_line

def get_future_league_games():

    list_of_files = glob.glob('python_app/league_schedule/*.csv')  # create the list of file
    all_matches_after_now = []
    list_counter = 0
    for file_name in list_of_files:
        FI = open(file_name, 'r')
        for line in FI:
            game_info_list = line.split(',')

            date = game_info_list[1]
            time = game_info_list[2]

            date_time_str = date + ' ' + time
            date_time = datetime.datetime.strptime(date_time_str.strip('\n'),'%Y-%m-%d %H:%M')

            now = datetime.datetime.now()

            if date_time > now:
                game_obj = game(date_time + datetime.timedelta(hours=3), line.strip('\n'))
                all_matches_after_now.append(game_obj)    
                list_counter = list_counter + 1        
        
        FI.close()

    all_matches_after_now.sort(key=lambda r: r.datetime)
    return generate_embeds(all_matches_after_now)

def generate_embeds(list_of_games):
    versus_strings = []
    all_embeds = []
    for game in list_of_games:
        full_string = game.full_line
        game_info = full_string.split(',')
        league_and_versus = game_info[0]
        date = game_info[1]
        time = game_info[2]

        league = "lcs" if "LCS" in league_and_versus else "lck"
        league_emoji = "<:" + league + ":" + str(emoji_id.get(league)) + ">" 

        left_team = league_and_versus.split(" ")[-3]
        right_team = league_and_versus.split(" ")[-1]

        if left_team != "100":
            left_team_emoji = left_team.lower()
        else:
            left_team_emoji = "100~1"
        
        if right_team != "100":
            right_team_emoji = right_team.lower()
        else:
            right_team_emoji = "100~1"

        left_team_emoji = "<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">"
        right_team_emoji = "<:" + right_team_emoji + ":" + str(emoji_id.get(right_team_emoji)) + ">"
        vs_emoji = "<:versus:" + str(emoji_id.get("vs")) + ">"
        
        if left_team_emoji == "<:100~1:None>":
            left_team_emoji = ":100:"
        if right_team_emoji == "<:100~1:None>":
            right_team_emoji = ":100:"

        versus_strig = league_emoji + "       " + left_team_emoji + vs_emoji + right_team_emoji

        game_date_time = datetime.datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
        # , title="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">", description="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + "> test"
        #embed = discord.Embed(timestamp=game_date_time, description=league_emoji + "     " + left_team_emoji + " vs " + right_team_emoji)
        embed = discord.Embed(timestamp=game_date_time + datetime.timedelta(hours=3))
        #embed.set_thumbnail(url="https://am-a.akamaihd.net/image/?resize=120:&f=http%3A%2F%2Fstatic.lolesports.com%2Fleagues%2F1592516205122_LCK-01-FullonDark.png")
        #embed.add_field(name="<:" + left_team_emoji + ":" + str(emoji_id.get(left_team_emoji)) + ">", value=".")
        #embed.add_field(name="<:" + right_team_emoji + ":" + str(emoji_id.get(right_team_emoji)) + ">", value=".")
        versus_strings.append(versus_strig)
        all_embeds.append(embed)

    return versus_strings, all_embeds

"""