require('dotenv').config();
var credentials = require('./configuration.json');
var Discord = require("discord.js");
var discordFuncs = require('./discordPostAndResponse');
var twitterFunc = require('./twitter');
var twitch = require('./twitchLiveAndPost');
var liveYoutubeCheck = require('./liveYoutubeCheck');
var queryYoutueVods = require('./queryLastYoutubeVid');

var clientForDiscord = new Discord.Client();


clientForDiscord.on('ready', () => {    
    discordFuncs.respondToMessagesLive(clientForDiscord);
    //twitterFunc.twitterFilter(clientForDiscord);
    //twitch.initiateLiveCheckForTwitchLoop(clientForDiscord, "T1", 30000);
    twitch.initiateLiveCheckForTwitchLoop(clientForDiscord, "ragen", 30000);
    liveYoutubeCheck.initiateLiveCheckLoop(clientForDiscord, "ICE", 20000);
    //liveYoutubeCheck.initiateLiveCheckLoop(clientForDiscord, "EBZ", 300000);
    queryYoutueVods.queryLastYoutube(clientForDiscord, 'CXClips2', 5000);

    queryYoutueVods.queryLastYoutube(clientForDiscord, 'CXClips', 5000);
});


clientForDiscord.login(credentials.discordclientlogin);








// TO DO: Save the lastVideoId in database, and instead of checking streamersTracker[YTER][lastVideoId], check the database
/*
var streamersTracker = {
    DEEP : {channelId: "UC3Nlcpu-kbLmdhph_BN7OwQ", emoji: ':baby:', discordChannelToPost: "main", atorNot: false, postedToDiscord: false, lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    ICE : {channelId: "UCv9Edl_WbtbPeURPtFDo-uA", emoji: ':baby:', discordChannelToPost: "main", atorNot: false, postedToDiscord: false, lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false, filters: []}, 
    EBZ: {channelId: "UCUn24NHjc8asGiYet1P9h5Q", emoji: ':older_man::skin-tone-5: ', discordChannelToPost: "secondary", atorNot: false, postedToDiscord: false, lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    SAM : {channelId: "UCdSr4xliU8yDyS1aGnCUMTA", emoji: ':hot_pepper: ', discordChannelToPost: "secondary", atorNot: false, postedToDiscord:false , lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    SJC : {channelId: "UC4YYNTbzt3X1uxdTCJaYWdg", emoji: ':head_bandage:', discordChannelToPost: "secondary", atorNot: false, postedToDiscord:false , lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    CXNews : {channelId: "UCStEQ9BjMLjHTHLNA6cY9vg", emoji: ':newspaper:', discordChannelToPost: "main", atorNot: true, postedToDiscord:false , lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    MexicanAcne : {channelId: "UC8EmlqXIlJJpF7dTOmSywBg", emoji: ':flushed:', discordChannelToPost: "secondary", atorNot: false, postedToDiscord:false , lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    T1 : {channelId: "51496027", emoji: '', discordChannelToPost: "main", atorNot: true, postedToDiscord: false, postedToDiscord : false, lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    trick : {channelId: "28036688", emoji: '', discordChannelToPost: "main", atorNot: true, postedToDiscord: false, postedToDiscord : false, lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    Hyphonix : {channelId: "UCaFpm67qMk1W1wJkFhGXucA", emoji: '', discordChannelToPost: "main", atorNot: false, postedToDiscord : false, lastVideoID: '',
        status: 'offline', URL:"", viewers: 0, MoreThan10kPostedDiscord: false},

    CXClips : {channelId: "UCFthsIV3Bp11cRwb6R9AOOw", discordChannelToPost: "main", atorNot: false, lastVideoID: '', filters: []},
    TeamLiquid : {channelId: "UCLSWNf28X3mVTxTT3_nLCcw", discordChannelToPost: "main", atorNot: false, lastVideoID: '', filters: ['SQUAD']},
    Cloud9 : {channelId: "UCEkorHXUNJ5tpcH0VE77_fA", discordChannelToPost: "main", atorNot: false, lastVideoID: '', filters: ['On Cloud9']},
    Flyquest : {channelId: "UCy0omD6TIJklBme14VQqV6A", discordChannelToPost: "main", atorNot: false, lastVideoID: '', filters: ['FlyVlog']},
    TSM : {channelId: "UC4Ndz98NI_-9VQM3E7fctnQ", discordChannelToPost: "main", atorNot: false, lastVideoID: '', filters: ['LEGENDS']},    
    HundredT : {channelId: "UCnrX2_FoKieobtw19PiphDw", discordChannelToPost: "main", atorNot: false, lastVideoID: '', filters: ['Heist']},

};
*/

