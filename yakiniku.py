# coding:utf-8
import twpy

keywords = ['焼肉']

# Twitter 検索方法
# queryにキーワードを入れて，api.searchに入れる
# query = ' OR '.join(keywords)
query = keywords
for tweet in twpy.api.search(q=query, count=100):
    print(tweet.text)