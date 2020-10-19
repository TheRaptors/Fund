#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certifi
import json
import os
import re
import requests
import time
import urllib3

# 股票列表
stocks_list = []

with open('config.ini', 'r+') as f:
    fr = f.readlines()
    for i in fr:
        stocks_list.append(i.strip('\n'))

# 股票价格
stocks_price = {}

stock_api_url = "http://hq.sinajs.cn/list=s_{0}"

robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=19dd7f92-ff34-46f5-8013-a5ae74825637'


def send_message(msg, robot=robot):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": msg}})
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    send = http.request(method='POST', url=robot, body=data, headers=headers)
    print(send.data.decode())


def get_stock_info(stock_id):
    response = requests.get(url=stock_api_url.format(stock_id))
    response_text = response.text
    stock_info = re.search(r"=\"([ \S]*)\"", response_text).group(1).split(",")
    stock_name = stock_info[0]
    stock_price = stock_info[1]
    stock_change = stock_info[2]
    stock_changePercent = stock_info[3]

    if stock_id not in stocks_price:
        stocks_price[stock_id] = stock_price
    else:
        content = stocks_price[stock_id]

    try:
        content
    except NameError:
        pass

    else:
        if float(stock_price) > float(content):
            if float(stock_change) > 0:
                message = u'【%s】价格<font color="#FF0000">新高</font>，当前价格：【<font color="#FF0000">%s</font>】，涨幅：【<font color="#FF0000">%s%%</font>】，涨跌：【<font color="#FF0000">%s</font>】' % (stock_name, stock_price, stock_changePercent, stock_change)
            else:
                message = u'【%s】价格<font color="#008000">新高</font>，当前价格：【<font color="#008000">%s</font>】，涨幅：【<font color="#008000">%s%%</font>】，涨跌：【<font color="#008000">%s</font>】' % (stock_name, stock_price, stock_changePercent, stock_change)
            send_message(message)
            stocks_price[stock_id] = stock_price


# 当前日期
date = time.strftime('%Y-%m-%d', time.localtime())
# 当前日期 00:00:00 时间戳
timestamp1 = int(time.mktime(time.strptime(date, '%Y-%m-%d')))

while True:
    # 当前时间
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # 当前时间戳
    timestamp2 = int(time.mktime(time.strptime(now, '%Y-%m-%d %H:%M:%S')))
    # 时间差
    diff = timestamp2 - timestamp1

    if diff >= int(9.5 * 3600) and diff <= int(15 * 3600):

        for stock_id in stocks_list:
            if stock_id[0:2] == '60' or stock_id[0:3] == '900':
                stock_id = 'sh.' + stock_id
            elif stock_id[0:2] == '00' or stock_id[0:3] == '200' or stock_id[0:3] == '300':
                stock_id = 'sz.' + stock_id
            stock_id = stock_id.replace('.', '')
            get_stock_info(stock_id)
        time.sleep(10)
    else:
        break
