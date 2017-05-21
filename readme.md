# Twitter WordCloud Generate bot

## Overview  
Twitter用のBotプログラム．  
This is the bot program on Twitter, written in Python3.  

リプライを受け取ると，リプライ中の単語について関連するツイートからワードクラウドを生成するBotです．  
When this bot receives reply, this generates the WordCloud
from tweets related to word in the reply.

## Environment  
* Python 3.6.0 (Anaconda 4.3.0)  
* Mecab 0.996
    * mecab-ipadic-neologd
* Cabocha 0.69
* mecab-python3 0.7
* cabocha-python 0.69
* tweepy 3.5.0