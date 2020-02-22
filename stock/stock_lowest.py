#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
证券宝：http://baostock.com/
安装模块：pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
'''

# 证券宝相关模块
import baostock as bs
import pandas as pd

# 日期、时间模块
import datetime
import time

# 其他模块
import certifi
import json
import os
import re
import requests
import urllib3

# 股票列表
stocks_list = [
    'sh.601816',
    'sz.000063',
    'sz.000725',
    'sz.002238',
    'sz.002463',
]

stock_api_url = "http://hq.sinajs.cn/list=s_{0}"
robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=19dd7f92-ff34-46f5-8013-a5ae74825637'

# 获取起始时间
def get_date(num):
    today = datetime.datetime.now()
    offset = datetime.timedelta(days = -num)
    date = (today + offset).strftime('%Y-%m-%d')
    return date

# 获取股票历史数据
def get_stock_info_history(stock_id, start_date, end_date):
    # 登录系统
    login = bs.login()
    # 显示登录返回信息
    #print('login respond error code: %s' % login.error_code)
    #print('login respond error msg: %s' % login.error_msg)

    # 获取沪深 A 股历史 K 线数据
    # 详细指标参数，参见'历史行情指标参数'章节；'分钟线'参数与'日线'参数不同。
    # 分钟线指标：date, code, open, high, low, close, volume, amount, adjustflag
    stock_info = bs.query_history_k_data_plus(stock_id, 'date, code, open, high, low, close, volume, amount, adjustflag', start_date = start_date, end_date = end_date, frequency = 'd', adjustflag = '3')
    #print('query_history_k_data_plus respond error code: %s' % stock_info.error_code)
    #print('query_history_k_data_plus respond error msg: %s' % stock_info.error_msg)

    # 打印结果集
    lowest_list = []
    while stock_info.error_code == '0' and stock_info.next():
        # 获取第一条记录，将记录合并在一起
        lowest_list.append("%.2f" % float(stock_info.get_row_data()[4]))
    lowest = min(lowest_list)

    # 登出系统
    bs.logout()

    return lowest

def send_message(msg, robot = robot):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": msg}})
    http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())
    send = http.request(method = 'POST', url = robot, body = data, headers = headers)
    print(send.data.decode())

# 获取股票当前数据
def get_stock_info_now(stock_id):
    stock_save = stock_id + '.txt'
    response = requests.get(url = stock_api_url.format(stock_id))
    response_text = response.text
    stock_info = re.search(r"=\"([ \S]*)\"", response_text).group(1).split(",")
    stock_name = stock_info[0]
    stock_price = stock_info[1]
    return stock_name, stock_price

# 截止日期为昨天，此为固定值
end_date = get_date(1)
history = [7, 15, 30]

for stock_id in stocks_list:
    stock_save = stock_id + '.txt'
    if os.path.exists(stock_save):
        os.remove(stock_save)

for i in history:
    start_date = get_date(i)
    for stock_id in stocks_list:
        stock_save = stock_id + '.txt'
        lowest = get_stock_info_history(stock_id = stock_id, start_date = start_date, end_date = end_date)
        with open(stock_save, 'a+') as f:
            f.write(lowest)
            f.write('\n')

while True:
    for i in range(len(history)):
        for stock_id in stocks_list:
            stock_save = stock_id + ".txt"
            stock_id = stock_id.replace('.', '')
            result = get_stock_info_now(stock_id)
            with open(stock_save) as f:
                lowest = f.readlines()[i]
                if result[1] <= lowest:
                    message = '【%s】当前价格【%s】低于【%s】天历史价格【%s】' % (result[0], result[1], history[i], lowest)
                    #message = message.encode('utf-8')
                    send_message(message)
    time.sleep(10)
