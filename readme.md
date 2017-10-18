# Twitter WordCloud Generate bot

## Overview  
Twitter用のBotプログラム．  
This is the bot program on Twitter, written in Python3.  

リプライを受け取ると，リプライ中の単語について関連するツイートからワードクラウドを生成するBotです．  
When this bot receives reply, this generates the WordCloud
from tweets related to word in the reply.

## How to Use
- Dockerイメージの作成  
`docker build -t <name> .`
- Dockerコンテナの起動  
`docker run -d -it -v /path/to/secret.py:/twitter-wordcloud-bot/secret_key_bot/secret.py <name>`

## Twitter API Key
ホストとコンテナ間における鍵の移動については，`-v`を用いて行う．