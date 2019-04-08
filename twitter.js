
var discordPost = require('./discordPost');
var Twitter = require('twitter');
var credentials = require('./configuration.json');

var Twitterclient = new Twitter({
    consumer_key: credentials.twitterApiKey,
    consumer_secret: credentials.twitterApiSecretKey,
    access_token_key: credentials.twitterAccessToken,
    access_token_secret: credentials.twitterTokenSecret
});

module.exports = {
    
    twitterFilter : function(clientForDiscord){
    
        Twitterclient.stream('statuses/filter', {
            //solonoid12 is 1615735502
            follow: '1615735502,4833803780,736784706486734852,344538810,873949601522487297,290495509'
        }, function(stream) {
    
            stream.on('data', function(tweet) {
                //console.log(tweet)
                if ((tweet.user.screen_name == 'solonoid12') || (tweet.user.screen_name == 'loltyler1') || (tweet.user.screen_name == 'REALIcePoseidon') || (tweet.user.screen_name == 'TLDoublelift') || (tweet.user.screen_name == 'JacobK_Cx')) {
                    //discordClient.channels.get("").send("<@173611085671170048> <@173610714433454084> https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str);
                    console.log("attemping to post to twitter now");
                    discordPost.postToDiscord(clientForDiscord, '', "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str, "Twitter - " + tweet.user.screen_name, false)
                }
            });
    
            stream.on('error', function(error) {
                console.log(error);
            });
        });
    }
}