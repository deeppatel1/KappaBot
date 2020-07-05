#!/bin/bash/
cd ~/.forever/
rm kappabot.log
touch kappabot.log
sleep 8
cd ~/KappaBot/KappaBot/
git pull --all
python3 python_discord.py
forever start -a -l kappabot.log index.js -p 8000
python3 -m pip install -r requirements.txt
