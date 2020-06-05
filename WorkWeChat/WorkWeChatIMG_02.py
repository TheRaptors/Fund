#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certifi, datetime
Now = datetime.datetime.now()
Format_Now = Now.strftime('%Y%m%d%H%M%S')

# User-Agent
Headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

# 防盗链
Headers['Referer'] = 'https://www.meitulu.com/t/ugirls/'

# 企信
import base64, hashlib, json, os, urllib3
Robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d9e61993-7cc2-45ea-a64a-65e92e615bbe'

# ugirls
import random, re, requests

class DownloadImage(object):
    def __init__(self, url):
        self.url = url
    def get_pages(self):
        # 获取所有页面URl
        try:
            Request = requests.get(url = self.url, headers = Headers)
            Content = Request.text
            Pattern_Pages = re.compile('<center>(.*?)</center>', re.S)
            Pages = re.findall(Pattern_Pages, Content)
            Pattern_Page = re.compile('<a href="(.*?)"', re.S)
            Page = re.findall(Pattern_Page, Pages[0])
            self.Pages = Page
            #return self.Pages
        except Exception as e:
            print(e)
    def random_page(self):
        # 随机获取任意页面URL
        self.Page = random.choice(self.Pages)
    def get_items(self):
        # 获取所有item
        try:
            Request = requests.get(url = self.Page, headers = Headers)
            Content = Request.text
            Pattern_Items = re.compile('<p class="p_title"><a href="(.*?)" target="_blank">', re.S)
            Items = re.findall(Pattern_Items, Content)
            self.Items = Items
            #return self.Items
        except Exception as e:
            print(e)
    def random_item(self):
        # 随机获取任意item
        self.Item = random.choice(self.Items)
    def get_images(self):
        # 获取所有图片URL
        try:
            Request = requests.get(url = self.Item, headers = Headers)
            Content = Request.text
            Pattern_Images = re.compile('<center>(.*?)</center>', re.S)
            Images = re.findall(Pattern_Images, Content)
            Pattern_Image = re.compile('<img src="(.*?)"', re.S)
            Image = re.findall(Pattern_Image, Images[0])
            self.Images = Image
            #return self.Images
        except Exception as e:
            print(e)
    def random_image(self):
        # 获取任意图片URL
        self.Image = random.choice(self.Images)
        #return self.Image
    def download_image(self):
        File_Type = self.Image.split('.')[-1]
        File_Name = Format_Now + '.' + File_Type
        try:
            res = requests.get(self.Image, headers = Headers)
            with open(File_Name, 'wb') as f:
                f.write(res.content)
            self.File_Name = File_Name
            return self.File_Name
        except Exception as e:
            print(e)
    def doing(self):
        self.get_pages()
        self.random_page()
        self.get_items()
        self.random_item()
        self.get_images()
        self.random_image()
        #self.download_image()

class WorkWeChatRobot(object):
    def __init__(self, image, robot):
        self.image = image
        self.robot = robot
    def get_info(self):
        with open(self.image, 'rb') as f:
            fr = f.read()
            self.image_md5 = hashlib.md5(fr).hexdigest()
            self.image_base64 = base64.b64encode(fr)
    def send_msg(self):
        self.get_info()
        self.data = json.dumps({"msgtype": "image", "image": {"base64": self.image_base64.decode(), "md5": self.image_md5}})
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        self.send = self.http.request(method = 'POST', url = self.robot, body = self.data, headers = {'Content-Type': 'application/json'})
        print(self.send.data)

if __name__ == "__main__":
    url = 'https://www.meitulu.com/t/ugirls/'
    Obj1 = DownloadImage(url = url)
    Obj1.doing()
    Local_Image = Obj1.download_image()
    Obj2 = WorkWeChatRobot(image = Local_Image, robot = Robot)
    Obj2.send_msg()
