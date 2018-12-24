require('dotenv').config();
var { Client, RichEmbed } = require("discord.js");
var rest = require('node-rest-client').Client;
const readLastLines = require('read-last-lines');
var credentials = require('./configuration.json');
var fs = require('fs');
var Twitter = require('twitter');
var dbQuery = require('./db.js');

var client = new Client();
var nodeRestClientForUse = new rest();
var neatclipClient = new rest();
var restClient = new rest();
var restClient2 = new rest();

var Twitterclient = new Twitter({
    consumer_key: credentials.twitterApiKey,
    consumer_secret: credentials.twitterApiSecretKey,
    access_token_key: credentials.twitterAccessToken,
    access_token_secret: credentials.twitterTokenSecret
});

var gKey = credentials.gKey;

var args = {
    headers: { "Client-ID": credentials.twitchauth } // request headers
};

var t1PostedOnDiscord = false;
var isT1Live = false;


function checkifYTisLive(YTer, YTChannelName, discordChannelToPost, millisecondsInterval, client){

    var online = false;
    var postedToDiscord = false;

    setInterval(function(){
        console.log("[" + YTer + " FUNC] checking youtube for " + YTer + " / live  --- " + new Date());
        restClient.get("https://www.youtube.com/channel/"+ YTChannelName+ "/live",function (data,response){
            data = String(data);
        //    console.log("HES LIVE CHECK WHAT HAPPEN NOW WITH OFFICIAL API");
        //    console.log(data);
        //if JSON response doesn't have "Live stream offline", than this user is online"
            if (data.search("Live stream offline") == -1){
                console.log("["+ YTer +"] " + " is live per GET request --- " + new Date());
                //setting online true will trigger other function
                online = true;

        //this dude is offline
            }else{
                console.log("["+ YTer +"] " + " is offline per GET request --- " + new Date());
                online = false;
                //postedToDiscord false means don't need to post a message to discord since offline, and won't trigger other function
                postedToDiscord = false;
            }
        });

        if ((online) && (!postedToDiscord)){
            console.log("["+ YTer +"] " + " starting main YT request" + new Date());
            restClient2.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+YTChannelName+"&type=video&eventType=live&key=" + gKey, function(data2,response2){
                data2STRING = String(data2);
                if (data2.items.length > 0){  //confirmed live, now post it on discord!
                    console.log("["+ YTer +"] " + "is live posting on discord now  --- " + new Date())
                    var currentdate = new Date(); 
                    var datetime = (currentdate.getMonth()+1)+ "/"
                                    +  currentdate.getDate()  + "/" 
                                    + currentdate.getFullYear() + " @ "  
                                    + currentdate.getHours() + ":"  
                                    + currentdate.getMinutes() + ":" 
                                    + currentdate.getSeconds();
                    client.channels.get(discordChannelToPost).send(YTer + " LIVE https://www.youtube.com/watch?v=" + data2.items[0].id.videoId);
                    
                    const { Client } = require('pg')
                    const pgClient = new Client()
                    // const date = new Date();
                    const url = "https://www.youtube.com/watch?v=" + data2.items[0].id.videoId;

                    var sql_query = 'INSERT INTO cxnetwork (date, url, name) SELECT \'' + datetime +'\', \'' + url + '\', \'' + YTer + '\' WHERE NOT EXISTS (SELECT 1 FROM cxnetwork WHERE url=\''+ url +'\');'

                    dbQuery.query(sql_query);

                    // fs.appendFile("icevods.txt","https://www.youtube.com/watch?v=" + data2.items[0].id.videoId + "  " + datetime + '\n', (err) =>{
                    //     if (err) throw err;
                    // });
                    postedToDiscord = true;
                }else{  //confirmed not live!
                    console.log("["+ YTer +"] Main API says offline --- " + new Date());
                    //console.log("checked main api, offline");
                }

            });
        }

    }, millisecondsInterval)
}

