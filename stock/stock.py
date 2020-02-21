#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certifi
import json
import os
import re
import requests
import time
import urllib3

stocks = [
         'sh601816',
         'sz000063',
         'sz000725',
         'sz002238',
         'sz002463',
         ]

stock_api_url = "http://hq.sinajs.cn/list=s_{0}"

robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=19dd7f92-ff34-46f5-8013-a5ae74825637'

def send_message(msg, robot = robot):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": msg}})
    http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())
    send = http.request(method = 'POST', url = robot, body = data, headers = headers)
    print(send.data.decode())

def get_stock_info(stock):
    stock_save = stock + '.txt'
    response = requests.get(url = stock_api_url.format(stock))
    response_text = response.text
    stock_info = re.search(r"=\"([ \S]*)\"", response_text).group(1).split(",")
    stock_name = stock_info[0]
    stock_price = stock_info[1]
    if not os.path.exists(stock_save):
        with open(stock_save, 'w+') as f:
            f.write(stock_price)
    else:
        with open(stock_save, 'r+') as f:
            content = f.read()
    try:
        content
    except NameError:
        pass
    else:
        if float(stock_price) > float(content):
            message = '【%s】价格新高，当前价格：【%s】' % (stock_name, stock_price)
            message = message.encode('utf-8')
            send_message(message)
            with open(stock_save, 'r+') as f:
                f.write(stock_price)

while True:
    for stock in stocks:
        get_stock_info(stock)
    time.sleep(5)
