# coding:utf-8
import re
import twpy
from pprint import *
import MeCab
import secret
import datetime

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Word Cloud 参考
# http://qiita.com/kenmatsu4/items/9b6ac74f831443d29074


class TwitterOperator:

    def __init__(self):
        self.data = []
        self.keywords = []

    def getTimeline(self, get_id):
        # 特定のidのタイムラインを取得
        user_id = get_id
        for tweet in twpy.api.user_timeline(user_id, count=600):
            self.data.append(tweet.text)

        return self.data

    def searchWord(self, keywords):
        # keywordsについてツイート検索し，その結果を取得

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
            self.data.append(tweet.text)

        return self.data


def makecloud(tw, filename):
    tmp_list = []
    word_list = []
    r1 = r'\n'
    r2 = r'[\t\, ]'

    for i, tweet in enumerate(tw.data):
        # MeCabによる実装
        tagger = MeCab.Tagger(' -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
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
    # fpath = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    fpath = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'

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


def main():
    tw = TwitterOperator()
    # ダブルクォーテーションで検索する単語を囲むこと
    tw.searchWord(['てすと'])
    makecloud(tw, filename='aiueo')

if __name__ == '__main__':
    main()
