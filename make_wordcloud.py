# coding:utf-8
import re
import twpy
from pprint import *
import MeCab
from secret_key_bot import secret
import datetime

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Word Cloud 参考
# http://qiita.com/kenmatsu4/items/9b6ac74f831443d29074


class TwitterOperator:

    def __init__(self):
        self.data = []
        self.reply_to_me = []
        self.search_tweet = []
        self.keywords = []
        self.me = twpy.api.me()

    def getTimeline(self, get_id):
        # 特定のidのタイムラインを取得
        user_id = get_id
        for tweet in twpy.api.user_timeline(user_id, count=600):
            self.data.append(tweet)

        return self.data

    def getMyLatestTweetID(self):
        # 自分の最新ツイートを取得,そのツイートIDを返す
        user_id = self.me.id
        latest_tweet = twpy.api.user_timeline(user_id, count=1)[0]
        print(latest_tweet.id)

        return latest_tweet.id

    def getMyMention(self, since_id):
        # 自分への(引数：since_id以降の)リプライを取得する．
        for tweet in twpy.api.mentions_timeline(since_id=since_id):
            self.reply_to_me.append(tweet)
            # print(tweet.text)

        return self.reply_to_me

    def replyCloudImage(self):
        pass

    def searchWord(self, keywords):
        # keywordsについてツイート検索し，その結果を取得
        self.search_tweet = []
        self.keywords = keywords

        # 検索する文字列(ダブルクォーテーションで囲む処理)
        searchwords = list(map(lambda word: '"'+word+'"', self.keywords))

        # Twitter 検索方法
        # queryにキーワードを入れて，api.searchに入れる
        # NOT検索が以下のようにして可能

        # 検索ワード
        query = ' '.join(searchwords)
        # query = ' AND '.join(keywords)
        # query = ' OR '.join(keywords)
        query = query + ' -RT'

        for tweet in twpy.api.search(q=query, count=600):
            self.search_tweet.append(tweet.text)

        return self.search_tweet


def makecloud(tw, filename, object_tweet):
    tmp_list = []
    word_list = []
    r1 = r'\n'
    r2 = r'[\t\, ]'

    # 引数にとったツイート群に対して形態素解析
    for i, tweet in enumerate(object_tweet):
        # MeCabによる実装
        tagger = MeCab.Tagger()
        result = tagger.parse(tweet)

        # 改行による分割
        result = re.split(r1, result)
        # pprint(result)

        for morph in result:
            element = re.split(r2, morph)
            if '名詞' in element and '組織' not in element:
                word_list.append(element[0])

    wordcloud_text = ' '.join(word_list)

    # 環境に合わせてフォントのパスを指定する。
    fpath = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    # fpath = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'

    # ストップワードの設定
    stop_words = [u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', \
                  u'さん', u'して', u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した', \
                  u'思う', u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て', u'に',u'を',u'は', \
                  u'の', u'が', u'と', u'た', u'し', u'で', u'ない', u'も', u'な', u'い', \
                  u'か', u'ので', u'よう', u'', u'https', u'やっ', u'なっ', u'RT'
                  ]

    if len(tw.keywords) > 0:
        stop_words = stop_words + tw.keywords

    wordcloud = WordCloud(background_color="white",
                          font_path=fpath,
                          width=790,
                          height=500,
                          stopwords=set(stop_words)
                          ).generate(wordcloud_text)

    plt.figure(figsize=(12, 9))
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.show()
    plt.savefig(filename)


def __main():
    tw = TwitterOperator()
    # ダブルクォーテーションで検索する単語を囲むこと
    latest_tweet_id = tw.getMyLatestTweetID()

    # 自分へのsince_id以降のリプライを取得
    tw.getMyMention(since_id=latest_tweet_id)
    for status in reversed(tw.reply_to_me):
        status.created_at += datetime.timedelta(hours=9)
        print(status.created_at)
        if str(status.in_reply_to_screen_name) == secret.MY_USER_ID:
            # ツイートから，@以下を削除し，対象単語のみを抽出
            searchword = re.sub(r'^@.+? ', '', status.text)

            # filename:時刻を名前にする
            filename_time = str(datetime.datetime.today())

            if searchword != '@'+secret.MY_USER_ID:
                # 単語が，ユーザ名と一致しない -> 検索単語が含まれている
                # 空白で，リストに分割
                searchword_list = searchword.split()
                print(searchword_list)
                # 入力された単語についてツイート検索
                tw.searchWord(searchword_list)
            else:
                # リプライ内に検索単語が含まれない
                # リプライしてきたユーザのタイムラインを取得
                searchword_list = ['']
                print(searchword_list)
                tw.getTimeline(get_id=status.user.screen_name)

        # ワードクラウド作成
        makecloud(tw, './wordcloud_image/' + filename_time + '.png', tw.search_tweet)

        # ツイート内容を以下の変数に記述
        tweet = '@' + status.user.screen_name + ' ' + ' '.join(searchword_list) + ' ' + filename_time \
                    + ' #wordcloud #ワードクラウド'

        print(status.user.screen_name)

        # 画像を添付してツイート
        twpy.api.update_with_media(filename='./wordcloud_image/'+filename_time+'.png',
                                   status=tweet,
                                   in_reply_to_status_id=status.id
                                   )


if __name__ == '__main__':
    __main()
