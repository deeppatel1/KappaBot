require('dotenv').config();
var request = require('request');
var credentials = require('./configuration.json');
var rest = require('node-rest-client').Client;
var Twitter = require('twitter');
const Discord = require("discord.js");
const clientForDiscord = new Discord.Client();
var dbQuery = require('./db.js');


var neatclipClient = new rest();
var gKey = credentials.gKey;
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

function firstYTGETRequest(YTer, YTChannelName) {

    // console.log("[" + YTer + "] " + "starting initial GET request " + new Date());

    return new Promise(function(resolve, reject) {  
        request.get('https://youtube.com/channel/' + YTChannelName + '/live', function(err, resp, body) {
            if (err) {
                reject(err);
            } else {
                var isOnline;
                if (body.search("Live stream offline") == -1) {
                    console.log("[" + YTer + "] " + "initial GET says ONLINE");
                    isOnline = true
                } else {
                    console.log("[" + YTer + "] " + "initial GET says OFFLINE")
                    isOnline = false
                }
                resolve(isOnline);
            }
        })
    })
}

function secondYTLiveAPIRequest(YTer, YTChannelName) {

    // console.log("[" + YTer + "] " + "starting main API request " + new Date());

    // Return new promise 
    return new Promise(function(resolve, reject) {
    	// Do async job
        request.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + YTChannelName + "&type=video&eventType=live&key=" + gKey, function(err, resp, body) {
            if (err) {  
                reject(err);
            } else {
                //parse the response now to determine if live by API or NOT
                var parsed = JSON.parse(body);
                //utube API says live, now return result
                if (parsed.items.length > 0) {
                    resolve(parsed.items[0].id.videoId);
                }else{
                    // console.log("[" + YTer + "] Main API says offline --- " + new Date());
                    resolve("Not Live Yet")
                }
                
            }
        })
    })

}

function postToDiscord(channelId, atOrNot, stringToPost, discordClient, YTer){
    
    var stringtoPostWithAt = (atOrNot ? '<@173611085671170048> <@173610714433454084> ' : '');		                        
    // console.log("[" + YTer + "] " + "Now posting to discord he/she is live ")
    discordClient.channels.get(channelId).send(stringtoPostWithAt + stringToPost)

}

function pollToCheckYTerIsLive(YTer, YTChannelName, discordChannelToPost, discordClient, AtOrNot, online, postedToDiscord) {
    
    return new Promise(function(resolve, reject) {
        //A Get request is initially made cuz uTube API sucks. If live, then we do main API request which is a couple minutes delayed
        firstYTGETRequest(YTer, YTChannelName).then(function(result) {
            online = result
            if (!online) postedToDiscord = false

            if ((online) && (!postedToDiscord)) {
                //console.log("[" + YTer + "] " + "starting main YT request " + new Date());
                secondYTLiveAPIRequest(YTer, YTChannelName).then(function(secondApiResult){
                    
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


                        postToDiscord(discordChannelToPost, true, "https://www.youtube.com/watch?v=" + secondApiResult, discordClient, YTer)
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

function initiateLiveCheckLoop(YTer, YTChannelName, discordChannelToPost, discordClient, AtOrNot, online, postedToDiscord, intervalLength) {

    // console.log(intervalLength)
    setInterval(function() {
        pollToCheckYTerIsLive(YTer, YTChannelName, discordChannelToPost, discordClient, AtOrNot, online, postedToDiscord).then(function(result) {
            online = result[1]
            postedToDiscord = result[2]

            // console.log("online is " + online);
            // console.log("postedToDiscord " + postedToDiscord)
        })        
    }, intervalLength)
    
}

function twitterFilter(discordClient){
    
    Twitterclient.stream('statuses/filter', {
        follow: '4833803780,736784706486734852,344538810,873949601522487297'
    }, function(stream) {
        stream.on('data', function(tweet) {
            if ((tweet.user.screen_name == 'loltyler1') || (tweet.user.screen_name == 'REALIcePoseidon') || (tweet.user.screen_name == 'TLDoublelift') || (tweet.user.screen_name == 'JacobK_Cx')) {
                client.channels.get("173611297387184129").send("<@173611085671170048> <@173610714433454084> https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str);
                postToDiscord("173611297387184129", true, "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str, discordClient, "T1")
            }
        });

        stream.on('error', function(error) {
            console.log(error);
        });
    });
}

function continuousYTCheck(){

    clientForDiscord.on('ready', () => {

        twitterFilter(clientForDiscord)

        initiateLiveCheckLoop("MexicanAcne", "UC8EmlqXIlJJpF7dTOmSywBg", "284157566693539851", clientForDiscord, false, false, false, 300000);
        initiateLiveCheckLoop("SJC", "UC4YYNTbzt3X1uxdTCJaYWdg", "284157566693539851", clientForDiscord, false, false, false, 300000);
        initiateLiveCheckLoop("EBZ", "UCkR8ndH0NypMYtVYARnQ-_g", "284157566693539851", clientForDiscord, false, false, false, 300000);
        initiateLiveCheckLoop("SAM", "UCdSr4xliU8yDyS1aGnCUMTA", "284157566693539851", clientForDiscord, false, false, false, 300000);
		initiateLiveCheckLoop("CXNews", "UCStEQ9BjMLjHTHLNA6cY9vg","173611297387184129", clientForDiscord, true, false, false, 300000);
		initiateLiveCheckLoop("ICE", "UCv9Edl_WbtbPeURPtFDo-uA","173611297387184129", clientForDiscord, true, false, false, 300000);
	
	});

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

            // console.log(args)

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

        }*/ else if (message.content.startsWith('!update')) {
            // main discord channel is 173611297387184129
            // secondary discord channel is 284157566693539851

            //checkifYTFunction paramters are 1) name of YTer, 2) YT Channel ID, 3) Discord Channel to post to, 4)Millisecond to refresh, 5) discord client passed in

            pollToCheckYTerIsLive("ICE", "UCv9Edl_WbtbPeURPtFDo-uA", "173611297387184129", clientForDiscord, true, false, false);

            // EBZz channel ID is UCkR8ndH0NypMYtVYARnQ-_g
            pollToCheckYTerIsLive("EBZ", "UCkR8ndH0NypMYtVYARnQ-_g", "284157566693539851", clientForDiscord, true, false, false);

            // SAMs channel ID is UCdSr4xliU8yDyS1aGnCUMTA
            pollToCheckYTerIsLive("SAM", "UCdSr4xliU8yDyS1aGnCUMTA", "284157566693539851", clientForDiscord, true, false, false);

            // SJCs channel ID is UC4YYNTbzt3X1uxdTCJaYWdg
            pollToCheckYTerIsLive("SJC", "UC4YYNTbzt3X1uxdTCJaYWdg", "284157566693539851", clientForDiscord, true, false, false);

            // CXNews channel ID is UCStEQ9BjMLjHTHLNA6cY9vg
            pollToCheckYTerIsLive("CXNews", "UCStEQ9BjMLjHTHLNA6cY9vg", "173611297387184129", clientForDiscord, true, false, false);

            // MexicanAcnes channel ID is UC8EmlqXIlJJpF7dTOmSywBg
            pollToCheckYTerIsLive("MexicanAcne", "UC8EmlqXIlJJpF7dTOmSywBg", "284157566693539851", clientForDiscord, true, false, false);

        }

    });

}

respondToMessagesLive()
continuousYTCheck()
twitterFilter()

clientForDiscord.login(credentials.discordclientlogin);