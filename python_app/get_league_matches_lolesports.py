import json
import requests
import time
from datetime import datetime, timedelta

API_KEY = '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'

# each id is seperated by %... example "WORLDS_ID"%"LCS_ID"
LEAGUES_IDS = "98767991299243165%2C98767991310872058%2C98767991302996019%2C98767975604431411%98767991325878492"

# only msi for now
LEAGUES_IDS = "98767991325878492"


DIFF_BETWEEN_UTC_AND_EST = 4 # in january this was 5, so after daylight savings (summer) this should be 4


class Team:
    def __init__(self, team_stat):
        self.name = team_stat.get("code")
        self.full_name = team_stat.get("name")
        self.image = team_stat.get("image")
        self.current_record_wins = team_stat.get("record").get("wins") if (team_stat and ("record" in team_stat) and (team_stat.get("record") != None)) else 0
        self.current_record_losses = team_stat.get("record").get("losses") if (team_stat and ("record" in team_stat) and (team_stat.get("record") != None)) else 0
    
        self.result_outcome = team_stat.get("outcome") if (team_stat and ("record" in team_stat) and (team_stat.get("record") != None)) else 0
        self.result_games_won = team_stat.get("gameWins") if (team_stat and ("record" in team_stat) and (team_stat.get("record") != None)) else 0


class Match:
    def __init__(self, match_dict):
        try:
            self.start_time = (datetime.strptime(match_dict.get("startTime"), "%Y-%m-%dT%H:%M:%S.%fZ")) - timedelta(hours=DIFF_BETWEEN_UTC_AND_EST)
        except ValueError:
            self.start_time = (datetime.strptime(match_dict.get("startTime"), "%Y-%m-%dT%H:%M:%SZ")) - timedelta(hours=DIFF_BETWEEN_UTC_AND_EST)

        self.state = match_dict.get("state")
        self.block_name = match_dict.get("blockName")

        self.league_name = match_dict.get("league").get("name") if "league" in match_dict else None
        self.team_1 = Team(match_dict.get("match").get("teams")[0]) if "match" in match_dict and "teams" in match_dict.get("match") and match_dict.get("match").get('teams') else None
        self.team_2 = Team(match_dict.get("match").get("teams")[1]) if "match" in match_dict and "teams" in match_dict.get("match") and match_dict.get("match").get('teams') else None


relevant_teams = ["c9", "tsm", "fly", "tl", "100t", "clg", "eg",
                  "fnc", "g2", "vit",
                  "skt", "dk", "gen"]


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





def call_lolesports_api():
    url = f"https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US&leagueId={LEAGUES_IDS}"
    headers = {
        "x-api-key": API_KEY
    }

    print(url)

    response = requests.get(url, headers=headers)

    if not response.ok:
        raise Exception(f" ----> Failed to call lolesports with status code {response.status_code}")

    resp = response.json()

    return resp


def get_future_events(number_of_games):
    import json
    print(json.dumps(call_lolesports_api()))
    all_matches = call_lolesports_api().get('data').get('schedule').get('events')

    print(f"all_matches --> {all_matches}")
    # print(all_matches)
    # for a in all_matches:
    #     print(a)

    future_matches = [x for x in all_matches if x.get("state") != "completed"]

    # get all games 

    if len(future_matches) > number_of_games*2:
        future_matches = future_matches[0:5*4]

    print(f"---> future matches {future_matches}")

    return future_matches


def parse_future_matches(number_of_games=5):

    future_matches = get_future_events(number_of_games)

    future_matches_messages = []

    for match in future_matches:
        match_obj = Match(match)

        if match_obj:

            team_1_name = match_obj.team_1.name
            team_2_name = match_obj.team_2.name

            # if team_1_name.lower() in relevant_teams or team_2_name.lower() in relevant_teams:
            if True: #for msi or worlds
            
                team_1_emoji = f'<:{team_1_name}:{str(emoji_id.get(team_1_name.lower()))}>' if team_1_name.lower() in emoji_id else team_1_name.upper()
                team_2_emoji = f'<:{team_2_name}:{str(emoji_id.get(team_2_name.lower()))}>' if team_2_name.lower() in emoji_id else team_2_name.upper()
                
                vs_emoji = "<:versus:" + str(emoji_id.get("vs")) + ">"
                game_date_time = "<t:" + str(int(time.mktime(match_obj.start_time.timetuple()))) + ":R>"

                string_to_post = f'{team_1_emoji} ({match_obj.team_1.current_record_wins}-{match_obj.team_1.current_record_losses})  {vs_emoji}  {team_2_emoji} ({match_obj.team_2.current_record_wins}-{match_obj.team_2.current_record_losses})      {game_date_time}'
            
                future_matches_messages.append(string_to_post)

                if len(future_matches_messages) >= number_of_games:
                    break

    return future_matches_messages


def get_future_games(number_of_games):

    future_matches_strings = parse_future_matches(number_of_games)
    return future_matches_strings


get_future_games(5)