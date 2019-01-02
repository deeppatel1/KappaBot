var request = require('request');
var credentials = require('./configuration.json');
var rest = require('node-rest-client').Client;
var Twitter = require('twitter');
const Discord = require("discord.js");
const clientForDiscord = new Discord.Client();


var neatclipClient = new rest();
var gKey = credentials.gKey;
var Twitterclient = new Twitter({
    consumer_key: credentials.twitterApiKey,
    consumer_secret: credentials.twitterApiSecretKey,
    access_token_key: credentials.twitterAccessToken,
    access_token_secret: credentials.twitterTokenSecret
});

var options = {
    url: "https://api.twitch.tv/helix/streams?user_id=51496027",
    headers: {
        "Client-ID": credentials.twitchauth
    }
  };

request.get(options, function(err, resp, body) {
    //console.log(resp);
    console.log(body);
    body = JSON.parse(body);

    console.log(body['data']);
}); 