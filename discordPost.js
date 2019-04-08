
module.exports = {

    postToDiscord : function(clientForDiscord, YTer, msgToPost, ifEmbed){

        if ((YTer == 'Twitch') || (YTer == '')) {
            var channel = "173611297387184129";
            clientForDiscord.channels.get(channel).send(msgToPost);
            return;
        }
        //var discordChannel = (streamersTracker[YTer].discordChannelToPost == "main") ? "173611297387184129" : "284157566693539851"

        //console.log(clientForDiscord.channel);

        if (!ifEmbed){
            // main discord channel is 173611297387184129
            // secondary discord channel is 284157566693539851
            console.log("[" + YTer + "] " + "Now posting  ---- " + msgToPost + "  " + new Date())
            clientForDiscord.channels.get("173611297387184129").send(msgToPost)
        }else{
            clientForDiscord.channels.get("173611297387184129").send(msgToPost)
        }

    }

}