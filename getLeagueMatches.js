const request = require('request');
const puppeteer = require('puppeteer-core')
const cheerio = require('cheerio')

var discordPost = require('./discordPost');

var allMatchesArray = [];

module.exports = {

	getAllMatches: function () {
		return new Promise(async (resolve, reject) => {
			// set some options (set headless to false so we can see 
			// this automated browsing experience)
			const browser = await puppeteer.launch({executablePath: '/usr/bin/chromium-browser'});

			const page = await browser.newPage();
		
			// go to the target web
			await page.goto('https://watch.lolesports.com/schedule?leagues=lcs,lck');
		
			content = (await page.content());
			const $ = cheerio.load(content)
			console.log($)
			console.log($.html())
			

			// close the browser
			await browser.close();
		});
	},


	getAndPostAllMatches: function (clientForDiscord) {
		var leagueMatchesPromise = this.getAllMatches();
		leagueMatchesPromise.then(returnArrayOfMatches => {
			if (returnArrayOfMatches.length != 0) {
				var counter = 0;
				//console.log(returnArrayOfMatches);
				for (var a = 0;
					(a < returnArrayOfMatches.length) && (counter < 6); a++) {

					if ((returnArrayOfMatches[a]['league'].includes(('cblol'))) || (returnArrayOfMatches[a]['league'].includes(('LMSS'))) || (returnArrayOfMatches[a]['league'].includes(('LJL'))) || (returnArrayOfMatches[a]['league'].includes(('LMS'))) || (returnArrayOfMatches[a]['league'].includes(('OPL'))) || (returnArrayOfMatches[a]['league'].includes(('CBLoL')))) {
						//a = a - 1;
					} else {

						var newDate = new Date(0); // The 0 there is the key, which sets the date to the epoch
						newDate.setUTCSeconds(returnArrayOfMatches[a]['dayAndTimeEPOC'] / 1000);

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

						discordPost.postToDiscord(clientForDiscord, '', {
							embed: embed
						}, true, "main-channel");
						counter++;
					}
				}
			}
		});
	}
}
