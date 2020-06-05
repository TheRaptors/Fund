#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certifi, datetime
Now = datetime.datetime.now()
Now = Now.strftime('%Y%m%d%H%M%S')

# User-Agent
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

# 防盗链
headers['Referer'] = 'https://www.2meinv.com/'

# 企业微信机器人
import base64, hashlib, json, os, urllib3
robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d9e61993-7cc2-45ea-a64a-65e92e615bbe'

import random, re, requests

class downloadImage(object):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
    def getAllItemsOnThisPage(self):
        try:
            request = requests.get(url = self.url, headers = self.headers)
            content = request.text
            pattern = re.compile('<div class="dl-name">(.*?)<a href="(.*?)" target="_blank">(.*?)</a></div>', re.S)
            result = re.findall(pattern, content)
            self.allItems = []
            for i in result:
                self.allItems.append(i[1])
        except Exception as Error:
            print(Error)
    def randomItem(self):
        self.item = random.choice(self.allItems)
    def getItemMaxImageNum(self):
        try:
            request = requests.get(url = self.item, headers = self.headers)
            content = request.text
            pattern = re.compile('...</a> <a href="(.*?)">(.*?)</a>', re.S)
            result = re.findall(pattern, content)
            for i in result:
                self.maxNum = i[1]
        except Exception as Error:
            print(Error)
    def randomImageUrl(self):
        i = random.randrange(int(self.maxNum))
        if i == 0:
            self.imageUrl = self.item
        else:
            self.imageUrl = self.item[:-5] + '-' + str(i) + self.item[-5:]
    def getImageResourceLink(self):
        try:
            request = requests.get(url = self.imageUrl, headers = self.headers)
            content = request.text
            pattern = re.compile('<a href="(.*?)"><img src="(.*?)" alt="(.*?)" title="" /></a>', re.S)
            result = re.findall(pattern, content)
            for i in result:
                self.imageResourceLink = i[1]
        except Exception as Error:
            print(Error)
    def downloadAsLocalImage(self):
        fileType = self.imageResourceLink.split('.')[-1]
        fileName = Now + '.' + fileType
        try:
            request = requests.get(url = self.imageResourceLink, headers = self.headers)
            with open(fileName, 'wb') as f:
                f.write(request.content)
            self.fileName = fileName
            return self.fileName
        except Exception as Error:
            print(Error)
    def doing(self):
        self.getAllItemsOnThisPage()
        self.randomItem()
        self.getItemMaxImageNum()
        self.randomImageUrl()
        self.getImageResourceLink()
        #self.downloadAsLocalImage()

class WorkWeChatrobot(object):
    def __init__(self, image, robot):
        self.image = image
        self.robot = robot
    def get_info(self):
        with open(self.image, 'rb') as f:
            fr = f.read()
            self.image_md5 = hashlib.md5(fr).hexdigest()
            self.image_base64 = base64.b64encode(fr)
    def sendMessage(self):
        self.get_info()
        self.data = json.dumps({"msgtype": "image", "image": {"base64": self.image_base64.decode(), "md5": self.image_md5}})
        self.http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())
        self.send = self.http.request(method = 'POST', url = self.robot, body = self.data, headers = {'Content-Type': 'application/json'})
        print(self.send.data)


if __name__ == "__main__":
    i = random.randrange(500)
    if i == 0:
        url = 'https://www.2meinv.com/'
    else:
        url = 'https://www.2meinv.com/index-%d.html' % (i + 1)
    obj = downloadImage(url = url, headers = headers)
    obj.doing()
    localImage = obj.downloadAsLocalImage()
    Obj = WorkWeChatrobot(image = localImage, robot = robot)
    Obj.sendMessage()