#!/bin/bash/
sleep 8
cd ~/KappaBot/KappaBot/
git pull --all
forever -a -l kappabot.log index.js -p 8000
