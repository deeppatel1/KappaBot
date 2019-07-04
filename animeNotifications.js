const fetch = require("node-fetch");
var discordPost = require('./discordPost');

animesToPost = {

  attackOnTitan : {
      name: 'Shingeki-no-Kyojin-3',
      id: 104578
  },
  
  onePunchMan : {
    name: 'One_Punch_Man',
    id: 97668
  },
  
  kimetsu : {
    name: 'Kimetsu_no_Yaiba',
    id: 101922
  },

  bokunohero : {
    name: 'Boku_no_Hero_Academia',
    id: 31964
  }

}

var clientForDiscord1;
var anime1;

var variables = {}

module.exports = {
  getAirTime: function (clientForDiscord, anime) {
    clientForDiscord1 = clientForDiscord;
    anime1 = anime;
    variables = {
      id: animesToPost[anime].id
    };

    console.log(variables);

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
              id: animesToPost[anime1].id
            }
        })
    };

    fetch(url, options).then(handleResponse)
                   .then(handleData)
                   .catch(handleError);
  }
}

// Here we define our query as a multi-line string
// Storing it in a separate .graphql/.gql file is also possible
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

// Define our query variables and values that will be used in the query request

// Define the config we'll need for our Api request


// Make the HTTP Api request


function handleResponse(response) {
    return response.json().then(function (json) {
        return response.ok ? json : Promise.reject(json);
    });
}

function handleData(data) {

    console.log(data);
    discordPost.postToDiscord(clientForDiscord1, anime1, 'airing at : ' + timeConverter(data.data.Media.nextAiringEpisode.airingAt) + ' in this amount of days : + ' + (data.data.Media.nextAiringEpisode.timeUntilAiring)/60/60/24, false, "main-channel");
  
    console.log(data.data.Media.nextAiringEpisode.airingAt);
    console.log(timeConverter(data.data.Media.nextAiringEpisode.airingAt));
    console.log((data.data.Media.nextAiringEpisode.timeUntilAiring)/60/60/24);
       
}

function handleError(error) {
    //alert('Error, check console');
    console.error(error);
    console.log(JSON.stringify(error));

}


function timeConverter(UNIX_timestamp){
    var a = new Date(UNIX_timestamp * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
  }
  //console.log(timeConverter(0));