/*

function queryLastYoutube(YTer, interval){
    setInterval(function() {
        
        queryLastYoutubeSingle(YTer);

    }, interval)
}




function queryLastYoutubeSingle(YTer){

    request.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + streamersTracker[YTer].channelId + "&maxResults=1&order=date&type=video&key=" + gKey, function(err, resp, body) {
   
        console.log('querying youtube for vids: ' + YTer + ' at ' + new Date());

        if (err) {
            reject(err);
        } else {
            //console.log("Body of VID IS: " + body);
            body = JSON.parse(body);
            var videoId = body.items[0].id.videoId;
            var url = "https://www.youtube.com/watch?v=" + videoId;

            console.log(videoId);
            var checkIfURLExistsInDatabase = dbQuery.checkURL(url);

            checkIfURLExistsInDatabase.then(checkIfURLExistsInDatabase => {
                if (!checkIfURLExistsInDatabase) {   //If the video is not in the DB, do all this
                    // Add video to database
                    var currentdate = new Date();
                    var datetime = getFormattedDate(currentdate);
                    var time = currentdate.getHours() + ":"
                                + currentdate.getMinutes() + ":"
                                + currentdate.getSeconds();
                    var sql_query = 'INSERT INTO cxnetwork (date, url, name, time) SELECT \'' + datetime +'\', \'' + url + '\', \'' + "YouTube" + '\', \'' + time + '\' WHERE NOT EXISTS (SELECT 1 FROM cxnetwork WHERE url=\''+ url +'\');'
                    dbQuery.query(sql_query);
    
    
                    var properVidToPost = false;
    
                    console.log("Checking filters");
                    if (streamersTracker[YTer].filters.length == 0) {
                        properVidToPost = true;
                    } else {
                        
                        for (filter in streamersTracker[YTer].filters){
                            if (body.items[0].snippet.title == filter){
                                properVidToPost = true;
                            }
                        }
                    }
    
                    if (properVidToPost){
                        if (videoId != streamersTracker[YTer].lastVideoID){
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
                                "fields": [
                                    {
                                        "name": "-",
                                        "value": body.items[0].snippet.description
                                    }
                                ]
                            };
    
                            postToDiscord(YTer, {embed}, true);
    
                            var messageToPost = (streamersTracker[YTer].atorNot) ? "<@173611085671170048> <@173610714433454084> https://www.youtube.com/watch?v=" + videoId : "https://www.youtube.com/watch?v=" + videoId; 
                            
                            postToDiscord(YTer, messageToPost, false);
                        }
                    }
                }
            });            

        }
    });

}
























































































/*
function getFormattedDate(date) {
    var year = date.getFullYear();
  
    var month = (1 + date.getMonth()).toString();
    month = month.length > 1 ? month : '0' + month;
  
    var day = date.getDate().toString();
    day = day.length > 1 ? day : '0' + day;
    
    return year + '/' + month + '/' + day;
}

function updateStreamerTracker(YTer, status, videoID, viewers){
 
    streamersTracker[YTer].URL = videoID;

    //post that person is live now
    if (status == "live"){
        if (streamersTracker[YTer].status == "offline"){

            if ((YTer != "T1")){
                console.log("In IF: ");
                var urlToCheck = "https://www.youtube.com/watch?v=" + streamersTracker[YTer].URL;
                var checkIfURLExistsInDatabase = dbQuery.checkURL(urlToCheck);

                checkIfURLExistsInDatabase.then(checkIfURLExistsInDatabase => {
                    if (!checkIfURLExistsInDatabase) {
                        var messageToPost = YTer + " is LIVE " + "https://www.youtube.com/watch?v=" + streamersTracker[YTer].URL;
        
                        var currentdate = new Date();
                        var datetime = getFormattedDate(currentdate);
                        var time = currentdate.getHours() + ":"
                                    + currentdate.getMinutes() + ":"
                                    + currentdate.getSeconds();
                        var url = "https://www.youtube.com/watch?v=" + streamersTracker[YTer].URL;
            
                        var sql_query = 'INSERT INTO cxnetwork (date, url, name, time) SELECT \'' + datetime +'\', \'' + url + '\', \'' + YTer + '\', \'' + time + '\' WHERE NOT EXISTS (SELECT 1 FROM cxnetwork WHERE url=\''+ url +'\');'
                        dbQuery.query(sql_query);
            
                        messageToPost = (streamersTracker[YTer].atorNot ? messageToPost + ' <@173611085671170048> <@173610714433454084> ' : messageToPost + ' ');
                        //console.log('[' + TWITCHer + '] Twitch API Says LIVE, attempting to post now ---- ' + new Date())
                        postToDiscord(YTer, messageToPost, false);
                    }
                });
            } else {
                console.log('in else');
                messageToPost = (streamersTracker[YTer].atorNot ? 'T1 IS LIVE  <@173611085671170048> <@173610714433454084> ' : 'T1 IS LIVE ');
                messageToPost = messageToPost + streamersTracker[YTer].URL;
                console.log('[' + YTer + '] is LIVE attempting to post now ---- ' + new Date())
                postToDiscord("Twitch", messageToPost, false);                
            }
            
        }
    }

    //post if more than 10k viewers
    if (viewers > 10000){
        if (!streamersTracker[YTer].MoreThan10kPostedDiscord){
            postToDiscord(YTer, YTer + " has more than 10k POGGERS", false);
        }
    }


    if (status == "offline"){
        if (streamersTracker[YTer].status == "live"){
            var messageToPost = YTer + " went offline";
            postToDiscord(YTer, messageToPost, false);
        }
    }

    streamersTracker[YTer].status = status;
    if (viewers != -1) streamersTracker[YTer].viewers = viewers;
}



/*




YOUTUBE FUNCTIONS HERE



New video on youtube notification

CX Clips channel ID: UCFthsIV3Bp11cRwb6R9AOOw
Ice's channel ID: UCv9Edl_WbtbPeURPtFDo-uA

Deeps: UC3Nlcpu-kbLmdhph_BN7OwQ








function getRequest(YTer){
    request.get('https://youtube.com/channel/' + streamersTracker[YTer].channelId + '/live', function(err, resp, body) {
        console.log('checked YT :' + YTer + ' at ' + new Date());
        if (err) {
            reject(err);
        } else {
            var isOnline;
            if (body.search("Live stream offline") == -1) {
                
                var splitted = body.split('\n');

                for (var x = 0; x < splitted.length; x++){
                    //console.log(x + splitted[x]);
            
                    if (splitted[x].indexOf('<meta itemprop="videoId" content=') > 0){
                        var firstQuotation = 34;
                        var secondQuotation = firstQuotation + splitted[x].trim().substring(34).indexOf('"');
                        var videoId = splitted[x].trim().substring(firstQuotation,secondQuotation);
            
                        if (videoId != streamersTracker[YTer].URL){
                            updateStreamerTracker(YTer, "live", videoId, -1);
                            
                            break;
                        }
                        ///postToDiscord(YTer, true, "main", "SDFSDFSDF");

                        }
            
                }
            } else {
                updateStreamerTracker(YTer, "offline", "", 0);
            }
        }
    });
}

*/




