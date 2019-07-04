const request = require('request');
const cheerio = require('cheerio');

var discordPost = require('./discordPost');

var allMatchesArray = [];

module.exports = {

	getAllMatches: function() {
		return new Promise(async (resolve, reject) => {
			request('https://www.leagueofgraphs.com/lcs/lcs-schedule', function(error, response, html) {

				if (!error && response.statusCode == 200) {
					var $ = cheerio.load(html);
					var recentGames = false;

					var lastLeagueName = '';
					var lastLeagueIcon = '';

					$('td.lcsMatchScoreColumn').each(function(i, element) {
						if (($(this).parent().prev().children().text()) == 'Recent games') {
							recentGames = true;
						}

						if (!recentGames) {

							var timeOfMatch = ($(this).children().last().attr('data-timestamp-time'));
							// console.log("time: " + timeOfMatch)

							var leagueIcon = ($(this).prev().prev().children().children().children().children().attr('src'));
							var leagueName = ($(this).prev().prev().children().children().children().children().attr('title'));

							if (leagueIcon == undefined){
								leagueIcon = lastLeagueIcon;
								leagueName = lastLeagueName;
							} else {
								lastLeagueIcon = leagueIcon;
								lastLeagueName = leagueName;
							}
							
							var leftSideTeamIconAndName = ($(this).prev().children().children().children());

							var leftSideTeamIcon = leftSideTeamIconAndName.children().attr('src');
							var leftSideTeamName = leftSideTeamIconAndName.children().attr('title');

							var rightSideTeamIconAndName = ($(this).next().children().children().children());

							var rightSideTeamIcon = rightSideTeamIconAndName.children().attr('src');
							var rightSideTeamName = rightSideTeamIconAndName.children().attr('title');

							var eachMatch = {
								league: leagueName,
								leagueIcon: leagueIcon,
								dayAndTimeEPOC: timeOfMatch,
								team1: leftSideTeamName,
								team1Icon: leftSideTeamIcon,
								team2: rightSideTeamName,
								team2Icon: rightSideTeamIcon
							}

							allMatchesArray.push(eachMatch);

						}
					});

					resolve(allMatchesArray);

				}

				reject(allMatchesArray);

			});
		});
	},


	getAndPostAllMatches: function(clientForDiscord) {
		var leagueMatchesPromise = this.getAllMatches();
		leagueMatchesPromise.then(returnArrayOfMatches => {
			if (returnArrayOfMatches.length != 0) {
				var counter = 0;
				console.log(returnArrayOfMatches);
				for (var a = 0; (a < returnArrayOfMatches.length) && (counter < 5); a++) {

					if ((returnArrayOfMatches[a]['league'] == 'cblol 2019 1st split') || (returnArrayOfMatches[a]['league'] == '2019 LMS Spring Split') || (returnArrayOfMatches[a]['league'] == 'LJL 2019 Spring Split') || (returnArrayOfMatches[a]['league'] == '2019 LMS Spring Split')) {
						//a = a - 1;
					} else {

						var newDate = new Date(0); // The 0 there is the key, which sets the date to the epoch
						newDate.setUTCSeconds(returnArrayOfMatches[a]['dayAndTimeEPOC']/1000);

						const embed = {
							"color": 9336950,
							"timestamp": newDate,
							"footer": {
								"icon_url": "https:" + returnArrayOfMatches[a]['leagueIcon'], //cdn.leagueofgraphs.com/img/lcs/leagues/64/2.png",
								"text": returnArrayOfMatches[a]['league']
							},
							"thumbnail": {
								"url": "https:" + returnArrayOfMatches[a]['team2Icon']
							},
							"image": {
								"url": "https:" + returnArrayOfMatches[a]['team1Icon']
							},
							"author": {
								"name": returnArrayOfMatches[a]['league'],
								"icon_url": "https:" + returnArrayOfMatches[a]['leagueIcon']
							},
							"fields": [{
									"name": returnArrayOfMatches[a]['team1'],
									"value": "^",
									"inline": true
								},
								{
									"name": returnArrayOfMatches[a]['team2'],
									"value": "^",
									"inline": true
								}
							]
						};

						discordPost.postToDiscord(clientForDiscord, '', {embed: embed}, true, "main-channel");
						counter++;
					}
				}
			}
		});
	}
}