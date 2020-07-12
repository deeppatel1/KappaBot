from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

with open('../configuration.json') as json_file :
    config = json.load(json_file)

class listener(StreamListener):

    def on_data(self, data):
        print(data)
        return(True)

    def on_error(self, status):
        print(status)

print(config.get("twitterAccessToken"))
print(config.get("twitterTokenSecret"))
print(config.get("twitterApiKey"))
print(config.get("twitterApiSecretKey"))

#auth = OAuthHandler(config.get("twitterAccessToken"), config.get("twitterTokenSecret"))
#auth.set_access_token(config.get("twitterApiKey"), config.get("twitterApiSecretKey"))


auth = OAuthHandler(config.get("twitterApiKey"), config.get("twitterApiSecretKey"))
auth.set_access_token(config.get("twitterAccessToken"), config.get("twitterTokenSecret"))

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["bitcoin"])