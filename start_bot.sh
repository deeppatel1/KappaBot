#!/bin/bash/
cd /home/kapp/.forever/
rm kappabot.log
touch kappabot.log
sleep 8
cd /home/kapp/KappaBot/KappaBot/
git pull --all
forever start -a -l /home/kapp/.forever/kappabot.log index.js -p 8000
pip3 install --upgrade
pip3 install -r requirements.txt
#forever start -a -l /home/kapp/.forever/kappabot.log -c python3 python_discord.py