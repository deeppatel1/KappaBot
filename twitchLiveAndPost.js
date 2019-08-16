var credentials = require('./configuration.json');
var request = require('request');
var discordPost = require('./discordPost');
var dbQuery = require('./db');

twitchStreamerTracker = {
    t1: {
        channelName: 'loltyler1',
        channelId: "51496027",
        emoji: '',
        discordChannelToPost: "main",
        atorNot: true,
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline',
        URL: "https://www.twitch.tv/loltyler1",
        MoreThan10kPostedDiscord: false
    },
    trick: {
        channelName: 'trick2g',
        channelId: "28036688",
        emoji: '',
        discordChannelToPost: "main",
        atorNot: true,
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline',
        URL: "https://www.twitch.tv/trick2g",
        MoreThan10kPostedDiscord: false
    },
    riotgames: {
        channelName: 'riotgames',
        channelId: "36029255",
        emoji: '',
        discordChannelToPost: "main",
        atorNot: true,
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline',
        URL: "https://www.twitch.tv/riotgames",
        MoreThan10kPostedDiscord: false
    },
    ragen: {
        channelId: "17582288",
        emoji: '',
        discordChannelToPost: "main",
        atorNot: true,
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline',
        URL: "https://www.twitch.tv/itachipower",
        MoreThan10kPostedDiscord: false
    },
    yassuo: {
        channelId: "121203480",
        emoji: '',
        discordChannelToPost: "main",
        atorNot: false,
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline',
        URL: "https://www.twitch.tv/yassuo",
        MoreThan10kPostedDiscord: false
    }
}

module.exports = {

    initiateLiveCheckForTwitchLoop: function (clientfordiscord, Twitcher, intervalLength) {
        setInterval(function () {

            // T1's ID is 51496027
            pollToCheckTwitcherIsLive(Twitcher, clientfordiscord);

        }, intervalLength)
    },


    getTopClips: function (clientForDiscord, twitchStreamer, period, numberOfClips) {
        var options = {
            url: "https://api.twitch.tv/kraken/clips/top?limit=" + numberOfClips + "&channel=" + twitchStreamerTracker[twitchStreamer].channelName + "&period=" + period,
            headers: {
                "Client-ID": credentials.twitchauth,
                "Accept": "application/vnd.twitchtv.v5+json"
            }
        };

        console.log('Twitch Get Top Clips - ' + twitchStreamer + ' ++ ' + options.url);

        request.get(options, function (err, resp, body) {
            data = JSON.parse(body);
            var discordPostWithAllClips = '';
            for (clip in data["clips"]) {
                discordPostWithAllClips = discordPostWithAllClips + "\n https://clips.twitch.tv/" + data["clips"][clip]["slug"];
            }
            discordPost.postToDiscord(clientForDiscord, '', discordPostWithAllClips, false, "main-channel");
        });

    }
};

function pollToCheckTwitcherIsLive(TWITCHer, clientfordiscord) {

    var options = {
        url: "https://api.twitch.tv/helix/streams?user_id=" + twitchStreamerTracker[TWITCHer].channelId,
        headers: {
            "Client-ID": credentials.twitchauth
        }
    };

    request.get(options, function (err, resp, body) {
        console.log('Twitch Check Live - ' + TWITCHer + ' ++ ' + new Date());
        data = JSON.parse(body);
        if (data['data'] != undefined) {
            if (data['data'].length != 0) {
                console.log('Twitch Check Live - ' + TWITCHer + ' said is Live. Now Checking DB');
                //console.log(data);
                var dateStreamStarted = data['data'][0]['started_at'];
                var checkifDateStreamStartedExistsInDatabase = dbQuery.checkURL(dateStreamStarted);
                console.log(TWITCHer + ' stream started at ' + dateStreamStarted);
                checkifDateStreamStartedExistsInDatabase.then(checkifDateStreamStartedExistsInDatabase => {
                    if (!checkifDateStreamStartedExistsInDatabase) {
                        console.log('Twitch Check for ' + TWITCHer + ' says DB is live, now trying to post');
                        var currentdate = new Date();
                        var datetime = getFormattedDate(currentdate);
                        var time = currentdate.getHours() + ":" +
                            currentdate.getMinutes() + ":" +
                            currentdate.getSeconds();


                        var messageToPost = twitchStreamerTracker[TWITCHer]['channelName'] + ' is LIVE ' + twitchStreamerTracker[TWITCHer]['URL'];
                        messageToPost = twitchStreamerTracker[TWITCHer]['atorNot'] ? messageToPost + " <@173611085671170048> <@173610714433454084>" : messageToPost;
                        discordPost.postToDiscord(clientfordiscord, '', messageToPost, false, "main-channel");
                        var sql_query = 'INSERT INTO cxnetwork (date, url, name, time) SELECT \'' + datetime + '\', \'' + dateStreamStarted + '\', \'' + "Twitch" + '\', \'' + time + '\' WHERE NOT EXISTS (SELECT 1 FROM cxnetwork WHERE url=\'' + twitchStreamerTracker[TWITCHer]['URL'] + '\');'
                        dbQuery.query(sql_query);
                    }
                })
            } else {
                //if data == 0, then offline
            }
        }

        /*
        //console.log(data);
        if((data['data'].length != 0) && (!twitchStreamerTracker[TWITCHer].postedToDiscord)){
            if (!twitchStreamerTracker[TWITCHer].postedToDiscord){
                // post on discord
                console.log(TWITCHer + " is LIVE " );
                updateStreamerTracker(clientfordiscord, TWITCHer, "live", "twitch.tv/loltyler1", 0);

                isT1CurrentlyLive = true;
                var hourZULU = data['data'][0]['started_at'].substring(11,13);
                var minutesZULU = parseInt(data['data'][0]['started_at'].substring(14,16));
                var hourEST = (parseInt(hourZULU) - 5 + 24) % 12;
                
                if (minutesZULU < 10)   minutesZULU = '0' + minutesZULU;

                //postToDiscord(discordChannelToPost, AtorNot, "T1 LIVE  https://www.twitch.tv/loltyler1 - stream started at " + hourEST + ':' + (minutesZULU), Twitcher)

                //t1LivePostedOnDiscord = true;
            }
        }else if (data['data'].length == 0){
            
            updateStreamerTracker(clientfordiscord, TWITCHer, "offline");
            
            //console.log('[' + Twitcher + '] Twitch API Says OFFLINE ---- ' + new Date())
            //if (isT1CurrentlyLive)  postToDiscord(discordChannelToPost, true, "T1 stopped streaming", "T1")            
            //isT1CurrentlyLive = false;
            // console.log("not live");
            //t1LivePostedOnDiscord = false;
        }
        */
    });
}

function getFormattedDate(date) {
    var year = date.getFullYear();

    var month = (1 + date.getMonth()).toString();
    month = month.length > 1 ? month : '0' + month;

    var day = date.getDate().toString();
    day = day.length > 1 ? day : '0' + day;

    return year + '/' + month + '/' + day;
}