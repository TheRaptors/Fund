#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
保存消息为md文件，内容为table格式，企信机器人暂不支持
2019.08.16
"""

from configparser import ConfigParser
import re, requests

# 企信
import json, os, random, requests, time, urllib3
Robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=19dd7f92-ff34-46f5-8013-a5ae74825637'

# Stock_API
stock_api_url = 'http://hq.sinajs.cn/list=s_{0}'

# 配置文件及消息文件
stock_config = 'WorkWeChatStock.conf'
stock_message = 'WorkWeChatStock.md'

# 企信机器人发送消息的头部信息
def Msg_Headers(Msg_File):
    msg = '''|代码|名称|价格|涨额|涨幅|持有|盈亏|\n|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n'''
    with open(Msg_File, 'wt', encoding = 'utf-8') as f:
        f.write(msg)

# 创建消息文件
Msg_Headers(Msg_File = stock_message)

# Stock
class StocksInfo(object):
    def __init__(self, stock_id, stock_val, stock_message):
        self.stock_id = stock_id
        self.stock_val = stock_val
        self.stock_message = stock_message
    def get_stock_info(self):
        request = requests.get(stock_api_url.format(self.stock_id))
        info = request.text
        self.stock_info = re.search(r"=\"([ \S]*)\"", info).group(1).split(',')
        return self.stock_info
    def format_stock_info(self):
        self.format_stock_info = {}
        self.format_stock_info['name'] = self.stock_info[0]
        self.format_stock_info['price'] = float(self.stock_info[1])
        self.format_stock_info['change'] = float(self.stock_info[2])
        self.format_stock_info['rate'] = float(self.stock_info[3])
        self.format_stock_info['yingkui'] = float(self.format_stock_info['change']*int(self.stock_val))
        return self.format_stock_info
    def format_message(self):
        line = '''|%s|%s|%s|%s|%s|%s|%s|''' % (
            self.stock_id,
            self.format_stock_info['name'],
            self.format_stock_info['price'],
            self.format_stock_info['change'],
            self.format_stock_info['rate'],
            self.stock_val,
            self.format_stock_info['yingkui']
        )
        with open(self.stock_message, 'at', encoding = 'utf-8') as f:
            f.write(line + '\n')
    def do(self):
        self.get_stock_info()
        self.format_stock_info()
        self.format_message()

class WorkWeChatRobot(object):
    def __init__(self, robot, message):
        self.robot = robot
        self.message = message
    def read_message(self):
        with open(self.message, 'r', encoding = 'utf-8') as f:
            self.data = f.read()
        return self.data
    def send_msg(self):
        self.headers = {'Content-Type': 'application/json'}
        self.data = json.dumps({"msgtype": "markdown", "markdown": {"content": self.data}})
        self.http = urllib3.PoolManager()
        self.send = self.http.request(method = 'POST', url = self.robot, body = self.data, headers = self.headers)
    def do(self):
        self.read_message()
        self.send_msg()

if __name__ == '__main__':
    config = ConfigParser()
    config.read(stock_config, encoding = 'utf-8')
    stock_list = config.items('Stock')

    for stock_id, stock_val in stock_list:
        Obj1 = StocksInfo(stock_id, stock_val, stock_message)
        Obj1.do()

    Obj2 = WorkWeChatRobot(robot = Robot, message = stock_message)
    Obj2.do()