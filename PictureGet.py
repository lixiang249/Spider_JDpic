# _*_ coding:utf-8 _*_
# author:"xianli"

import re
import os
import urllib.request
from urllib import error


def craw(url, page):
    html1 = urllib.request.urlopen(url).read()  # 打开URL，并且获取网页源码，存储在HTML1中
    html1 = str(html1)
    pat1 = '<div id="plist".+? <div class="page clearfix">'  # 正则表达式，过滤一部分无用源码
    result = re.compile(pat1).findall(html1)  # compile用于对正则表达式进行预编译，findall则是对字符串进行正则匹配
    result = result[0]

    pat2 = '<img width="220" height="220" data-img="1" src="//(.+?\.jpg)">'  # 正则表达式，过滤源代码，得到需要的URL
    imglist = re.compile(pat2).findall(result)
    x = 1

    for imageurl in imglist:
        imagename = "./photo/" + str(page) + "_" + str(x) + ".jpg"
        imageurl = "http://" + imageurl
        try:
            urllib.request.urlretrieve(imageurl, filename=imagename)
            print('{} success!'.format(imagename))
        except error.URLError as e:
            """
              引发URLError异常有四种
              1.连接不上服务器 2.远程URL不存在 3.无网络 4.触发了HTTPError
              URLerror 包含一个 reason的属性
              HTTPerror 包含 code属性和reason属性
                HTTPError code：200-正常 301-重定向到临时的URL 304-请求资源未更新 400-非法请求
                                401-请求未经过授权 403-禁止访问 404-没有找到对应的页面 500-服务器内部出现错误
                                501-服务器不支持现在请求所需要的功能
            """
            if hasattr(e, "code"):  # hasattr(obj,attr)判断对象obj中是否包含有attr属性，有则返回TRUE
                x += 1
            if hasattr(e, "reason"):
                x += 1
        x += 1


def main():
    if not os.path.exists("./photo/"):  # 判断是否存在该目录
        os.makedirs("./photo/")  # mkdir用于创建一级目录  mkdirs用于创建多级目录

    for i in range(1, 20):
        url = "https://list.jd.com/list.html?cat=9987,653,655&page=" + str(i)
        craw(url, i)

main()

