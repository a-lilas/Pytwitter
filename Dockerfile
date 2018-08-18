FROM ubuntu:16.04

RUN apt-get update \
  && apt-get install python3 python3-pip python3-tk python3-dev python3-setuptools curl git sudo cron -y

RUN apt-get install -y libfreetype6-dev
RUN apt-get install -y fonts-takao-pgothic

ENV PYTHONIOENCODING=UTF-8

WORKDIR /opt
RUN git clone https://github.com/taku910/mecab.git
WORKDIR /opt/mecab/mecab
RUN ./configure  --enable-utf8-only \
  && make \
  && make check \
  && make install \
  && ldconfig

WORKDIR /opt/mecab/mecab-ipadic
RUN ./configure --with-charset=utf8 \
  && make \
  && make install

WORKDIR /opt
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR /opt/mecab-ipadic-neologd
RUN ./bin/install-mecab-ipadic-neologd -n -y

WORKDIR /
RUN git clone https://github.com/a-lilas/twitter-wordcloud-bot.git
WORKDIR /twitter-wordcloud-bot

RUN pip3 install --upgrade pip
RUN pip install tweepy pillow==2.9.0 wordcloud mecab-python3 matplotlib
# RUN pip install pillow==2.9.0
# RUN pip install wordcloud
# RUN pip install mecab-python3

WORKDIR /root/.config/matplotlib
RUN echo 'backend : Agg' >> ./matplotlibrc

WORKDIR /twitter-wordcloud-bot
CMD [ "python3", "make_wordcloud.py" ]