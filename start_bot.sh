#!/bin/bash/
sudo chown +755 kapp:kapp /home/kapp/KappaBot/KappaBot/.git/*
sudo su kapp
# cd /home/kapp/.forever/
# rm kappabot.log
# touch kappabot.log
# sleep 8
cd /home/kapp/KappaBot/KappaBot/
git pull --all

docker build -t kappabot .
docker run kappabot


# forever start -a index.js -p 8000
# forever start -a -l /home/kapp/.forever/kappabot.log index.js -p 8000
# pip3 install --upgrade
# pip3 install -r requirements.txt
# python3 python_discord.py
