import json
import csv
import re
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

screen_name = "MAK__trading"

REGEX_RULE = r"[A-Z]{1,4}"

output_dict = []

TRADES_KEYWORDS = ["sold", "bought", "out"]

# for a in range(1,10):

status = api.user_timeline(screen_name, count=200, page=5)
for a in status:
    created_at = a._json.get("created_at")
    if a._json.get("truncated"):
        tweet_text = a._json.get("text").replace("\n", "")
    else:
        tweet_text = a._json.get("text").replace("\n", "")
    
    # if tweet_text[0:1] != "@" and tweet_text[0:2] != "RT":
    if (tweet_text[0:1] != "@") and (tweet_text[0:2] != "RT") and any(word in tweet_text.lower() for word in TRADES_KEYWORDS):
        regex_rule = re.findall(REGEX_RULE, tweet_text)
        if regex_rule:
            dict = {
                "createdAt": created_at,
                "text": tweet_text,
            }

            # take out "A" or "ALL" or 1 char length

            for x in regex_rule:
                if len(x) == 1:
                    del x
                print(regex_rule)


            dict["ticker"] = regex_rule

            # print(dict)
            output_dict.append(dict)
keys = output_dict[0].keys()
with open('onlyBuysAndSells.csv', 'a', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    # dict_writer.writeheader()
    dict_writer.writerows(output_dict)
