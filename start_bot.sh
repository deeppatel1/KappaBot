#!/bin/bash/
sleep 30
cd ~/KappaBot/KappaBot/
git pull --all
sudo npm install
forever start index.js -p 8000
