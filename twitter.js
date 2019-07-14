
var discordPost = require('./discordPost');
var Twitter = require('twitter');
var credentials = require('./configuration.json');

var Twitterclient = new Twitter({
    consumer_key: credentials.twitterApiKey,
    consumer_secret: credentials.twitterApiSecretKey,
    access_token_key: credentials.twitterAccessToken,
    access_token_secret: credentials.twitterTokenSecret
});

twitterAccounts = {
    deep : {
        tweeter: 'solonoid12',
        twitterId: '1615735502',
        postOnlyIfContains: []
    },
    t1 : {
        tweeter: 'loltyler1',
        twitterId: '4833803780',
        postOnlyIfContains: []
    },
    ice : {
        tweeter: 'REALIcePoseidon',
        twitterId: '736784706486734852',
        postOnlyIfContains: []
    },
    lift : {
        tweeter: 'TLDoublelift',
        twitterId: '344538810',
        postOnlyIfContains: []
    },
    jacob : {
        tweeter: 'jacobK_Cx',
        twitterId: '873949601522487297',
        postOnlyIfContains: []
    },
    reapered : {
        tweeter: 'Reapered',
        twitterId: '290495509',
        postOnlyIfContains: []
    },
    lolesports : {
        tweeter: 'lolesports',
        twitterId: '614754689',
        postOnlyIfContains: ['#lcs', 'na', 'lcs']
    },
    c9 : {
        tweeter: 'Cloud9',
        twitterId: '1452520626',
        postOnlyIfContains: ['c9lol, lol, lcs']
    },
    lcs : {
        tweeter: 'LCS',
        twitterId: '1099419521654222848',
        postOnlyIfContains: []
    }
} 

var twitterClientSubscribeToListDelimittedComma = '';

for (tweeter in twitterAccounts){
    twitterClientSubscribeToListDelimittedComma = twitterClientSubscribeToListDelimittedComma + twitterAccounts[tweeter].twitterId;
    console.log(tweeter);
    console.log(twitterAccounts.length);
    if (tweeter != twitterAccounts.length - 1) twitterClientSubscribeToListDelimittedComma = twitterClientSubscribeToListDelimittedComma + ',';
}

console.log(twitterClientSubscribeToListDelimittedComma);

module.exports = {
    
    twitterFilter : function(clientForDiscord){
    
        Twitterclient.stream('statuses/filter', {
            //solonoid12 is 1615735502
            follow: twitterClientSubscribeToListDelimittedComma
        }, function(stream) {
    
            stream.on('data', function(tweet) {
                //console.log(tweet)

                for (tweeter in twitterAccounts){
                    if (tweet.user.screen_name == twitterAccounts[tweeter].tweeter){
                        var postThisQuestion = false;

                        if (twitterAccounts[tweeter].postOnlyIfContains.length == 0){
                            postThisQuestion = true;
                        }else{

                            for (eachFilter in twitterAccounts[tweeter].postOnlyIfContains){

                                if ((tweet.text).toLowerCase().includes(twitterAccounts[tweeter].postOnlyIfContains.eachFilter)){
                                    postThisQuestion = true;
                                }
                            }

                            if (postThisQuestion){
                                console.log("Twitter - Post - For: " + tweet.user.screen_name);
                                discordPost.postToDiscord(clientForDiscord, '', "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str, "Twitter - " + tweet.user.screen_name, false, "main-channel");
                            }
                        }
                    }
                }
                /*
                if ((tweet.user.screen_name == 'solonoid12') || (tweet.user.screen_name == 'loltyler1') || (tweet.user.screen_name == 'REALIcePoseidon') || (tweet.user.screen_name == 'TLDoublelift') || (tweet.user.screen_name == 'JacobK_Cx')) {
                    //discordClient.channels.get("").send("<@173611085671170048> <@173610714433454084> https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str);
                    console.log("attemping to post to twitter now");
                    discordPost.postToDiscord(clientForDiscord, '', "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str, "Twitter - " + tweet.user.screen_name, false)
                }
                */
            });
    
            stream.on('error', function(error) {
                console.log(error);
            });
        });
    }
}
