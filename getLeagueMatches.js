const request = require('request');
const cheerio = require('cheerio');

var discordFuncs = require('./discordPostAndResponse.js');
var discordPost = require('./discordPost');

var moment = require('moment');

var allMatchesArray = [];

module.exports = {

	getAllMatches: function() {
		return new Promise(async (resolve, reject) => {
			request('https://www.leagueofgraphs.com/lcs/lcs-schedule', function(error, response, html) {

				if (!error && response.statusCode == 200) {
					var $ = cheerio.load(html);
					var recentGames = false;
					$('td.lcsMatchScoreColumn').each(function(i, element) {

						if (($(this).parent().prev().children().text()) == 'Recent games') {
							recentGames = true;
						}

						if (!recentGames) {

							var timeOfMatch = ($(this).children().last().attr('data-timestamp-time'));

							var leagueIcon = ($(this).prev().prev().children().children().children().children().attr('src'));
							var leagueName = ($(this).prev().prev().children().children().children().children().attr('title'));

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
				for (var a = 0;
					(a < returnArrayOfMatches.length) && (a < 10); a++) {

					if ((returnArrayOfMatches[a]['league'] == 'cblol 2019 1st split') || (returnArrayOfMatches[a]['league'] == '2019 LMS Spring Split') || (returnArrayOfMatches[a]['league'] == 'LJL 2019 Spring Split') || (returnArrayOfMatches[a]['league'] == '2019 LMS Spring Split')) {
						//a = a - 1;
					} else {

						var newDate = moment.unix(returnArrayOfMatches[a]['dayAndTimeEPOC']);
						console.log(newDate);
						const embed = {
							"description": "```\n" + newDate + "```",
							"color": 9336950,
							"timestamp": new Date(),
							"footer": {
								"icon_url": "https:" + returnArrayOfMatches[a]['leagueIcon'], //cdn.leagueofgraphs.com/img/lcs/leagues/64/2.png",
								"text": "LCS"
							},
							"thumbnail": {
								"url": "https:" + returnArrayOfMatches[a]['leagueIcon']
							},
							"image": {
								"url": "https:" + returnArrayOfMatches[a]['team1Icon']
							},
							"author": {
								"name": returnArrayOfMatches[a]['league'],
								"icon_url": "https:" + returnArrayOfMatches[a]['leagueIcon']
							},
							"fields": [{
									"name": "_",
									"value": returnArrayOfMatches[a]['team1'],
									"inline": true
								},
								{
									"name": "_",
									"value": returnArrayOfMatches[a]['team2'],
									"inline": true
								}
							]
						};

						discordPost.postToDiscord(clientForDiscord, '', {embed: embed}, true);

					}
				}
			}
		});
	}
}