var request = require('request');

var streamerInformation = require('./index.js');

module.exports = {
    getRequest : function(YTer){
        request.get('https://youtube.com/channel/' + streamerInformation['streamersTracker'][YTer].channelId + '/live', function(err, resp, body) {
        console.log('YouTube Checking Live For - ' + YTer + ' at ' + new Date());
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
                
                            if (videoId != streamerInformation['streamersTracker'][YTer].URL){
                                streamerInformation['updateStreamerTracker'](updateStreamerTracker(YTer, "live", videoId, -1));
                                
                                break;
                            }
                            ///postToDiscord(YTer, true, "main", "SDFSDFSDF");

                            }
                    }
                } else {
                    streamerInformation['updateStreamerTracker'](updateStreamerTracker(YTer, "offline", "", 0));
                }
            }
        });
    },

    getLiveViewers : function(YTer){

        if (streamerInformation['streamersTracker'][YTer].status == "live"){

            request.get("https://www.youtube.com/live_stats?v=" + streamerInformation['streamersTracker'][YTer].URL, function(err, resp, body) {
                if (err) {
                } else {
                    body = parseInt(body)
                    streamerInformation['updateStreamerTracker'](updateStreamerTracker(YTer, "live", streamerInformation['streamersTracker'][YTer].videoID, body));
                }
            })
        } else {
            streamerInformation['updateStreamerTracker'](updateStreamerTracker(YTer, "offline", "", 0));
        }
    },

    queryLastYoutubeSingle : function(YTer){

        request.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + streamerInformation['streamersTracker'][YTer].channelId + "&maxResults=1&order=date&type=video&key=" + gKey, function(err, resp, body) {
    
            console.log('YouTube Querying for Vod: - ' + YTer + ' - ' + new Date());

            if (err) {
                reject(err);
            } else {
                body = JSON.parse(body);
                var videoId = body.items[0].id.videoId;
                var url = "https://www.youtube.com/watch?v=" + videoId;

                var checkIfURLExistsInDatabase = dbQuery.checkURL(url);

                checkIfURLExistsInDatabase.then(checkIfURLExistsInDatabase => {
                    if (!checkIfURLExistsInDatabase) {   //If the video is not in the DB, do all this
                        // Add video to database
                        var currentdate = new Date();
                        var datetime = getFormattedDate(currentdate);
                        var time = currentdate.getHours() + ":"
                                    + currentdate.getMinutes() + ":"
                                    + currentdate.getSeconds();
                        var sql_query = 'INSERT INTO cxnetwork (date, url, name, time) SELECT \'' + datetime +'\', \'' + url + '\', \'' + "YouTube" + '\', \'' + time + '\' WHERE NOT EXISTS (SELECT 1 FROM cxnetwork WHERE url=\''+ url +'\');'
                        dbQuery.query(sql_query);
        
        
                        var properVidToPost = false;
        
                        if (streamerInformation['streamerInformation'][YTer].filters.length == 0) {
                            properVidToPost = true;
                        } else {
                            
                            for (filter in streamersTracker['streamersTracker'][YTer].filters){
                                if (body.items[0].snippet.title == filter){
                                    properVidToPost = true;
                                }
                            }
                        }
        
                        if (properVidToPost){
                            if (videoId != streamerInformation['streamersTracker'][YTer].lastVideoID){
                                streamerInformation['streamersTracker'][YTer].lastVideoID = videoId;
        
                                const embed = {
                                    "thumbnail": {
                                        "url": body.items[0].snippet.thumbnails.medium.url
                                    },
                                    "color": 4922096,
                                    "timestamp": body.items[0].snippet.publishedAt,
                                    "author": {
                                    "name": YTer + " - " + body.items[0].snippet.title,
                                    },
                                    "fields": [
                                        {
                                            "name": "-",
                                            "value": body.items[0].snippet.description
                                        }
                                    ]
                                };
        
                                postToDiscord(YTer, {embed}, true, "main-channel");
        
                                var messageToPost = (streamerInformation['streamersTracker'][YTer].atorNot) ? "<@173611085671170048> <@173610714433454084> https://www.youtube.com/watch?v=" + videoId : "https://www.youtube.com/watch?v=" + videoId; 
                                
                                postToDiscord(YTer, messageToPost, false, "main-channel");
                            }
                        }
                    }
                });            

            }
        });

    }
}
