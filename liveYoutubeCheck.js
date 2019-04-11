var request = require('request');
var discordPost = require('./discordPost');
var Discord = require('discord.js');
var dbQuery = require('./db');


var streamersTracker = {
    DEEP : {channelId: "UC3Nlcpu-kbLmdhph_BN7OwQ", emoji: ':baby:', discordChannelToPost: "main", atorNot: false, postedToDiscord: false, lastVideoID: '',
        status: 'offline', URL: "", viewers: 0, MoreThan10kPostedDiscord: false}, 
    ICE : {channelId: "UCv9Edl_WbtbPeURPtFDo-uA", emoji: ':baby:', discordChannelToPost: "main", atorNot: true, postedToDiscord: false, lastVideoID: '',
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
    Hyphonix : {channelId: "UCaFpm67qMk1W1wJkFhGXucA", emoji: '', discordChannelToPost: "main", atorNot: false, postedToDiscord : false, lastVideoID: '',
        status: 'offline', URL:"", viewers: 0, MoreThan10kPostedDiscord: false},
};


module.exports = {
    initiateLiveCheckLoop : function(clientForDiscord, YTer, intervalLength) {
        //console.log(intervalLength)
        setInterval(function() {
    
            getRequest(clientForDiscord, YTer);
    
        }, intervalLength)
        
    },

    queryOnceAndThenPostSummary : function(clientForDiscord){

        getRequest(clientForDiscord, "ICE");
        getRequest(clientForDiscord, "EBZ");
        getRequest(clientForDiscord, "MexicanAcne");
        getRequest(clientForDiscord, "CXNews");
    
        setTimeout(postSummary, 3000, clientForDiscord);

    }
}

function postSummary(clientForDiscord){
    const embed = new Discord.RichEmbed()
    .setTitle('Commands')
    .setColor("#67279C")

    for (data in streamersTracker) {
        if (streamersTracker[data].status == "live") {
            embed.addField(data + " - " + streamersTracker[data].emoji, "[link -- replace with YT title?](" + streamersTracker[data].URL + ")")
        }
    }

    //channel.send(embed);
    discordPost.postToDiscord(clientForDiscord, '', embed, true);
}

function getRequest(clientForDiscord, YTer){
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
                            updateStreamerTracker(clientForDiscord, YTer, "live", videoId);
                            
                            break;
                        }
                        ///postToDiscord(YTer, true, "main", "SDFSDFSDF");

                        }
            
                }
            } else {
                updateStreamerTracker(clientForDiscord, YTer, "offline", "");
            }
        }
    });
}


function updateStreamerTracker(clientForDiscord, YTer, status, videoID){
 
    streamersTracker[YTer].URL = videoID;

    //post that person is live now
    if (status == "live"){
        if (streamersTracker[YTer].status == "offline"){
                console.log("In IF: ");
                var urlToCheck = "https://www.youtube.com/watch?v=" + streamersTracker[YTer].URL;
                console.log("After urlAToCheck:");
                var checkIfURLExistsInDatabase = dbQuery.checkURL(urlToCheck);
                console.log("After dbQuery.checkURL");
                checkIfURLExistsInDatabase.then(checkIfURLExistsInDatabase => {
                    console.log("In checkURLExistsInDatabase");
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
                        discordPost.postToDiscord(clientForDiscord, YTer, messageToPost, false);
                    }
                });
            
        }
    }

    if (status == "offline"){
        if (streamersTracker[YTer].status == "live"){
            var messageToPost = YTer + " went offline";
            discordPost.postToDiscord(clientForDiscord, YTer, messageToPost, false);
        }
    }

    streamersTracker[YTer].status = status;
}


function getFormattedDate(date) {
    var year = date.getFullYear();
  
    var month = (1 + date.getMonth()).toString();
    month = month.length > 1 ? month : '0' + month;
  
    var day = date.getDate().toString();
    day = day.length > 1 ? day : '0' + day;
    
    return year + '/' + month + '/' + day;
}