/*

function getAndPostAllMatches(){
    var leagueMatchesPromise = getLeagueMatches.getAllMatches();
    leagueMatchesPromise.then(returnArrayOfMatches => {
        if (returnArrayOfMatches.length != 0){
            for (var a = 0; (a < returnArrayOfMatches.length) && (a < 10); a++){

                if ((returnArrayOfMatches[a]['league'] == 'cblol 2019 1st split') || (returnArrayOfMatches[a]['league'] == '2019 LMS Spring Split') || (returnArrayOfMatches[a]['league'] == 'LJL 2019 Spring Split') || (returnArrayOfMatches[a]['league'] == '2019 LMS Spring Split')){ 
                    //a = a - 1;
                } else{
                    
                    var newDate = moment.unix( returnArrayOfMatches[a]['dayAndTimeEPOC']);
                    console.log(myDate);
                    
                    console.log(newDate);
                    var dateString = myDate.toLocaleString();

                    const embed = {
                        "description": "```\n"+ myDate  + "```",
                        "color": 9336950,
                        "timestamp": new Date(),
                        "footer": {
                        "icon_url": "https:" + returnArrayOfMatches[a]['leagueIcon'],//cdn.leagueofgraphs.com/img/lcs/leagues/64/2.png",
                        "text": "LCS"
                        },
                        "thumbnail": {
                        "url": "https:" + returnArrayOfMatches[a]['leagueIcon']
                        },
                        "image": {
                        "url": "https:" + returnArrayOfMatches[a]['team1Icon']
                        },
                        "author": {
                        "name": returnArrayOfMatches[a]['league'],
                        "icon_url": "https:" + returnArrayOfMatches[a]['leagueIcon']
                        },
                        "fields": [
                        {
                            "name": "_",
                            "value": returnArrayOfMatches[a]['team1'],
                            "inline": true
                        },
                        {
                            "name": "_",
                            "value": returnArrayOfMatches[a]['team2'],
                            "inline": true
                        }
                        ]
                    };
                    
                    postToDiscord('',{ embed: embed },true);
                }
        }
    }
    });
}

*/


