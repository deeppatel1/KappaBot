var credentials = require('./configuration.json');
var Discord = require("discord.js");
var dbQuery = require('./db.js');
//var get_league_matches = require('./get_league_matches.js');
var liveYouTubeCheck = require('./liveYoutubeCheck');
var twitchFunctions = require('./twitchLiveAndPost');
var animeFunctions = require('./animeNotifications.js');

module.exports = {

    respondToMessagesLive: function (clientForDiscord) {

        clientForDiscord.on("message", function (message) {

            if (message.content.startsWith("--h") || message.content.startsWith("?help")) {
                const embed = new Discord.RichEmbed()
                    .setTitle('Commands')
                    .setColor("#67279C")
                    .addField("?ice last #", "Get the last {#} of vod urls")
                    //.addField("!clips hour/day/week/month/year/alltime #", "Get most popular clips for last hour/day/week/month/year/alltime")
                    //.addField("!ice hour/day/week/month/year/alltime #", "Get most popular clips for ice for the last hour/day/week/month/year/alltime")
                    .addField("?vod {name} {number}", "Gets the last {number} of vods for a particular streamer.\n{name}: EBZ, SAM, SJC, CXNews, MexicanAcne")
                    .addField("!league games", "post upcoming league games")
                    .addField("!(t1/lolesports) (day/week/month/all)", "query twitch vods for these 2 channels. tops clips per day/week/month/all")
                    .addField("_", "_")
                    .addField("!version", "checks current version")

                message.channel.send(embed)
            } else if (message.content.startsWith('!update')) {

                message.channel.send(':thinking:')

                liveYouTubeCheck.queryOnceAndThenPostSummary(clientForDiscord);

            } else if (message.content.startsWith('?vod ')) {
                var numberofVods = message.content.split(" ");
                const num = numberofVods[2];
                const name = numberofVods[1];

                if (numberofVods.length == 3) {
                    dbQuery.queryOthers(num, name, message);
                }
            } else if (message.content.startsWith('?ice last')) {
                var numberofVods = message.content.split(" ");
                const num = numberofVods[2];
                if (numberofVods.length == 3) {
                    console.log("==QUERYING VODS=== querying " + num + " number of vods")
                    dbQuery.queryVod(num, message);
                }
            } /*else if (message.content.startsWith('!league games')) {
                get_league_matches.getAndPostAllMatches(clientForDiscord);
            }*/ else if (message.content.startsWith('!logs')) {
                message.channel.send("kappabot logs", {
                    files: ["/home/pi/.forever/kappabot.log"]
                });
            } else if (message.content.startsWith('!version')) {
                message.channel.send("version ios 19.0");
            } else if (message.content.startsWith('!clips')) {
                var extraInputs = message.content.split(" ");
                var streamer = extraInputs[1];
                streamer = streamer.toLowerCase();
                var period = extraInputs[2];
                console.log('streamer = ' + streamer);
                console.log('period: ' + period);
                twitchFunctions.getTopClips(clientForDiscord, streamer, period, 5);
            }

            /* anime stuff is here 
            else if (message.content.startsWith("!anime")) {
                animeFunctions.extractAnimeAndAnimeID();
            } *//* else if (message.content.startsWith("!add anime")) {
                var animeAndID = message.content.split(" ");
                console.log(animeAndID)
                animeFunctions.addAnime(animeAndID[2], animeAndID[3], animeAndID[4]);
            } */ else if (message.content.startsWith("!view anime")) {
                console.log('in anime functions view')
                animeFunctions.viewAnime();
            } /* else if (message.content.startsWith("!remove anime")){
                var animeToRemove = message.content.split(" ");
                console.log('in remove functions anime')
                animeFunctions.removeAnime(animeToRemove[2]);
            } */


        });

    },

};