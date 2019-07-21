require('dotenv').config();
var credentials = require('./configuration.json');
var Discord = require("discord.js");
var discordFuncs = require('./discordPostAndResponse');
var twitterFunc = require('./twitter');
var twitch = require('./twitchLiveAndPost');
var liveYoutubeCheck = require('./liveYoutubeCheck');
var queryYoutubeVods = require('./queryLastYoutubeVid');
var animeNotifications = require('./animeNotifications');

var clientForDiscord = new Discord.Client();

// TO DO: download node-schedule NPM to schedule the remidners. than use RSS on nyaa.si to link the torrent downloads.

//animeNotifications.makeAniListCall();

clientForDiscord.on('ready', () => {    

    discordFuncs.respondToMessagesLive(clientForDiscord);

    twitterFunc.twitterFilter(clientForDiscord);
    twitch.initiateLiveCheckForTwitchLoop(clientForDiscord, "t1", 49000);
    twitch.initiateLiveCheckForTwitchLoop(clientForDiscord, "yassuo", 320000);
    twitch.initiateLiveCheckForTwitchLoop(clientForDiscord, "ragen", 60000);
    twitch.initiateLiveCheckForTwitchLoop(clientForDiscord, "riotgames", 150000);

    liveYoutubeCheck.initiateLiveCheckLoop(clientForDiscord, "ICE", 20000);
    
    liveYoutubeCheck.initiateLiveCheckLoop(clientForDiscord, "SAM", 300000);

    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'ICE', 600000);
    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'TeamLiquid', 600000);
    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'Cloud9', 590000);
    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'Flyquest', 610000);
    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'TSM', 611000);
    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'HundredT', 621000);
    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'T1', 622000);
    queryYoutubeVods.queryLastYoutube(clientForDiscord, 'T1Vods', 610000);
    
});


clientForDiscord.login(credentials.discordclientlogin);
