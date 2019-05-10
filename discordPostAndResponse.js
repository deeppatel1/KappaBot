var credentials = require('./configuration.json');
var Discord = require("discord.js");
var dbQuery = require('./db.js');
var getLeagueMatches = require('./getLeagueMatches.js');
var liveYouTubeCheck = require('./liveYoutubeCheck');

module.exports = {
    
    respondToMessagesLive : function(clientForDiscord){

        clientForDiscord.on("message", function(message) {
    
            if (message.content.startsWith("--h") || message.content.startsWith("?help")) {
                const embed = new Discord.RichEmbed()
                    .setTitle('Commands')
                    .setColor("#67279C")
                    .addField("?ice last #", "Get the last {#} of vod urls")
                    //.addField("!clips hour/day/week/month/year/alltime #", "Get most popular clips for last hour/day/week/month/year/alltime")
                    //.addField("!ice hour/day/week/month/year/alltime #", "Get most popular clips for ice for the last hour/day/week/month/year/alltime")
                    .addField("?vod {name} {number}", "Gets the last {number} of vods for a particular streamer.\n{name}: EBZ, SAM, SJC, CXNews, MexicanAcne")
                    .addField("!league matches post upcoming league games")
    
                message.channel.send(embed)
            } /* else if (message.content.startsWith("!ice")) {
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
    
            } */else if (message.content.startsWith('!update')) {
    
                message.channel.send(':thinking:')

                liveYouTubeCheck.queryOnceAndThenPostSummary(clientForDiscord);
    
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
                getLeagueMatches.getAndPostAllMatches(clientForDiscord);
            } else if (message.content.startsWith('!logs')) {
                message.channel.send("kappabot logs", { files: ["/home/pi/.forever/kappabot.log"] });
            } else if (message.content.startsWith('!version')) {
                message.channel.send("version ios 15.2");
            }
    
        });
    
    },

};