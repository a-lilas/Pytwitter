# coding:utf-8
from requests_oauthlib import OAuth1Session
import json
import secret
import pprint

twitter = OAuth1Session(secret.CONSUMER_KEY, secret.CONSUMER_SECRET, secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)

params = {"status": "Hello, World!"}
req = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)

# timeline = json.loads(req.text)

# for tweet in timeline:
#     print(tweet['user']['name'])
#     print(tweet['text'])
#     print('===')
#     print()
