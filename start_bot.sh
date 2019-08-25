#!/bin/bash/
npm install npm@latest -g
cd ~/KappaBot/KappaBot/
git pull --all
forever start -a -l kappabot.log index.js -p 8000