/*
function getLiveViewers(YTer){

    if (streamersTracker[YTer].status == "live"){

        request.get("https://www.youtube.com/live_stats?v=" + streamersTracker[YTer].URL, function(err, resp, body) {
            if (err) {
            } else {
                body = parseInt(body)
                updateStreamerTracker(YTer, "live", streamersTracker[YTer].videoID, body);
            }
        })
    } else {
        updateStreamerTracker(YTer, "offline", "", 0);
    }
}

function initiateLiveCheckLoop(YTer, intervalLength) {

    //console.log(intervalLength)
    setInterval(function() {

        getRequest(YTer);
        getLiveViewers(YTer);

    }, intervalLength)
    
}

*/


/*




TWITCH 






function pollToCheckTwitcherIsLive(TWITCHer){   

    var options = {
        url: "https://api.twitch.tv/helix/streams?user_id=" +  streamersTracker[TWITCHer].channelId,
        headers: {
            "Client-ID": credentials.twitchauth
        }
    };

    request.get(options, function(err, resp, body) {
        console.log ("checked Twitch for: " + TWITCHer + " at " + new Date());
        data = JSON.parse(body);
        if((data['data'].length != 0) && (!streamersTracker[TWITCHer].postedToDiscord)){
            if (!streamersTracker[TWITCHer].postedToDiscord){
                // post on discord
                console.log(TWITCHer + " is LIVE " );
                updateStreamerTracker(TWITCHer, "live", "twitch.tv/loltyler1", 0);

                isT1CurrentlyLive = true;
                var hourZULU = data['data'][0]['started_at'].substring(11,13);
                var minutesZULU = parseInt(data['data'][0]['started_at'].substring(14,16));
                var hourEST = (parseInt(hourZULU) - 5 + 24) % 12;
                
                if (minutesZULU < 10)   minutesZULU = '0' + minutesZULU;

                //postToDiscord(discordChannelToPost, AtorNot, "T1 LIVE  https://www.twitch.tv/loltyler1 - stream started at " + hourEST + ':' + (minutesZULU), Twitcher)

                //t1LivePostedOnDiscord = true;
            }
        }else if (data['data'].length == 0){
            
            updateStreamerTracker(TWITCHer, "offline", "", 0);
            
            //console.log('[' + Twitcher + '] Twitch API Says OFFLINE ---- ' + new Date())
            //if (isT1CurrentlyLive)  postToDiscord(discordChannelToPost, true, "T1 stopped streaming", "T1")            
            //isT1CurrentlyLive = false;
            // console.log("not live");
            //t1LivePostedOnDiscord = false;
        }
    });
}


function initiateLiveCheckForTwitchLoop(Twitcher, intervalLength) {    

    setInterval(function() {
        
        // T1's ID is 51496027
        pollToCheckTwitcherIsLive(Twitcher);

    }, intervalLength)
}
*/
/*

function postToDiscord(YTer, msgToPost, ifEmbed){

    if ((YTer == 'Twitch') || (YTer == '')) {
        var channel = "173611297387184129";
        clientForDiscord.channels.get(channel).send(msgToPost);
        return;
    }
    var discordChannel = (streamersTracker[YTer].discordChannelToPost == "main") ? "173611297387184129" : "284157566693539851"

    //console.log(clientForDiscord.channel);

    if (!ifEmbed){
        // main discord channel is 173611297387184129
        // secondary discord channel is 284157566693539851
        console.log("[" + YTer + "] " + "Now posting  ---- " + msgToPost + "  " + new Date())
        clientForDiscord.channels.get(discordChannel).send(msgToPost)
    }else{
        clientForDiscord.channels.get(discordChannel).send(msgToPost)
    }

}

/*


/*



Twitter filter






function twitterFilter(discordChannelToPost){
    
    Twitterclient.stream('statuses/filter', {
        //solonoid12 is 1615735502
        follow: '1615735502,4833803780,736784706486734852,344538810,873949601522487297,290495509'
    }, function(stream) {

        stream.on('data', function(tweet) {
            //console.log(tweet)
            if ((tweet.user.screen_name == 'solonoid12') || (tweet.user.screen_name == 'loltyler1') || (tweet.user.screen_name == 'REALIcePoseidon') || (tweet.user.screen_name == 'TLDoublelift') || (tweet.user.screen_name == 'JacobK_Cx')) {
                //discordClient.channels.get("").send("<@173611085671170048> <@173610714433454084> https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str);
                console.log("stuff !!!" + tweet);
                postToDiscord("Twitter", "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str, "Twitter - " + tweet.user.screen_name, false)
            }
        });

        stream.on('error', function(error) {
            console.log(error);
        });
    });
}


*/

