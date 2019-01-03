#-*-coding:utf-8-*-
#python3.6
#author :shen
#date :2019/1/3
import requests
from bs4 import BeautifulSoup as bs
from requests import Session
from urllib.request import urlretrieve
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
class Login():
    def __init__(self):
        self.s = Session()
    def get_html(self,url):
        """
        得到HTML网页
        :param url: 网址Url
        :return: 网页
        """
        html = self.s.get(url)
        html.encoding = 'utf-8'
        return html.text
    def get_imghash(self,html):
        """

        :param html:得到的网页
        :return: 返回imghash字符串
        """
        data = bs(html,'lxml')
        inputs = data.select('input')
        dic = {}
        for input in inputs:
            dic[input.get('name')]=input.get('value')
        return dic['imagehash']
    def get_image(self,html):
        """

        :param html:
        :return:验证码图片链接
        """
        data = bs(html, 'lxml')
        imgs = data.select('img')
        for img in imgs:
            img = img.get('src')
            if 'imagehash' in img:
                return 'https://bt.byr.cn/'+img
        return None
    def indexLogin(self):
        """

        :return:imghash字符串
        """
        loginUrl = 'https://bt.byr.cn/login.php'
        html = self.get_html(loginUrl)
        imghash = self.get_imghash(html)
        imgUrl = self.get_image(html)
        imgPath = 'cap.jpg'
        urlretrieve(imgUrl,imgPath)
        return imghash
    def TakeLogin(self):
        imghash = self.indexLogin()
        src = 'cap.jpg'
        imagestring = self.cap_rec(src)
        print(imagestring)
        if input('验证码是否正确？（Y/N）：') !='Y':
            return False
        data = {
            'username':'你的账户',
            'password':'密码',
            'imagestring':imagestring,
            'imagehash':imghash
        }
        takeUrl = 'https://bt.byr.cn/takelogin.php'
        self.s.post(takeUrl,data = data)
        return True
    def get_torrent(self):
        url = 'https://bt.byr.cn/torrents.php'
        html = self.s.get(url)
        html.encoding = 'utf-8'
        print(type(bs(html.text,'lxml').prettify()))
        with open('result.html','w',encoding='utf-8') as f:
            f.write(bs(html.text,'lxml').prettify())
    def cap_rec(self,src):
        img = Image.open(src)
        img = img.convert('L')
        arr = np.array(img)
        for x in range(arr.shape[0]):
            for y in range(arr.shape[1]):
                if x == 0 or x == arr.shape[0] - 1 or y == 0 or y == arr.shape[1] or arr[x][y] != 0:
                    arr[x][y] = 255
        for x in range(1, arr.shape[0] - 1):
            for y in range(1, arr.shape[1] - 1):
                if arr[x][y] == 0 and arr[x - 1][y] != 0 and arr[x + 1][y] != 0 and arr[x][y - 1] != 0 and arr[x][
                    y + 1] != 0:
                    arr[x][y] = 255
        # arr = arr[13:26,:]
        image = Image.fromarray(arr.astype('uint8')).convert('L')
        image.save('cap1.jpg')
        str = pytesseract.image_to_string(image)
        return str
def main():
    login = Login()
    if login.TakeLogin():
        login.get_torrent()
if __name__ == '__main__':
   main()
