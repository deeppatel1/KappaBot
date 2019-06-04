var request = require('request');
var credentials = require('./configuration.json');


let formData = {
    grant_type: 'client_credentials',
    client_id: credentials.anilistID,
    client_secret: credentials.anilistSecret
};

module.exports = {
    
    makeAniListCall : function(){
    
        var options = {
            uri: 'https://graphql.anilist.co',
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + 'def5020003d982a563c1c2beb4f1fbd3b6ebc73dc4eae4327a72ad838a70ab16d7da938510350fa3207df552b609523952e72c8e73fe496d0a16917773d0ae2f32fea3b068a0166ecb403854a53ea971f8ce0888e088e3d741e6620be18fed95119df8660240accf6134e910658733a56a75d879ded8237684e78ca7fe959cfe5e0abc231a28b38f2d82171e6a1d3b54532da89d85366a7902d979523ec281cd894e158f090a89df55f7282d25ec46e4faacd0621b1cf46519ce038eefb563107ed8d71e93214212bcd1fadadb8d9a7b60a7b36ab5925220c59f17f63567c749e803e396f02301e8d4b504575bd6a19c17ee78dcd09e6e3cf587b5a7ee30dacc4a2ffc822fd92de32bc617ad1651a75a85d0817354e3c62e875e7140ef58c6b5d381d253bb3bf14c9bed789879157bd41555d72112ee08cbd2fbccae8cdc5a780e6d118b9701a22872c442104c2f00102ee45b3655787d1520b9233b5b36562d682846ef423bad004e085e5b5c659e43',
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            json: {
              'query': query,
            }
          };
          
          request(options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
              console.log(body.data);
            }
          });
    }
}