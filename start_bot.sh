#!/bin/bash/
npm install npm@latest -g
sleep 50
cd ~/KappaBot/KappaBot/
git pull --all
forever start -a -l kappabot.log index.js -p 8000
