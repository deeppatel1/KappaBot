var request = require('request')

var lineReader = require('line-reader');
const fetch = require("node-fetch");
const fs = require('fs')

var discordPost = require('./discordPost');
var schedule = require('node-schedule');

var clientForDiscord;

var animeIdAnd4AnimeTitle = new Object();

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
				console.log("--ANIME--" + value[eachAnime])
				getTimeUntilAiring(value[eachAnime][0], value[eachAnime][1])
			}
		});
	},

	/*
	addAnime: function (anime, Id, watchAnimeTitle) {
		data = '\n' + anime + ',' + Id + ',' + watchAnimeTitle;
		console.log(data)
		fs.appendFile('animeList.txt', data, (err) => {
			// In case of a error throw err.
			if (err) throw err;
		})
	},
	*/

	viewAnime: function () {
		console.log("--ANIME--" + '---in viewAnime')
		lineReader.eachLine('animeList.txt', function (line) {
			console.log(line)
			animeAndAnimeID = line.split(',')
			discordPost.postToDiscord(clientForDiscord, '', animeAndAnimeID[0] + ' - ' + animeAndAnimeID[1], false, "main-channel");
		});
	},

	/*

	removeAnime: function(anime){
		fs.readFile('animeList.txt', 'utf8', function(err, data){
			var linesToEnterinTxt = [];
			var allLines = data.split('\n');
			for (var eachLine in allLines){
				if (!allLines[eachLine].toLowerCase().includes(anime.toLowerCase())){
					linesToEnterinTxt.push(allLines[eachLine]);
				}
			}

            fs.writeFile('animeList.txt', linesToEnterinTxt.join('\n'), {}, () => {
                fs.close('animeList.txt', () => {});
            });

			console.log(linesToEnterinTxt)
			//var linesExceptFirst = data.split('\n').slice(1).join('\n');
			//fs.writeFile(filename, linesExceptFirst);
		});
	}

	*/
}

var extractAnimeAndAnimeIdPromise = new Promise(function (resolve, reject) {
	var animeAndAnimeID2DArray = []
	lineReader = require('line-reader');
	console.log("--ANIME--" + '--Entered in extractAnimeAndAnimeID')
	lineReader.eachLine('animeList.txt', function (line, last) {
		console.log(line)
		animeAndAnimeID = line.split(',')
		animeIdAnd4AnimeTitle[animeAndAnimeID[1]] = animeAndAnimeID[0]
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
	console.log("--ANIME--" + animeName + ' -- Reminder alert set for anime ' + animeName + ' at ' + j.nextInvocation());
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
										status
										episodes
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
	if (data.data.Media.nextAiringEpisode != null){
		var unixAirTime = data.data.Media.nextAiringEpisode.airingAt;

		var nextAirDateString = timeConverterBeautifulString(unixAirTime);
		var nextAirDateCronInput = unixToDateTimeStringCron(unixAirTime);
		var nextEpisodeNumber = data.data.Media.nextAiringEpisode.episode;

		console.log("--ANIME--" + anime + ' - Creating Reminder at ' + nextAirDateString + ' with cronInput as ' + nextAirDateCronInput);
		createReminder(anime, nextAirDateCronInput, nextEpisodeNumber);
		//discordPost.postToDiscord(clientForDiscord, '', anime + ' : will air at --- ' + nextAirDateString, false, "main-channel");
	}
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
										id
										title {
												romaji
												english
												native
												userPreferred
										}
										siteUrl
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
										status
										episodes
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

	var id = data.data.Media.id;
	var siteUrl = data.data.Media.siteUrl;
	var coverImage = data.data.Media.coverImage.medium;
	var bannerImage = data.data.Media.bannerImage;

	var anime = data.data.Media.title.romaji;


	if ( data.data.Media.nextAiringEpisode != null){
		console.log("--ANIME--" + '--entered if statement')
		var unixAirTime = data.data.Media.nextAiringEpisode.airingAt;
		var episode = data.data.Media.nextAiringEpisode.episode;

		var dateTimeOfAirDate = new Date(unixAirTime * 1000);
	
		var watchanimetitle = animeIdAnd4AnimeTitle[id];

		discordPost.postToDiscord(clientForDiscord, '', {
			embed: createEmbed(anime, dateTimeOfAirDate, bannerImage, episode,watchanimetitle)
		}, true, "main-channel");

	} else {

		var episode = data.data.Media.episodes
		var watchanimetitle = animeIdAnd4AnimeTitle[id];
		discordPost.postToDiscord(clientForDiscord, '', {
			embed: createEmbed(anime, null, bannerImage, episode ,watchanimetitle)
		}, true, "main-channel");

	}
}


function createEmbed(anime, airDateTime, bannerImage, episode, watchanimetitle) {
	
	var text = ''

	if (airDateTime == null){
		text = "This show is done!"
		episode = episode + 1
	}else{
		text = 'Episode ' + episode + ' will air'
	}

	var episodeMinus1Link = 'https://4anime.to/' + watchanimetitle + '-episode-' + ('0' + (episode - 1)).slice(-2);
	var episodeMinus2Link = 'https://4anime.to/' + watchanimetitle + '-episode-' + ('0' + (episode - 2)).slice(-2);

	const embed = {
		color: 0x0099ff,
		title: anime,
		image: {
			url: bannerImage,
		},
		timestamp: airDateTime,
		footer: {
			text: text
		},
		fields: [],
	};

	console.log('--next episode for ' + anime + ' is ' + episode)

	if (episode > 1){
		embed.fields.push({
			name: 'Watch Episode ' + (episode-1).toString() + ':',
			value: episodeMinus1Link	
		})
		
		if (episode > 2){
			embed.fields.push({
				name: 'Watch Episode ' + (episode-2).toString() + ':',
				value: episodeMinus2Link
			})
		}
	}

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
