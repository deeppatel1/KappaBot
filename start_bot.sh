#!/bin/bash/
cd ~/.forever/
rm kappabot.log
touch kappabot.log
sleep 8
cd ~/KappaBot/KappaBot/
git pull --all
forever start -a -l kappabot.log index.js -p 8000
pip install -r requirements.txt
python python_discord.py
