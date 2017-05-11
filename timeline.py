# coding:utf-8
from requests_oauthlib import OAuth1Session
import json
import pprint
import sys

sys.path.append('./secret_key/')
import secret

twitter = OAuth1Session(secret.CONSUMER_KEY,
                        secret.CONSUMER_SECRET,
                        secret.ACCESS_TOKEN,
                        secret.ACCESS_TOKEN_SECRET
                        )

class getTwitterInfo:
    def __init__(self):
        pass

    def getTimeline(self):
        params = {}
        # Resource URL
        url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        req = twitter.get(url, params=params)
        timeline = json.loads(req.text)

        return timeline

        # for tweet in timeline:
        #     print(tweet['user']['name'])
        #     print(tweet['text'])
        #     print('===')
        #     print()

    def getUserInfo(self):
        pass


def __main():
    get_object = getTwitterInfo()
    timeline = get_object.getTimeline()

if __name__ == '__main__':
    __main()