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
		extractAnimeAndAnimeIdPromise.then(function (value) {
			for (var eachAnime in value) {
				getNextAirDate(value[eachAnime][0], value[eachAnime][1])
			}
		});
	},

	extractAnimeAndAnimeID: function () {
		extractAnimeAndAnimeIdPromise.then(function (value) {
			for (var eachAnime in value) {
				getTimeUntilAiring(value[eachAnime][0], value[eachAnime][1])
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

/* 
//		Functions that deal with handling API return data OF GETTING NEXT AIR DATE!
//
//
*/

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

function handleData(data) {

	var anime = data.data.Media.title.romaji;
	var unixAirTime = data.data.Media.nextAiringEpisode.airingAt;

	var nextAirDateString = timeConverterBeautifulString(unixAirTime);
	var nextAirDateCronInput = unixToDateTimeStringCron(unixAirTime);
	var nextEpisodeNumber = data.data.Media.nextAiringEpisode.episode;

	console.log(anime + ' - Creating Reminder at ' + nextAirDateString + ' with cronInput as ' + nextAirDateCronInput);
	createReminder(anime, nextAirDateCronInput, nextEpisodeNumber);
	//discordPost.postToDiscord(clientForDiscord, '', anime + ' : will air at --- ' + nextAirDateString, false, "main-channel");

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

/* 
//		Functions that deal with handling API return data OF GETTING TIME UNTIL NEXT "Airing Until"
//
//
*/

function getTimeUntilAiring(id) {

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
										coverImage {
												large
												medium
										}
										bannerImage
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

	fetch(url, options).then(handleResponseForAiringUntil).then(handleDataForAiringUntil).catch(handleErrorForAiringUntil)
}

function handleDataForAiringUntil(data) {

	console.log(data.data.Media.coverImage.large)

	var coverImage = data.data.Media.coverImage.medium;
	var bannerImage = data.data.Media.bannerImage;

	var anime = data.data.Media.title.romaji;
	var unixAirTime = data.data.Media.nextAiringEpisode.airingAt;
	var episode = data.data.Media.nextAiringEpisode.episode;

	var dateTimeOfAirDate = new Date(unixAirTime * 1000);
	
	/*var currentDateTime = new Date();
	
	var seconds = Math.floor((dateTimeOfAirDate - (currentDateTime))/1000);
	var minutes = Math.floor(seconds/60);
	var hours = Math.floor(minutes/60);
	var days = Math.floor(hours/24);

	hours = hours-(days*24);
	minutes = minutes-(days*24*60)-(hours*60);
	seconds = seconds-(days*24*60*60)-(hours*60*60)-(minutes*60);

	if (hours == 0) {
		var msgToPost = anime + ' ~ Episode ' + episode + ' will air in ~ ' + hours + ' hours ' + minutes + ' minutes ' + seconds + ' seconds!';
	}else{
		var msgToPost = anime + ' ~ Episode ' + episode + ' will air in ~ ' + days + ' days ' + hours + ' hours ' + minutes + ' minutes ' + seconds + ' seconds!';

	}
*/
	console.log(anime + ' posting with embed: ' + createEmbed(anime, dateTimeOfAirDate, bannerImage, episode));

	discordPost.postToDiscord(clientForDiscord, '', {
		embed: createEmbed(anime, dateTimeOfAirDate, bannerImage, episode)
	}, true, "main-channel");

}


function createEmbed(anime, airDateTime, bannerImage, episode) {
	const embed = {
		color: 0x0099ff,
		title: anime,
		//description: 'Some description here',
		//thumbnail: {
		//	url: coverImage,
		//},
		image: {
			url: bannerImage,
		},
		timestamp: airDateTime,
		footer: {
			text: 'Episode ' + episode + ' will air'
		},
	};

	return embed

}


function handleResponseForAiringUntil(response) {
	return response.json().then(function (json) {
		return response.ok ? json : Promise.reject(json);
	});
}

function handleErrorForAiringUntil(error) {
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

function getDateDifference(start, end) {
	var secondsDifference = Math.round((start.getTime() - end.getTime()) / 1000);
	var hours = Math.floor(secondsDifference / 3600);
    secondsDifference -= hours * 3600
    var minutes = Math.floor(secondsDifference / 60);
    secondsDifference -= minutes * 60;
    var seconds = secondsDifference % 60;
    return hours + ":" + minutes + ":" + seconds;
}