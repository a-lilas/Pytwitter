# coding:utf-8
from requests_oauthlib import OAuth1Session
import json
import pprint
import sys
import tweepy

sys.path.append('./secret_key/')
import secret

auth = tweepy.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)

# APIインスタンスを作成
api = tweepy.API(auth)

print('API インスタンス作成完了')