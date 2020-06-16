var request = require('request');
var dbQuery = require('./db');
var discordPost = require('./discordPost');
var credentials = require('./configuration.json');

gKey = credentials.gKey;
var streamersTracker = {
    ICE: {
        channelId: "UCv9Edl_WbtbPeURPtFDo-uA",
        emoji: ':baby:',
        discordChannelToPost: "main",
        atorNot: true,
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline',
        URL: "",
        viewers: 0,
        MoreThan10kPostedDiscord: false,
        filters: []
    },
    T1: {
        channelId: "UCwV_0HmQkRrTcrReaMxPeDw",
        discordChannelToPost: "main",
        atorNot: true,
        lastVideoID: '',
        filters: []
    },
    T1Vods: {
        channelId: "UCzjyMXv0jg1RBg1PAdYmHsQ",
        discordChannelToPost: "main",
        atorNot: true,
        lastVideoID: '',
        filters: []
    },
    IRLMoments: {
        channelId: "UCK3LEiOxZacoXc5uBx3hJaw",
        discordChannelToPost: "main",
        atorNot: true,
        lastVideoID: '',
        filters: []
    },
    TeamLiquid: {
        channelId: "UCLSWNf28X3mVTxTT3_nLCcw",
        discordChannelToPost: "main",
        atorNot: true,
        lastVideoID: '',
        filters: ['SQUAD']
    },
    Cloud9: {
        channelId: "UCEkorHXUNJ5tpcH0VE77_fA",
        discordChannelToPost: "main",
        atorNot: true,
        lastVideoID: '',
        filters: ['On Cloud9']
    },
    Flyquest: {
        channelId: "UCy0omD6TIJklBme14VQqV6A",
        discordChannelToPost: "main",
        atorNot: false,
        lastVideoID: '',
        filters: ['FlyVlog']
    },
    TSM: {
        channelId: "UC4Ndz98NI_-9VQM3E7fctnQ",
        discordChannelToPost: "main",
        atorNot: false,
        lastVideoID: '',
        filters: ['LEGENDS']
    },
    HundredT: {
        channelId: "UCnrX2_FoKieobtw19PiphDw",
        discordChannelToPost: "main",
        atorNot: true,
        lastVideoID: '',
        filters: ['Heist']
    },
};


module.exports = {
    queryLastYoutube: function (clientForDiscord, YTer, interval) {
        setInterval(function () {

            queryLastYoutubeSingle(clientForDiscord, YTer);

        }, interval)
    }
}


function queryLastYoutubeSingle(clientForDiscord, YTer) {

    request.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + streamersTracker[YTer].channelId + "&maxResults=1&order=date&type=video&key=" + gKey, function (err, resp, body) {

        console.log('YOUTUBE VOD CHECK - querying youtube for vids: ' + YTer + ' at ' + new Date());

        if (err) {
            reject(err);
        } else {
            console.log("Body of VID IS: " + body);
            body = JSON.parse(body);
            var videoId = body.items[0].id.videoId;
            var url = "https://www.youtube.com/watch?v=" + videoId;

            var checkIfURLExistsInDatabase = dbQuery.checkURL(url);

            checkIfURLExistsInDatabase.then(checkIfURLExistsInDatabase => {
                if (!checkIfURLExistsInDatabase) { //If the video is not in the DB, do all this
                    // Add video to database
                    console.log(YTer + ' Database said this video is live and doesnt exist in data base ' + url);
                    var currentdate = new Date();
                    var datetime = getFormattedDate(currentdate);
                    var time = currentdate.getHours() + ":" +
                        currentdate.getMinutes() + ":" +
                        currentdate.getSeconds();

                    var properVidToPost = false;
                    console.log('filter check length: ' + streamersTracker[YTer].filters.length);

                    if (streamersTracker[YTer].filters.length == 0) {
                        properVidToPost = true;
                    } else {

                        for (filter in streamersTracker[YTer].filters) {
                            console.log('YOUTUBE VOD CHECK - checking filter: ' + filter + ' with this uRL: ' + body.items[0].snippet.title);
                            if (body.items[0].snippet.title.includes(streamersTracker[YTer].filters[filter])) {
                                console.log('YOUTUBE VOD CHECK - checked it exists, now making properVidTOPsotTrue');
                                properVidToPost = true;
                            }
                        }
                    }

                    if (properVidToPost) {
                        if (videoId != streamersTracker[YTer].lastVideoID) {
                            streamersTracker[YTer].lastVideoID = videoId;

                            const embed = {
                                "thumbnail": {
                                    "url": body.items[0].snippet.thumbnails.medium.url
                                },
                                "color": 4922096,
                                "timestamp": body.items[0].snippet.publishedAt,
                                "author": {
                                    "name": YTer + " - " + body.items[0].snippet.title,
                                },
                                "fields": [{
                                    "name": "-",
                                    "value": body.items[0].snippet.description
                                }]
                            };

                            //discordPost.postToDiscord(clientForDiscord, '', "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str, "Twitter - " + tweet.user.screen_name, false, "main-channel");
                            //discordPost.postToDiscord(clientForDiscord, '', { embed }, true, "main-channel");
                            var messageToPost = (streamersTracker[YTer].atorNot) ? "<@173611085671170048> <@173610714433454084> https://www.youtube.com/watch?v=" + videoId : "https://www.youtube.com/watch?v=" + videoId;
                            //var messageToPost = twitchStreamerTracker[TWITCHer]['atorNot'] ? messageToPost + " <@173611085671170048> <@173610714433454084>" : messageToPost;
                            //discordPost.postToDiscord(clientForDiscord, '', messageToPost, " Youtube - ! ", false, "main-channel");
                            discordPost.postToDiscord(clientForDiscord, '', messageToPost, false, "main-channel");
                            //discordPost.postToDiscord(clientfordiscord, '', messageToPost, false, "main-channel");
                            var sql_query = 'INSERT INTO cxnetwork (date, url, name, time) SELECT \'' + datetime + '\', \'' + url + '\', \'' + "YouTube" + '\', \'' + time + '\' WHERE NOT EXISTS (SELECT 1 FROM cxnetwork WHERE url=\'' + url + '\');'
                            dbQuery.query(sql_query);

                        }
                    }
                }
            });

        }
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
