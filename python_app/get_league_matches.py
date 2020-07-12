import glob
import datetime
import discord

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
