const lineReader = require('line-reader');
const fetch = require("node-fetch");
const fs = require('fs')

var discordPost = require('./discordPost');
var schedule = require('node-schedule');

var clientForDiscord;


module.exports = {

	initiateAnimes: function (clientForDiscordPassedIn) {
		clientForDiscord = clientForDiscordPassedIn;
		// Now get all the animes that are saved, and instantiate the automatic reminder
		this.extractAnimeAndAnimeID();
	},

	extractAnimeAndAnimeID: function () {
		extractAnimeAndAnimeIdPromise.then(function (value) {
			for (var eachAnime in value) {
				getNextAirDate(value[eachAnime][0], value[eachAnime][1])
			}
		});
	},

	addAnime: function (anime, Id) {
		data = '\n' + anime + ',' + Id
		console.log(data)
		fs.appendFile('animeList.txt', data, (err) => {
			// In case of a error throw err.
			if (err) throw err;
		})
	},

	viewAnime: function () {
		lineReader.eachLine('animeList.txt', function (line) {
			console.log(line)
			animeAndAnimeID = line.split(',')
			discordPost.postToDiscord(clientForDiscord, '', animeAndAnimeID[0] + ' - ' + animeAndAnimeID[1], false, "main-channel");
		});
	}

}

var extractAnimeAndAnimeIdPromise = new Promise(function (resolve, reject) {
	var animeAndAnimeID2DArray = []

	lineReader.eachLine('animeList.txt', function (line, last) {
		console.log(line)
		animeAndAnimeID = line.split(',')

		animeAndAnimeID2DArray.push([animeAndAnimeID[1], animeAndAnimeID[0]]);

		if (last) {
			resolve(animeAndAnimeID2DArray)
		}

	});
});


function createReminder(animeName, dateTimeUnixStringForm, episode) {

	var j = schedule.scheduleJob(dateTimeUnixStringForm, function () {

		var strToPost = '@everyone ' + animeName + ' episode: ' + episode + ' is LIVE!'
		discordPost.postToDiscord(clientForDiscord, '', strToPost, false, "main-channel");

	})
	console.log(animeName + ' -- Reminder alert set for anime ' + animeName + ' at ' + j.nextInvocation());
}

function getNextAirDate(id) {

	const query = `
				query($id: Int!) {
								Media(id: $id, type: ANIME) {
										title {
												romaji
												english
												native
												userPreferred
										}
										nextAiringEpisode {
												airingAt
												timeUntilAiring
												episode
										}
								}
						}
				`;

	var url = 'https://graphql.anilist.co',
		options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Accept': 'application/json',
			},
			body: JSON.stringify({
				query: query,
				variables: {
					id: id
				}
			})
		};

	fetch(url, options).then(handleResponse).then(handleData).catch(handleError)
}


/* Functions that deal with handling API return data */

function handleData(data) {

	var anime = data.data.Media.title.romaji;
	var unixAirTime = data.data.Media.nextAiringEpisode.airingAt;

	var nextAirDateString = timeConverterBeautifulString(unixAirTime);
	var nextAirDateCronInput = unixToDateTimeStringCron(unixAirTime);
	var nextEpisodeNumber = data.data.Media.nextAiringEpisode.episode;

	console.log(anime + ' - Creating Reminder at ' + nextAirDateString + ' with cronInput as ' + nextAirDateCronInput);
	createReminder(anime, nextAirDateCronInput, nextEpisodeNumber);
	discordPost.postToDiscord(clientForDiscord, '', anime + ' : will air at --- ' + nextAirDateString, false, "main-channel");

}

function handleResponse(response) {
	return response.json().then(function (json) {
		return response.ok ? json : Promise.reject(json);
	});
}

function handleError(error) {
	//alert('Error, check console');
	console.error(error);
	console.log(JSON.stringify(error));

}

// Functions that deal with translating UNIX time to normal times //

function timeConverterBeautifulString(UNIX_timestamp) {
	//console.log('UNIX time stamp is: ' + UNIX_timestamp);
	var a = new Date(UNIX_timestamp * 1000);
	var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
	var year = a.getFullYear();
	var month = months[a.getMonth()];
	var date = a.getDate();
	var hour = a.getHours();
	var min = "0" + a.getMinutes();
	var sec = "0" + a.getSeconds();
	var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min.substr(-2) + ':' + sec.substr(-2);
	return time;
}


function unixToDateTimeStringCron(UNIX_timestamp) {
	var a = new Date(UNIX_timestamp * 1000);
	var year = a.getFullYear();
	var month = a.getMonth() + 1;
	var date = a.getDate();
	var hour = a.getHours();
	var min = "0" + a.getMinutes();
	var sec = "0" + a.getSeconds();
	var time = min.substr(-2) + ' ' + hour + ' ' + date + ' ' + month + ' *';
	return time;
}