#!/bin/bash/
sleep 30
cd ~/KappaBot/KappaBot/
git pull --all
forever -l kappabot.log index.js -p 8000
