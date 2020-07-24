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

stock_api_url = "https://image.sinajs.cn/newchart/min/n/{0}.png"

import base64, hashlib, json, os, urllib3

robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d9e61993-7cc2-45ea-a64a-65e92e615bbe'


class WorkWeChatRobot(object):
    def __init__(self, stock, robot):
        self.stock = stock
        self.robot = robot

    def save_pic(self):
        request = requests.get(url=stock_api_url.format(self.stock))

        with open(self.stock, 'wb') as f:
            f.write(request.content)
        self.image = self.stock

    def get_info(self):
        with open(self.image, 'rb') as f:
            fr = f.read()
            self.image_md5 = hashlib.md5(fr).hexdigest()
            self.image_base64 = base64.b64encode(fr)

    def send_msg(self):
        self.save_pic()
        self.get_info()
        self.data = json.dumps(
            {"msgtype": "image", "image": {"base64": self.image_base64.decode(), "md5": self.image_md5}})
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        self.send = self.http.request(method='POST', url=self.robot, body=self.data,
                                      headers={'Content-Type': 'application/json'})
        print(self.send.data)


if __name__ == '__main__':
    for i in stocks_list:
        Obj = WorkWeChatRobot(stock=i, robot=robot)
        Obj.send_msg()
