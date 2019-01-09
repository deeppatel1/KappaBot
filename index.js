require('dotenv').config();
var request = require('request');
var credentials = require('./configuration.json');
var rest = require('node-rest-client').Client;
var Twitter = require('twitter');
var Discord = require("discord.js");
var dbQuery = require('./db.js');

var discordClientGlobalVar;
var neatclipClient = new rest();
var gKey = credentials.gKey;
var clientForDiscord = new Discord.Client();
var Twitterclient = new Twitter({
    consumer_key: credentials.twitterApiKey,
    consumer_secret: credentials.twitterApiSecretKey,
    access_token_key: credentials.twitterAccessToken,
    access_token_secret: credentials.twitterTokenSecret
});


var args = {
    headers: {
        "Client-ID": credentials.twitchauth
    } // request headers
};

var streamersTracker = {
    ICE : {channelId: "UCv9Edl_WbtbPeURPtFDo-uA", emoji: ':baby:', status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    EBZ: {channelId: "UCkR8ndH0NypMYtVYARnQ-_g", emoji: ':older_man::skin-tone-5: ', status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    SAM : {channelId: "UCdSr4xliU8yDyS1aGnCUMTA", emoji: ':hot_pepper: ', status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    SJC : {channelId: "UC4YYNTbzt3X1uxdTCJaYWdg", emoji: ':head_bandage:', status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    CXNews : {channelId: "UCStEQ9BjMLjHTHLNA6cY9vg", emoji: ':newspaper:', status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    MexicanAcne : {channelId: "UC8EmlqXIlJJpF7dTOmSywBg", emoji: ':flushed:', status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    T1 : {channelId: "51496027", emoji: '', status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}
};

function updateStreamerTracker(YTer, status, URL, viewers){

    if (viewers != -1) streamersTracker[YTer].viewers = viewers;

    if ((streamersTracker[YTer].status != 'Online') || (status != 'Live, getting link soon')){
        streamersTracker[YTer].status = status;
        streamersTracker[YTer].URL = URL;
    }

    if ((streamersTracker[YTer].MoreThan10kPostedDiscord == false) && (viewers > 10000)){
        postToDiscord("main", true, YTer + ' HAS MORE THAN 10k VIEWERS', YTer);
        streamersTracker[YTer].MoreThan10kPostedDiscord = true;
    }

    // removed this so it doesnt keep spamming
    // if ((streamersTracker[YTer].MoreThan10kPostedDiscord == true) && (viewers < 10000)){
    //     streamersTracker[YTer].MoreThan10kPostedDiscord = false
    // }

    //console.log(streamersTracker);

}

function firstYTGETRequest(YTer) {

    console.log("[" + YTer + "] " + "starting initial GET request ---- " + new Date());

    return new Promise(function(resolve, reject) {  
        request.get('https://youtube.com/channel/' + streamersTracker[YTer].channelId + '/live', function(err, resp, body) {
            if (err) {
                reject(err);
            } else {
                var isOnline;
                if (body.search("Live stream offline") == -1) {
                    console.log("[" + YTer + "] " + "initial GET says ONLINE ---- " + new Date())
                    updateStreamerTracker(YTer, "Live, getting link soon", "", -1)
                    isOnline = true
                } else {
                    console.log("[" + YTer + "] " + "initial GET says OFFLINE ---- " + new Date())
                    updateStreamerTracker(YTer, "Offline", "", 0)
                    isOnline = false
                }
                resolve(isOnline);
            }
        })
    })
}

function secondYTLiveAPIRequest(YTer) {

    console.log("[" + YTer + "] " + "starting main API request ---- " + new Date());

    // Return new promise 
    return new Promise(function(resolve, reject) {
    	// Do async job
        request.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + streamersTracker[YTer].channelId + "&type=video&eventType=live&key=" + gKey, function(err, resp, body) {
            if (err) {  
                reject(err);
            } else {
                //parse the response now to determine if live by API or NOT
                var parsed = JSON.parse(body);
                //utube API says live, now return result
                if (parsed.items.length > 0) {
                    updateStreamerTracker(YTer, "Online", "https://www.youtube.com/watch?v=" + parsed.items[0].id.videoId, -1)
                    resolve(parsed.items[0].id.videoId);
                }else{
                    console.log("[" + YTer + "] Main API says offline --- " + new Date());
                    updateStreamerTracker(YTer, "Getting link soon", "", 0)
                    resolve("Not Live Yet")
                }
                
            }
        })
    })

}

function getLiveViewers(YTer){
    
    return new Promise(function(resolve, reject) {
    	console.log('-----------------:::' + "https://www.youtube.com/live_stats?v=" + streamersTracker[YTer].URL.split("https://www.youtube.com/watch?v=").pop())
        request.get("https://www.youtube.com/live_stats?v=" + streamersTracker[YTer].URL.split("https://www.youtube.com/watch?v=").pop(), function(err, resp, body) {
            if (err) {  
                reject(err);
            } else {
                body = parseInt(body)
                console.log("NUMBER OF VIEWERS " + body)
                resolve(body)
            }
        })
    })
}

function updateIfMoreThan10kViewers(YTer, millisecondInterval){
    
    setInterval(function() {
        console.log("SDFJSLFJSDLKF" + streamersTracker[YTer].status + streamersTracker[YTer].URL)
        if (streamersTracker[YTer].status == 'Online'){
            getLiveViewers(YTer).then(function(result) {
                console.log("updating streamer tracker ith viewers " + result)
                updateStreamerTracker(YTer, streamersTracker[YTer].status, streamersTracker[YTer].URL, result);
            }, function(err) {
                console.log(err);
            })
        }

    }, millisecondInterval)
    
}

function postToDiscord(discordChannel, atOrNot, stringToPost, YTer){
    // main discord channel is 173611297387184129
    // secondary discord channel is 284157566693539851

    discordChannel = (discordChannel == "main") ? "173611297387184129" : "284157566693539851"

    var stringtoPostWithAt = (atOrNot ? '<@173611085671170048> <@173610714433454084> ' : '');
    console.log("[" + YTer + "] " + "Now posting to discord he/she is live ---- " + new Date())
    
    discordClientGlobalVar.channels.get(discordChannel).send(stringtoPostWithAt + stringToPost)

}

function pollToCheckYTerIsLive(YTer, discordChannelToPost, AtOrNot, online, postedToDiscord) {
    
    return new Promise(function(resolve, reject) {
        //A Get request is initially made cuz uTube API sucks. If live, then we do main API request which is a couple minutes delayed
        firstYTGETRequest(YTer).then(function(result) {
            online = result
            if (!online) postedToDiscord = false

            if ((online) && (!postedToDiscord)) {
                //console.log("[" + YTer + "] " + "starting main YT request " + new Date());
                secondYTLiveAPIRequest(YTer).then(function(secondApiResult){
                    
                    if (secondApiResult != 'Not Live Yet') {
                        // post to discord now
                        // console.log(secondApiResult)

                        // Add URL to database
                        const { Client } = require('pg')
                        const pgClient = new Client()
                        var currentdate = new Date();
                        var datetime = (currentdate.getMonth()+1)+ "/"
                                        + currentdate.getDate()  + "/"
                                        + currentdate.getFullYear() + " @ "
                                        + currentdate.getHours() + ":"
                                        + currentdate.getMinutes() + ":"
                                        + currentdate.getSeconds();
                        const url = "https://www.youtube.com/watch?v=" + secondApiResult;

                        var sql_query = 'INSERT INTO cxnetwork (date, url, name) SELECT \'' + datetime +'\', \'' + url + '\', \'' + YTer + '\' WHERE NOT EXISTS (SELECT 1 FROM cxnetwork WHERE url=\''+ url +'\');'

                        dbQuery.query(sql_query);


                        postToDiscord(discordChannelToPost, AtOrNot, "https://www.youtube.com/watch?v=" + secondApiResult, YTer)
                        postedToDiscord = true
                        resolve(([secondApiResult, online, postedToDiscord]))

                    } else {
                        resolve(([secondApiResult, online, postedToDiscord]))
                    }
                    
                }, function(errSecond){
                    console.log(errSecond);
                })
            }

        }, function(err) {
            console.log(err);
        })
    })
}

function pollToCheckTwitcherIsLive(Twitcher, AtorNot, isT1CurrentlyLive, t1LivePostedOnDiscord, discordChannelToPost){
    
    var options = {
        url: "https://api.twitch.tv/helix/streams?user_id=" +  streamersTracker[Twitcher].channelId,
        headers: {
            "Client-ID": credentials.twitchauth
        }
    };

    return new Promise(function(resolve, reject) {
        request.get(options, function(err, resp, body) {
            data = JSON.parse(body);
            if((data['data'].length != 0) && (!isT1CurrentlyLive)){
                if (!t1LivePostedOnDiscord){
                    // post on discord
                    console.log('[' + Twitcher + '] Twitch API Says LIVE, attempting to post now ---- ' + new Date())
                    isT1CurrentlyLive = true;
                    var hourZULU = data['data'][0]['started_at'].substring(11,13);
                    var minutesZULU = parseInt(data['data'][0]['started_at'].substring(14,16));
                    var hourEST = (parseInt(hourZULU) - 5 + 24) % 12;
                    
                    if (minutesZULU < 10)   minutesZULU = '0' + minutesZULU;
    
                    postToDiscord(discordChannelToPost, AtorNot, "T1 LIVE  https://www.twitch.tv/loltyler1 - stream started at " + hourEST + ':' + (minutesZULU), Twitcher)
    
                    t1LivePostedOnDiscord = true;
                }
            }else if (data['data'].length == 0){
                console.log('[' + Twitcher + '] Twitch API Says OFFLINE ---- ' + new Date())
                if (isT1CurrentlyLive)  postToDiscord(discordChannelToPost, true, "T1 stopped streaming", "T1")            
                isT1CurrentlyLive = false;
                // console.log("not live");
                t1LivePostedOnDiscord = false;
            }
            resolve([isT1CurrentlyLive, t1LivePostedOnDiscord])
        });
        
    })
}

function initiateLiveCheckLoop(YTer, discordChannelToPost, AtOrNot, online, postedToDiscord, intervalLength) {

    //console.log(intervalLength)
    setInterval(function() {
        pollToCheckYTerIsLive(YTer, discordChannelToPost, AtOrNot, online, postedToDiscord).then(function(result) {
            online = result[1]
            postedToDiscord = result[2]

            //console.log("online is " + online);
            //console.log("postedToDiscord " + postedToDiscord)
        })
    }, intervalLength)
    
}

function initiateLiveCheckForTwitchLoop(Twitcher, discordChannelToPost, AtOrNot, online, postedToDiscord, intervalLength) {    

    setInterval(function() {
        // T1's ID is 51496027
        pollToCheckTwitcherIsLive(Twitcher, AtOrNot, online, postedToDiscord, discordChannelToPost).then(function(result) {
            online = result[0]
            postedToDiscord = result[1]
        })

    }, intervalLength)
}

function twitterFilter(discordChannelToPost){
    
    Twitterclient.stream('statuses/filter', {
        //solonoid12 is 1615735502
        follow: '4833803780,736784706486734852,344538810,873949601522487297'
    }, function(stream) {

        stream.on('data', function(tweet) {
            //console.log(tweet)
            if ((tweet.user.screen_name == 'solonoid12') || (tweet.user.screen_name == 'loltyler1') || (tweet.user.screen_name == 'REALIcePoseidon') || (tweet.user.screen_name == 'TLDoublelift') || (tweet.user.screen_name == 'JacobK_Cx')) {
                //discordClient.channels.get("").send("<@173611085671170048> <@173610714433454084> https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str);
                postToDiscord(discordChannelToPost, true, "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str, "Twitter - " + tweet.user.screen_name)
            }
        });

        stream.on('error', function(error) {
            console.log(error);
        });
    });
}

function continuousYTAndTwitchCheck(){

    clientForDiscord.on('ready', () => {

        discordClientGlobalVar = clientForDiscord;

        twitterFilter("main")

        initiateLiveCheckLoop("MexicanAcne", "secondary", false, false, false, 300000);
        initiateLiveCheckLoop("SJC", "secondary", false, false, false, 275000);
        initiateLiveCheckLoop("EBZ", "secondary", false, false, false, 285000);
        initiateLiveCheckLoop("SAM", "secondary", false, false, false, 270000);
		initiateLiveCheckLoop("CXNews", "main", true, false, false, 350000);
		initiateLiveCheckLoop("ICE", "main", true, false, false, 250000);

        initiateLiveCheckForTwitchLoop("T1", "main", true, false, false, 250000)

        updateIfMoreThan10kViewers("ICE", 5000)
        
	});

}

function postSummary(channel){

    // var iceEmoji = (streamersTracker['ICE'].status != "Offline") ? ':baby: ' : ''
    // var ebzEmoji = (streamersTracker['EBZ'].status != "Offline") ? ':bust_in_silhouette: ' : ''
    // var pepperPalEmoji = (streamersTracker['SAM'].status != "Offline") ? ':hot_pepper: ' : ''
    // var sjcEmoji = (streamersTracker['SJC'].status != "Offline") ? ':head_bandage: ' : ''
    // var acneEmoji = (streamersTracker['MexicanAcne'].status != "Offline") ? ':flushed: ' : ''
    // var cxNewsEmoji = (streamersTracker['CXNews'].status != "Offline") ? ':newspaper: ' : ''

    // var stringToPost = 'ICE - ' + iceEmoji + streamersTracker['ICE'].status + "  " + streamersTracker['ICE'].URL + '\n'
    // stringToPost = stringToPost + 'EBZ - ' + ebzEmoji + streamersTracker['EBZ'].status + "  " + streamersTracker['EBZ'].URL + '\n'
    // stringToPost = stringToPost + 'SAM - ' + pepperPalEmoji + streamersTracker['SAM'].status + "  " + streamersTracker['SAM'].URL + '\n'
    // stringToPost = stringToPost + 'SJC - ' + sjcEmoji + streamersTracker['SJC'].status + "  " + streamersTracker['SJC'].URL + '\n'
    // stringToPost = stringToPost + 'CXNews - ' + cxNewsEmoji + streamersTracker['CXNews'].status + "  " + streamersTracker['CXNews'].URL + '\n'
    // stringToPost = stringToPost + 'MexicanAcne - ' + acneEmoji + streamersTracker['MexicanAcne'].status + "  " + streamersTracker['MexicanAcne'].URL + '\n'


    const embed = new Discord.RichEmbed()
    .setTitle('Commands')
    .setColor("#67279C")

    for (data in streamersTracker) {
        if (streamersTracker[data].status == "Online") {
            embed.addField(data + " - " + streamersTracker[data].emoji, "[link -- replace with YT title?](" + streamersTracker[data].URL + ")")
        }
    }


    channel.send(embed);

    /*
    const embed = {
        "title": "Live Streamers",
        "color": 14229326,
        "timestamp": "2018-12-29T23:12:35.836Z",
        "fields": [{
                "name": "streamersTracker - " + streamersTracker['ICE'].status,
                //"value": streamersTracker['ICE'].URL,
                "value": 'https://www.youtube.com/watch?v=HlIpWA7nmM4',

                "inline": true
            },{
                "name": "Sam - " + streamersTracker['SAM'].status,
                //"value": streamersTracker['SAM'].URL,
                "value": "streamersTracker['ICE'].URL,",

                "inline": true
            },{
                "name": "MexicanAcne - " + streamersTracker['MexicanAcne'].status,
//                "value": streamersTracker['MexicanAcne'].URL,
                "value": "streamersTracker['ICE'].URL,",

                "inline": true
            },{
                "name": "EBZ - " + streamersTracker['EBZ'].status,
                //"value": streamersTracker['EBZ'].URL,
                "value": "streamersTracker['ICE'].URL,",

                "inline": true
            },{
                "name": "SJC - " + streamersTracker['SJC'].status,
                //"value": streamersTracker['SJC'].URL,
                "value": "streamersTracker['ICE'].URL,",

                "inline": true
            }
        ]
    };
    channel.send({ embed });
    */
}

function respondToMessagesLive(){

    clientForDiscord.on("message", function(message) {

        if (message.content.startsWith("--h") || message.content.startsWith("?help")) {
            const embed = new Discord.RichEmbed()
                .setTitle('Commands')
                .setColor("#67279C")
                .addField("?ice last #", "Get the last {#} of vod urls")
                .addField("!clips hour/day/week/month/year/alltime #", "Get most popular clips for last hour/day/week/month/year/alltime")
                .addField("!ice hour/day/week/month/year/alltime #", "Get most popular clips for ice for the last hour/day/week/month/year/alltime")
                .addField("?vod {name} {number}", "Gets the last {number} of vods for a particular streamer.\n{name}: EBZ, SAM, SJC, CXNews, MexicanAcne")

            message.channel.send(embed)
        } else if (message.content.startsWith("!ice")) {
            var args = message.content.split(/ +/g);
            var inHowLongDuration = args[1]; //can be hour for last hour, day..., week..., month..., year..., alltime
            var howManyClips = args[2]; //how many clips to show
            var stringToSend = "";

            //console.log(args)

            neatclipClient.get("https://neatclip.com/api/v1/clips.php?streamer_url=https://www.youtube.com/channel/UCv9Edl_WbtbPeURPtFDo-uA&time=" + inHowLongDuration + "&sort=top", arguments, function(data, response) {

                var size = howManyClips
                if (data.length < size) size = data.length;
                for (var x = 0; x < size; x++) {
                    var entry = [data[x]["slugID"], data[x]["viewsAll"]];
                    stringToSend = stringToSend + "https://neatclip.com/clip/" + data[x]["slugId"] + " views:" + data[x]["viewsAll"] + "\n";
                }

                message.channel.send(stringToSend)

            });

        } else if (message.content.startsWith('!clips')) {
            var args = message.content.split(/ +/g);
            var inHowLongDuration = args[1]; //can be hour for last hour, day..., week..., month..., year..., alltime
            var howManyClips = args[2]; //how many clips to show
            var stringToSend = "";
            neatclipClient.get("https://neatclip.com/api/v1/clips.php?time=" + inHowLongDuration + "&sort=top", arguments, function(data, response) {

                var size = howManyClips;

                if (data.length < size) size = data.length;
                for (var x = 0; x < size; x++) {
                    var entry = [data[x]["slugID"], data[x]["viewsAll"]];
                    stringToSend = stringToSend + "https://neatclip.com/clip/" + data[x]["slugId"] + " views:" + data[x]["viewsAll"] + "\n";
                }
                message.channel.send(stringToSend);
            });

        } /*else if (message.content.startsWith('!ice last')) {

            var numberofVods = message.content.split(" ");
            const num = numberofVods[2];
            if (numberofVods.length == 3) {
                dbQuery.queryVod(num, message);
            }
            // readLastLines.read('icevods.txt',numberofVods).then((lines) =>
            //     message.channel.send(lines));
        } else if (message.content.startsWith('?vod')) {
            var numberofVods = message.content.split(" ");
            const num = numberofVods[2];
            const name = numberofVods[1];

            if (numberofVods.length == 3) {
                dbQuery.queryOthers(num, name, message);
            }

        }*/ 
        else if (message.content.startsWith('!update')) {

            message.channel.send(':thinking:')

            // second parameter is which discord channel, main channel or secondary channel
            // third is "at or not" ... at people or not

            pollToCheckYTerIsLive("ICE", "main", true, false, false);

            // EBZz channel ID is UCkR8ndH0NypMYtVYARnQ-_g
            pollToCheckYTerIsLive("EBZ", "secondary", false, false, false);

            // SAMs channel ID is UCdSr4xliU8yDyS1aGnCUMTA
            pollToCheckYTerIsLive("SAM", "secondary", false, false, false);

            // SJCs channel ID is UC4YYNTbzt3X1uxdTCJaYWdg
            pollToCheckYTerIsLive("SJC", "secondary", false, false, false);

            // CXNews channel ID is UCStEQ9BjMLjHTHLNA6cY9vg
            pollToCheckYTerIsLive("CXNews", "main", false, false, false);

            // MexicanAcnes channel ID is UC8EmlqXIlJJpF7dTOmSywBg
            pollToCheckYTerIsLive("MexicanAcne", "secondary", false, false, false);

            setTimeout(postSummary, 3000, message.channel);

        } else if (message.content.startsWith('?vod ')) {
            var numberofVods = message.content.split(" ");
            const num = numberofVods[2];
            const name = numberofVods[1];

            if (numberofVods.length == 3) {
                dbQuery.queryOthers(num, name, message);
            }
        } else if (message.content.startsWith('?ice last')){
            var numberofVods = message.content.split(" ");
            const num = numberofVods[2];
            if (numberofVods.length == 3) {
                dbQuery.queryVod(num, message);
            }
            // readLastLines.read('icevods.txt',numberofVods).then((lines) =>
            //     message.channel.send(lines));
        }

    });

}

respondToMessagesLive()
continuousYTAndTwitchCheck()

clientForDiscord.login(credentials.discordclientlogin);
