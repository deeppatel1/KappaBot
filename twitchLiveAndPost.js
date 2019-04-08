var credentials = require('./configuration.json');
var request = require('request');
var discordPost = require('./discordPost');

twitchStreamerTracker = {
    T1 : {channelId: "51496027", 
        emoji: '', 
        discordChannelToPost: "main", 
        atorNot: true, 
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline', 
        URL: "https://www.twitch.tv/loltyler1",
        MoreThan10kPostedDiscord: false
    },
    Trick : {channelId: "28036688", 
        emoji: '', 
        discordChannelToPost: "main", 
        atorNot: true, 
        postedToDiscord: false,
        lastVideoID: '',
        status: 'offline', 
        URL: "https://www.twitch.tv/trick2g",
        MoreThan10kPostedDiscord: false
    }

}

module.exports = {

    initiateLiveCheckForTwitchLoop : function(clientfordiscord, Twitcher, intervalLength) {    
        setInterval(function() {
            
            // T1's ID is 51496027
            pollToCheckTwitcherIsLive(Twitcher, clientfordiscord);
    
        }, intervalLength)
    }
};




function pollToCheckTwitcherIsLive(TWITCHer, clientfordiscord){

    var options = {
        url: "https://api.twitch.tv/helix/streams?user_id=" +  twitchStreamerTracker[TWITCHer].channelId,
        headers: {
            "Client-ID": credentials.twitchauth
        }
    };

    request.get(options, function(err, resp, body) {
        console.log ("checked Twitch for: " + TWITCHer + " at " + new Date());
        data = JSON.parse(body);
        console.log(data);
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
    });        
}

function updateStreamerTracker(clientfordiscord, twitchStreamer, status){
 
    if (status == "live"){
        if (twitchStreamerTracker[twitchStreamer].status == "offline"){
            messageToPost = (twitchStreamerTracker[twitchStreamer].atorNot ? 'T1 IS LIVE  <@173611085671170048> <@173610714433454084> ' : 'T1 IS LIVE ');
            messageToPost = messageToPost + twitchStreamerTracker[twitchStreamer].URL;
            console.log('[' + twitchStreamer + '] is LIVE attempting to post now ---- ' + new Date())
            discordPost.postToDiscord(clientfordiscord, '', messageToPost, false);                
        }
            
    }
    
    if (status == "offline"){
        if (twitchStreamerTracker[twitchStreamer].status == "live"){
            var messageToPost = twitchStreamer + " went offline";
            discordPost.postToDiscord(clientfordiscord, '', messageToPost, false);
        }
    }

    twitchStreamerTracker[twitchStreamer].status = status;
}