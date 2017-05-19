# coding:utf-8
import re
import twpy
from pprint import *
import MeCab
import CaboCha
import secret

# ref:http://blog.unfindable.net/archives/4257


class StdOutListener(StreamListener):
    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)
        if status.in_reply_to_screen_name == ''