#!/bin/bash/
sleep 8
cd ~/KappaBot/KappaBot/
git pull --all
npm install
forever start -a -l kappabot.log index.js -p 8000
