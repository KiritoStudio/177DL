## 说明

从某网站下载所有中文漫画

可以在局域网NAS下流畅阅读

## 依赖

需要

python3.5

lxml 

beautifulsoup

## For Windows

Before install pip components, you should install VS compile environment. You can install VS 2015 or install from http://download.microsoft.com/download/5/f/7/5f7acaeb-8363-451f-9425-68a90f98b238/visualcppbuildtools_full.exe


``` bash
set STATICBUILD=true && pip install lxml
pip3.5 install beautifulsoup4
pip3.5 install requests[socks]
pip3.5 install argparse
pip3.5 install django
```

## Linux使用

``` bash
pip3.5 install lxml
pip3.5 install beautifulsoup4
pip3.5 install requests[socks]
pip3.5 install argparse
pip3.5 install django

chmod +x 177dl.py
./177dl.py
```

## 多进程下载方式

先跑一下dl177.py，会自动创建一个recode文件，更改文件最后的页码，然后修改文件名为recodeX，再跑dl177.py -P X，实现分段下载（X代表你的进程序号，比如0，1，2）
eg: 177dl.py -P 0 0对应的是对应的recode0文件
你可以写一个脚本文件一次确定多个进程实现分段下载

然后就慢慢等吧。