/*



/*



main function



*/



/*




reply based on intial commands






function postSummary(channel){

    const embed = new Discord.RichEmbed()
    .setTitle('Commands')
    .setColor("#67279C")

    for (data in streamersTracker) {
        if (streamersTracker[data].status == "live") {
            embed.addField(data + " - " + streamersTracker[data].emoji, "[link -- replace with YT title?](" + streamersTracker[data].URL + ")")
        }
    }

    channel.send(embed);

}
*/
/*
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

            neatclipClient.get("https://neatclip.com/api/v1/clips.php?streamer_url=https://www.youtube.com/channel/UCv9Edl_WbtbPeURPtFDo-uA&time=" + inHowLongDuration + "&sort=top", {api_key:  credentials.neatclip}, function(data, response) {

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
            neatclipClient.get("https://neatclip.com/api/v1/clips.php?time=" + inHowLongDuration + "&sort=top", {api_key: credentials.neatclip}, function(data, response) {

                var size = howManyClips;

                if (data.length < size) size = data.length;
                for (var x = 0; x < size; x++) {
                    var entry = [data[x]["slugID"], data[x]["viewsAll"]];
                    stringToSend = stringToSend + "https://neatclip.com/clip/" + data[x]["slugId"] + " views:" + data[x]["viewsAll"] + "\n";
                }
                message.channel.send(stringToSend);
            });

        } else if (message.content.startsWith('!update')) {

            message.channel.send(':thinking:')

            // second parameter is which discord channel, main channel or secondary channel
            // third is "at or not" ... at people or not

            getRequest("ICE");

            // EBZz channel ID is UCkR8ndH0NypMYtVYARnQ-_g
            getRequest("EBZ");

            // SAMs channel ID is UCdSr4xliU8yDyS1aGnCUMTA
            getRequest("SAM");

            // SJCs channel ID is UC4YYNTbzt3X1uxdTCJaYWdg
            getRequest("SJC");

            // CXNews channel ID is UCStEQ9BjMLjHTHLNA6cY9vg
            getRequest("CXNews");

            // MexicanAcnes channel ID is UC8EmlqXIlJJpF7dTOmSywBg
            getRequest("MexicanAcne");

            pollToCheckTwitcherIsLive("T1");

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
        } else if (message.content.startsWith('!league games')){
            getAndPostAllMatches();
        }

    });

}
*/
