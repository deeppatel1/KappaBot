#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import datetime

import discord

client = discord.Client()


class game:

    def __init__(self, datetime, full_line):
        self.datetime = datetime
        self.full_line = full_line


list_of_files = glob.glob('league_schedule/*.csv')  # create the list of file

all_matches_after_now = []

@client.event
async def on_message(message):
    if message.content.startswith('!league'):
        print("-")
        for file_name iopen(file_name, 'r')
            for line in FI:
                game_info_list = line.split(',')

                date = game_info_list[1]
                time = game_info_list[2]

                date_time_str = date + ' ' + time
                date_time = datetime.datetime.strptime(date_time_str.strip('\n'),'%Y-%m-%d %H:%M')

                now = datetime.datetime.now()

                if date_time > now:
                    game_obj = game(date_time, line.strip('\n'))
                    all_matches_after_now.append(game_obj)            
            FI.close()

        all_matches_after_now.sort(key=lambda r: r.datetime)

        for x in range(0, len(all_matches_after_now)):
            if x < 6:
                await message.channel.send(all_matches_after_now[x].full_line)

n list_of_files:
            FI = 
client.run('MzEzODM4NTA1Mzc1ODI1OTIw.Xv6yEw.V5JRLBtztRXstP49z4BCAAHrG-k')