var credentials = require('./configuration.json');

module.exports = {

    postToDiscord : function(clientForDiscord, YTer, msgToPost, ifEmbed, channel){

        var postingChannel = credentials.channel;

        console.log("---YTeR:" + YTer + " msgToPost: " + msgToPost + " channel: " + channel + " posting channel: " + postingChannel);
        if ((YTer == 'Twitch') || (YTer == '')) {
            var channel = "173611297387184129";
            clientForDiscord.channels.get(channel).send(msgToPost);
            return;
        }
        //var discordChannel = (streamersTracker[YTer].discordChannelToPost == "main") ? "173611297387184129" : "284157566693539851"

        //console.log(clientForDiscord.channel);

        if (!ifEmbed){
            // main discord channel is          173611297387184129
            // secondary discord channel is     284157566693539851
            console.log("[" + YTer + "] " + "Now posting  ---- " + msgToPost + "  " + new Date())
            clientForDiscord.channels.get(postingChannel).send(msgToPost)
        }else{
            clientForDiscord.channels.get(postingChannel).send(msgToPost)
        }

    }

}