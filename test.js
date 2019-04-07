const request = require('request');
const cheerio = require('cheerio');

var allMatchesArray = [];


module.exports = {

  getAllMatches = function(){
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
}
}