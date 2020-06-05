#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, random, requests, time, urllib3
import pysnooper

Robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d9e61993-7cc2-45ea-a64a-65e92e615bbe'

class WorkWeChatRobot(object):
    def __init__(self, seconds, robot):
        self.seconds = seconds
        self.robot = robot
    def get_news(self):
        try:
            news_source = 'https://api.readhub.me/topic'
            resp = requests.get(url = news_source)
            self.status_code = resp.status_code
            self.json = resp.json()
        except Exception as e:
            print(e)
        return self.status_code, self.json
    def format_news(self):
        self.news = []
        for data in self.json['data']:
            new = {}
            new['id'] = data['id']
            new['url'] = data['newsArray'][0]['url']
            new['title'] = data['title']
            new['content'] = data['summary']
            self.news.append(new)
        return self.news
    def filter_news(self):
        self.is_not_exist_news = []
        with open('readhub.log', 'r') as f:
            news_id = f.read()
        self.is_exist_news = news_id.split('|')
        for new in self.news:
            if new['id'] not in self.is_exist_news:
                self.is_not_exist_news.append(new)
        return self.is_not_exist_news
    def format_news_str(self):
        #return self.choice_new['title'] + '\n' + self.choice_new['url'] + '\n' + self.choice_new['content']
        news_title = self.choice_new['title']
        news_url = self.choice_new['url']
        news_content = self.choice_new['content']
        self.msg = '[' + news_title + ']' + '(' + news_url + ')' + '\n' + news_content
        return self.msg
    def send_news(self):
        self.headers = {'Content-Type': 'application/json'}
        self.data = json.dumps({"msgtype": "markdown", "markdown": {"content": self.format_news_str()}})
        self.http = urllib3.PoolManager()
        self.send = self.http.request(method = 'POST', url = self.robot, body = self.data, headers = self.headers)
    def log_news(self):
        with open('readhub.log', 'a') as f:
            f.write('{0}|'.format(self.choice_new['id']))
    def choice_news(self):
        try:
            while True:
                if self.status_code != 200:
                    print(self.status_code)
                    time.sleep(60)
                    continue
                news = self.format_news()
                news = self.filter_news()
                if len(news) >= 1:
                    self.choice_new = random.choice(news)
                    self.send_news()
                    self.log_news()
                time.sleep(self.seconds)
        except Exception as e:
            print(e)
    def do(self):
        self.get_news()
        self.format_news()
        self.filter_news()
        self.choice_news()

if __name__ == '__main__':
    obj = WorkWeChatRobot(seconds = 1800, robot = Robot)
    obj.do()