client.on('ready', () => {

    // main discord channel is 173611297387184129
    // secondary discord channel is 284157566693539851

    //checkifYTFunction paramters are 1) name of YTer, 2) YT Channel ID, 3) Discord Channel to post to, 4)Millisecond to refresh, 5) discord client passed in

    // ICE's channel ID is UCv9Edl_WbtbPeURPtFDo-uA
    checkifYTisLive("ICE", "UCv9Edl_WbtbPeURPtFDo-uA","173611297387184129", 300000, client);

    // EBZz channel ID is UCkR8ndH0NypMYtVYARnQ-_g
    checkifYTisLive("EBZ", "UCkR8ndH0NypMYtVYARnQ-_g","284157566693539851", 300000, client);

    // SAMs channel ID is UCdSr4xliU8yDyS1aGnCUMTA
    checkifYTisLive("SAM", "UCdSr4xliU8yDyS1aGnCUMTA","284157566693539851", 300000, client);

    // SJCs channel ID is UC4YYNTbzt3X1uxdTCJaYWdg
    checkifYTisLive("SJC", "UC4YYNTbzt3X1uxdTCJaYWdg","284157566693539851", 300000, client);

    // CXNews channel ID is UCStEQ9BjMLjHTHLNA6cY9vg
    checkifYTisLive("CXNews", "UCStEQ9BjMLjHTHLNA6cY9vg","173611297387184129", 300000, client);

    // MexicanAcnes channel ID is UC8EmlqXIlJJpF7dTOmSywBg
    checkifYTisLive("MexicanAcne", "UC8EmlqXIlJJpF7dTOmSywBg","284157566693539851", 300000, client);


    Twitterclient.stream('statuses/filter', {follow: '4833803780,736784706486734852,344538810,873949601522487297'},  function(stream) {
        stream.on('data', function(tweet) {
            if ((tweet.user.screen_name == 'loltyler1') || (tweet.user.screen_name == 'REALIcePoseidon') || (tweet.user.screen_name == 'TLDoublelift') || (tweet.user.screen_name == 'JacobK_Cx')){
                client.channels.get("173611297387184129").send("<@173611085671170048> <@173610714433454084> https://twitter.com/" + tweet.user.screen_name +"/status/" + tweet.id_str);
            }
        });
      
        stream.on('error', function(error) {
          console.log(error);
        });
      });
    
});


client.on("message", function(message){

    if (message.content.startsWith("--h") || message.content.startsWith("?help")) {
        const embed = new RichEmbed()
            .setTitle('Commands')
            .setColor("#67279C")
            .addField("?ice last #", "Get the last {#} of vod urls")
            .addField("!clips hour/day/week/month/year/alltime #", "Get most popular clips for last hour/day/week/month/year/alltime")
            .addField("!ice hour/day/week/month/year/alltime #", "Get most popular clips for ice for the last hour/day/week/month/year/alltime")
            .addField("?vod {name} {number}", "Gets the last {number} of vods for a particular streamer.\n{name}: EBZ, SAM, SJC, CXNews, MexicanAcne")

        message.channel.send(embed)
    } else if (message.content.startsWith("!ice")){
        var args = message.content.split(/ +/g);
        var inHowLongDuration = args[1]; //can be hour for last hour, day..., week..., month..., year..., alltime
        var howManyClips = args[2]; //how many clips to show
        var stringToSend = "";
        neatclipClient.get("https://neatclip.com/api/v1/clips.php?streamer_url=https://www.youtube.com/channel/UCv9Edl_WbtbPeURPtFDo-uA&time=" + inHowLongDuration + "&sort=top", arguments, function (data, response){
        
            var size = howManyClips;
            
            if (data.length < size) size = data.length;
            for (var x = 0; x < size; x++){
                var entry = [data[x]["slugID"], data[x]["viewsAll"]];
                stringToSend = stringToSend + "https://neatclip.com/clip/" + data[x]["slugId"] + " views:" + data[x]["viewsAll"] + "\n";
            }

            message.channel.send(stringToSend);

        });
    
    } else if (message.content.startsWith('!clips')){
        var args = message.content.split(/ +/g);
        var inHowLongDuration = args[1]; //can be hour for last hour, day..., week..., month..., year..., alltime
        var howManyClips = args[2]; //how many clips to show
        var stringToSend = "";
        neatclipClient.get("https://neatclip.com/api/v1/clips.php?time=" + inHowLongDuration + "&sort=top", arguments, function (data, response){
        
            var size = howManyClips;
            
            if (data.length < size) size = data.length;
            for (var x = 0; x < size; x++){
                var entry = [data[x]["slugID"], data[x]["viewsAll"]];
                stringToSend = stringToSend + "https://neatclip.com/clip/" + data[x]["slugId"] + " views:" + data[x]["viewsAll"] + "\n";
            }

            message.channel.send(stringToSend);

        });

    } else if (message.content.startsWith('?ice last')){
        console.log("TEST")
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

    }

});

client.login(credentials.discordclientlogin);
