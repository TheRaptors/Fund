#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64, hashlib, json, os, urllib3
import pysnooper

Robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d9e61993-7cc2-45ea-a64a-65e92e615bbe'

class WorkWeChatRobot(object):
    def __init__(self, image, robot):
        self.image = image
        self.robot = robot
    def get_info(self):
        with open(self.image, 'rb') as f:
            fr = f.read()
            self.image_md5 = hashlib.md5(fr).hexdigest()
            self.image_base64 = base64.b64encode(fr)
    @pysnooper.snoop()
    def send_msg(self):
        self.get_info()
        self.data = json.dumps({"msgtype": "image", "image": {"base64": self.image_base64.decode(), "md5": self.image_md5}})
        self.http = urllib3.PoolManager()
        self.send = self.http.request(method = 'POST', url = self.robot, body = self.data, headers = {'Content-Type': 'application/json'})
        print(self.send.data)

if __name__ == '__main__':
    image = input("请输入本地图片的绝对路径：")
    obj = WorkWeChatRobot(image = image, robot = Robot)
    obj.send_msg()