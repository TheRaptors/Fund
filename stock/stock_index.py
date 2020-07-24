#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certifi
import datetime
import json
import os
import re
import requests
import time
import urllib3

# 股票列表
stocks_list = ['sh000001', 'sh000688', 'sz399001', 'sz399006']

stock_api_url = "http://hq.sinajs.cn/list=s_{0}"

robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d9e61993-7cc2-45ea-a64a-65e92e615bbe'

def send_message(msg, robot = robot):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": msg}})
    http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())
    send = http.request(method = 'POST', url = robot, body = data, headers = headers)
    print(send.data.decode())

def get_stock_info(stock_id):
    stock_save = stock_id + '.txt'
    response = requests.get(url = stock_api_url.format(stock_id))
    response_text = response.text
    stock_info = re.search(r"=\"([ \S]*)\"", response_text).group(1).split(",")
    stock_name = stock_info[0]
    stock_price = stock_info[1]
    stock_change = stock_info[2]
    stock_changePercent = stock_info[3]
    if float(stock_change) >= 0:
        message = u'【%s】【<font color="#FF0000">%s</font>】，涨幅：【<font color="#FF0000">%s%%</font>】，涨跌：【<font color="#FF0000">%s</font>】' % (stock_name, stock_price, stock_changePercent, stock_change)
    else:
        message = u'【%s】【<font color="#008000">%s</font>】，涨幅：【<font color="#008000">%s%%</font>】，涨跌：【<font color="#008000">%s</font>】' % (stock_name, stock_price, stock_changePercent, stock_change)

    return message

TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
msg = []

for stock_id in stocks_list:
    stock_id = stock_id.replace('.', '')
    message = get_stock_info(stock_id)
    msg.append(message)

ALL = TIME + '\n' + msg[0] + '\n' + msg[1] + '\n' + msg[2] + '\n' + msg[3]

send_message(msg = ALL)
