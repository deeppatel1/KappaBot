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

// discordChannelToPost, AtOrNot, online, postedToDiscord, 

var streamersTracker = {
    DEEP : {channelId: "UC3Nlcpu-kbLmdhph_BN7OwQ", emoji: ':baby:', discordChannelToPost: "main", atorNot: false, postedToDiscord: false,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    ICE : {channelId: "UCv9Edl_WbtbPeURPtFDo-uA", emoji: ':baby:', discordChannelToPost: "main", atorNot: true, postedToDiscord: false,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    EBZ: {channelId: "UCkR8ndH0NypMYtVYARnQ-_g", emoji: ':older_man::skin-tone-5: ', discordChannelToPost: "secondary", atorNot: false, postedToDiscord: false,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    SAM : {channelId: "UCdSr4xliU8yDyS1aGnCUMTA", emoji: ':hot_pepper: ', discordChannelToPost: "secondary", atorNot: false, postedToDiscord:false ,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    SJC : {channelId: "UC4YYNTbzt3X1uxdTCJaYWdg", emoji: ':head_bandage:', discordChannelToPost: "secondary", atorNot: false, postedToDiscord:false ,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    CXNews : {channelId: "UCStEQ9BjMLjHTHLNA6cY9vg", emoji: ':newspaper:', discordChannelToPost: "main", atorNot: true, postedToDiscord:false ,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    MexicanAcne : {channelId: "UC8EmlqXIlJJpF7dTOmSywBg", emoji: ':flushed:', discordChannelToPost: "secondary", atorNot: true, postedToDiscord:false ,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    T1 : {channelId: "51496027", emoji: '', discordChannelToPost: "main", atorNot: true, postedToDiscord: false, postedToDiscord : false,
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false},
    Hyphonix : {channelId: "UCaFpm67qMk1W1wJkFhGXucA", emoji: '', discordChannelToPost: "main", atorNot: true, postedToDiscord : false,
        status: 'offline', URL:"", viewers: 0, MoreThan10kPostedDiscord: false}
};

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
            var messageToPost = YTer + " is LIVE " + "https://www.youtube.com/watch?v=" + streamersTracker[YTer].URL;

            messageToPost = (streamersTracker[YTer].atorNot ? messageToPost + ' <@173611085671170048> <@173610714433454084> ' : messageToPost + ' ');
            //console.log('[' + TWITCHer + '] Twitch API Says LIVE, attempting to post now ---- ' + new Date())
            postToDiscord(YTer, messageToPost);
        }
    }

    //post if more than 10k viewers
    if (viewers > 10000){
        if (!streamersTracker[YTer].MoreThan10kPostedDiscord){
            postToDiscord(YTer, YTer + " has more than 10k POGGERS");
        }
    }


    if (status == "offline"){
        if (streamersTracker[YTer].status == "live"){
            var messageToPost = YTer + " went offline";
            postToDiscord(YTer, messageToPost);
        }
    }

    streamersTracker[YTer].status = status;
    if (viewers != -1) streamersTracker[YTer].viewers = viewers;
}

function getRequest(YTer){
    request.get('https://youtube.com/channel/' + streamersTracker[YTer].channelId + '/live', function(err, resp, body) {
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
            
                        updateStreamerTracker(YTer, "live", videoId, -1);
                        
                        break;
                        ///postToDiscord(YTer, true, "main", "SDFSDFSDF");

                        }
            
                }
            } else {
                updateStreamerTracker(YTer, "offline", "", 0);
            }
        }
    });
}

function postToDiscord(YTer, msgToPost){
    // main discord channel is 173611297387184129
    // secondary discord channel is 284157566693539851

    var discordChannel = (streamersTracker[YTer].discordChannelToPost == "main") ? "173611297387184129" : "284157566693539851"

    console.log("[" + YTer + "] " + "Now posting to discord he/she is live ---- " + new Date())
    
    clientForDiscord.channels.get(discordChannel).send(msgToPost)

}

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

function pollToCheckTwitcherIsLive(TWITCHer){   

    var options = {
        url: "https://api.twitch.tv/helix/streams?user_id=" +  streamersTracker[TWITCHer].channelId,
        headers: {
            "Client-ID": credentials.twitchauth
        }
    };

    request.get(options, function(err, resp, body) {
        data = JSON.parse(body);
        if((data['data'].length != 0) && (!streamersTracker[TWITCHer].postedToDiscord)){
            if (!streamersTracker[TWITCHer].postedToDiscord){
                // post on discord
                
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


/*

Twitter filter

*/


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




/*

interval functions that main function will run

*/

function initiateLiveCheckLoop(YTer, intervalLength) {

    //console.log(intervalLength)
    setInterval(function() {

        getRequest(YTer);
        getLiveViewers(YTer);

    }, intervalLength)
    
}

function initiateLiveCheckForTwitchLoop(Twitcher, intervalLength) {    

    setInterval(function() {
        
        // T1's ID is 51496027
        pollToCheckTwitcherIsLive(Twitcher);

    }, intervalLength)
}

/*

main function

*/



twitterFilter("main");
clientForDiscord.on('ready', () => {
     
    initiateLiveCheckLoop("ICE", 20000);
    //initiateLiveCheckLoop("DEEP",500);
    initiateLiveCheckForTwitchLoop("T1", 30000);

});


clientForDiscord.login(credentials.discordclientlogin);

/*
var request = require('request');
var credentials = require('./configuration.json');
var rest = require('node-rest-client').Client;
var Twitter = require('twitter');
const Discord = require("discord.js");
const clientForDiscord = new Discord.Client();


var neatclipClient = new rest();
var gKey = credentials.gKey;
var Twitterclient = new Twitter({
    consumer_key: credentials.twitterApiKey,
    consumer_secret: credentials.twitterApiSecretKey,
    access_token_key: credentials.twitterAccessToken,
    access_token_secret: credentials.twitterTokenSecret
});

var options = {
    url: "https://www.youtube.com/channel/UC4YYNTbzt3X1uxdTCJaYWdg/live",
    headers: {
        //"Client-ID": credentials.twitchauth
    }
  };

request.get(options, function(err, resp, body) {
    //console.log(resp);
    //console.log(body.split('\r\n'));

    //console.log(body);

    var splitted = body.split('\n');

    for (var x = 0; x < splitted.length; x++){
        //console.log(x + splitted[x]);

        if (splitted[x].indexOf('<meta itemprop="videoId" content=') > 0){
            var firstQuotation = 34;
            var secondQuotation = firstQuotation + splitted[x].trim().substring(34).indexOf('"');
            var videoId = splitted[x].trim().substring(firstQuotation,secondQuotation);


            


            break;
        }

    }





    console.log(body.split('\n').length);
    //body = JSON.parse(body);

    //console.log(body['data']);
}); 
*/