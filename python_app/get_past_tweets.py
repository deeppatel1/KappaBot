import json
with open('./configuration.json') as json_file :
    config = json.load(json_file)

from tweepy import API, OAuthHandler

atoken = config.get("twitterAccessToken")
asecret = config.get("twitterTokenSecret")
ckey = config.get("twitterApiKey")
csecret = config.get("twitterApiKeySecret")

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth)

screen_name = "cheddarflow"

output_dict = []
status = api.user_timeline(screen_name, count=4000, page=8)

for a in status:
    created_at = a._json.get("created_at")
    tweet_text = a._json.get("text")
    if tweet_text[0:1] == "$":
        output_dict.append({
            "createdAt": created_at,
            "text": tweet_text
        })

f = open("page8.txt", "a+")
f.write(str(output_dict))