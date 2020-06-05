#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import re, requests

# 企信
import json, os, random, requests, time, urllib3
Robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=19dd7f92-ff34-46f5-8013-a5ae74825637'

# Stock_API
stock_api_url = 'http://hq.sinajs.cn/list=s_{0}'

# 配置文件
stock_config = 'WorkWeChatStock.conf'

# Stock
class StocksInfo(object):
    def __init__(self, stock_id, stock_val):
        self.stock_id = stock_id
        self.stock_val = stock_val
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
        self.format_stock_info['yingkui'] = float(self.format_stock_info['change'] * int(self.stock_val))
        return self.format_stock_info
    def format_message(self):
        msg = '''代码：%s\n名称：%s\n价格：%s\n涨额：<font color="warning">%s</font>\n涨幅：<font color="warning">%s</font>\n持有：%s\n盈亏：<font color="warning">%s</font>\n''' % (
            self.stock_id,
            self.format_stock_info['name'],
            self.format_stock_info['price'],
            self.format_stock_info['change'],
            self.format_stock_info['rate'],
            self.stock_val,
            self.format_stock_info['yingkui']
        )

        if self.format_stock_info['change'] < 0:
            # info：绿色
            self.msg = msg.replace('warning', 'info')
        elif self.format_stock_info['change'] == 0:
            # comment：灰色
            self.msg = msg.replace('warning', 'comment')
        else:
            # warning：橘红色
            self.msg = msg
        return self.msg
    def do(self):
        self.get_stock_info()
        self.format_stock_info()
        #self.format_message()

class WorkWeChatRobot(object):
    def __init__(self, robot, message):
        self.robot = robot
        self.message = message
    def send_msg(self):
        self.headers = {'Content-Type': 'application/json'}
        self.data = json.dumps({"msgtype": "markdown", "markdown": {"content": self.message}})
        self.http = urllib3.PoolManager()
        self.send = self.http.request(method = 'POST', url = self.robot, body = self.data, headers = self.headers)

if __name__ == '__main__':
    config = ConfigParser()
    config.read(stock_config, encoding = 'utf-8')
    stock_list = config.items('Stock')
    robot_msg = ''
    for stock_id, stock_val in stock_list:
        Obj1 = StocksInfo(stock_id, stock_val)
        Obj1.do()
        msg = Obj1.format_message()
        robot_msgmsg = robot_msg + msg
    #print(robot_msg)

    Obj2 = WorkWeChatRobot(robot = Robot, message = msg)
    Obj2.send_msg()