# coding:utf-8
import re
import twpy
import tweepy
from pprint import *
import datetime
import secret
import make_wordcloud as makewc

# ref:http://blog.unfindable.net/archives/4257


class Listener(tweepy.StreamListener):
    def __init__(self, api):
        # 初期化
        super().__init__(api)
        self.me = twpy.api.me()

    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)
        if str(status.in_reply_to_screen_name) == secret.MY_USER_ID:
            # ツイートから，@以下を削除し，対象単語のみを抽出
            searchword = re.sub(r'^@.+? ', '', status.text)

            # filename:時刻を名前にする
            filename_time = str(datetime.datetime.today())

            # ツイート簡易操作クラス作成
            tw = makewc.TwitterOperator()

            if searchword != '@'+secret.MY_USER_ID:
                # 単語が，ユーザ名と一致しない -> 検索単語が含まれている
                # 空白で，リストに分割
                searchword_list = searchword.split()
                # 入力された単語についてツイート検索
                tw.searchWord(searchword_list)
            else:
                # リプライ内に検索単語が含まれない
                # リプライしてきたユーザのタイムラインを取得
                searchword_list = ['']
                tw.getTimeline(get_id=status.user.screen_name)

            # ワードクラウド作成
            makewc.makecloud(tw, './wordcloud_image/' + filename_time + '.png')

            # ツイート内容を以下の変数に記述
            tweet = '.@' + status.user.screen_name + ' ' + ' '.join(searchword_list) + ' ' + filename_time \
                                    + ' #wordcloud #ワードクラウド'
            # 画像を添付してツイート
            twpy.api.update_with_media(filename='./wordcloud_image/'+filename_time+'.png',
                                       status=tweet,
                                       in_reply_to_status_id=status.id
                                       )

            # ログ出力
            f.write(' '.join(searchword_list) + ' ' + filename_time + '\n')

        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')

    def on_event(self, event):
        try:
            if event.event == 'follow':
                print("followed")
                if self.me.id != event.source["id"]:
                    source_user = event.source
                    twpy.api.create_friendship(source_user["id"])
                    print("followed　by {} {}".format(source_user["name"], source_user["screen_name"]))
        except:
            pass


# ログファイルに追記モードで読み込み
with open('./log/wordlog.log', 'a') as f:
    # Twitterオブジェクトの生成
    listener = Listener(twpy.api)
    stream = tweepy.Stream(twpy.auth, listener)
    stream.userstream()

