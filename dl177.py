#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-
__author__ = 'wudaown'

#
#   应朋友要求做了一个脚本从 www.177pic.info/ 下载所有中文漫画
#   已经挂服务器上面慢慢跑了，没有上面用处，一次性的东西
#

import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
import io
import sys
import re
from requests import Request, Session
import argparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
sourceHost = 'www.177pic.info'
# sourceHost = 'pic177.com'
rootPath = ''
recodeFileName = 'recode'

proxies = {
  # 'http': 'http://127.0.0.1:10910',
  # 'https': 'http://127.0.0.1:10910',
     'http': 'http://127.0.0.1:1081',
  #   'https': 'https://192.168.2.100:8888',
  #  'http': 'socks5://127.0.0.1:10910',
  #  'https': 'socks5://127.0.0.1:10910',
}

def getSource(url):     # 读取完整页面 返回一个漫画名称和下载地址的mapping
    r = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(r.text,'lxml')
    link = soup.find_all('h2')  # bs4 找 h2 tag
    dl = []
    title = []
    for x in link:
        try:
            title.append(x.contents[0]['title'][13:]) # h2 tag 下还有其他tag读取内容
            dl.append(x.contents[0]['href'])
        except Exception as e:
            print ("error happened")
    comic = dict(zip(dl,title))
    return(comic)

def getSourceName(url):     # 读取完整页面 返回一个漫画名称和下载地址的mapping
    r = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(r.text,'lxml')
    link = soup.find_all('h1')  # bs4 找 h1 tag
    for x in link:
        return x.contents[0]
    return('')

def getPageNumber(page_url):    # 通过下载地址判断一共有多少页
    allPage = []
    p = requests.get(page_url, proxies=proxies)
    pagesoup = BeautifulSoup(p.text,'lxml')
    page = pagesoup.find(attrs={'class':'wp-pagenavi'}) # 直接查找attrs判断页面
    if page == None:    # 如果page值为空则返回默认页面
        number_of_page = 0
        allPage.append(page_url)
        return allPage
    else:
        number_of_page = int(page.contents[0].contents[-3].string)  # page不为空时返回多少页面
        for i in range(number_of_page):
            allPage.append(page_url+'/'+str(i+1))
        return allPage


def getImglink(page):       # 去的图片直链
    imgdr = []
    p = requests.get(page, proxies=proxies)
    imgsoup = BeautifulSoup(p.text,'lxml')
    imglink = imgsoup.findAll('img')    # 找html中所有图片
    for y in imglink:
        if 'alt' in y.attrs:        # 剔除没有编号的图片
            imgdr.append(y['src'])
    return  imgdr



def downloadComic(comic_link):      # 下载图片
    imglist = []
    comic_page = getPageNumber(comic_link)
    for x in comic_page:
        tmp = getImglink(x)
        for y in tmp:
            imglist.append(y)
    cnt = 0
    sumImages = len(imglist)
    for z in range(sumImages):      # 用range是因为要重命名图片为后面打包做准备
        fileName = str(z).zfill(3) + '.jpg'
        img = requests.get(imglist[z-1], proxies=proxies)
        with open(fileName, 'wb') as f: # 图片wb模式写入 binary
            f.write(img.content)
            cnt += 1
            print('\r', end="", flush=True)
            print(str(cnt).rjust(3, ' ') + '/' + str(sumImages), end="", flush=True)
    os.chdir('..')
    print('')

def getSourcePageNumber():
    url = 'http://' + sourceHost + '/html/category/tt/page/1'
    source = requests.get(url, proxies=proxies)
    sourcesoup = BeautifulSoup(source.text,'lxml')
    sourcepage = sourcesoup.find(attrs={'class':'wp-pagenavi'})
    source_page_number = int(sourcepage.contents[-2]['href'].split('/')[-1])
    return source_page_number


def main(): # main 模块
    recode = ''
    if os.path.exists(recodeFileName) == False:
        print('第一次运行，建立页面记录')
        os._exists(recodeFileName)
        # os.popen('touch recode')    # 判断是否首次执行脚本
        with open (recodeFileName,'w') as f:
            recode = '/html/category/tt/page/1'
            f.write(recode)
    else:
        print('读取上次停止下载页面')
        with open(recodeFileName,'r') as f:
            trecode = f.readline().replace('\n','')  # 读取记录
            recode = trecode.split('/')
            print('上次停止在第{0}页'.format(recode))
    url = 'http://' + sourceHost +'/html/category/tt'
    total_page = getSourcePageNumber()
    url_list = []
    for i in range(int(recode[-1]), total_page + 1):    # 根据记录选择开始页面
        url_list.append(url+'/page/'+str(i))
    # tmp = os.popen('ls').readlines()
    tmp = os.listdir(rootPath)
    allcomic = []
    for i in tmp:
        allcomic.append(i) # 读取目录列表，保存以便判断漫画是否下载
    del tmp
    for y in url_list:
        print('正在下载: ',y)
        with open(recodeFileName,'w') as f:
            wrotePart = ""
            yParts = y.split('/')
            for i in range(len(yParts)):
                if i == 0 or i == 1:
                    continue;
                else:
                    wrotePart += "/" + yParts[i]
            f.write(wrotePart)
        comic = getSource(y)
        while(len(comic) <= 0):
            print ("comic list should not be 0, retry")
            comic = getSource(y)
        print('下载列表:',comic)

        for x in comic:
            if (x != "http://www.177pic.info/html/2013/11/10659.html"):
                continue;
            comic[x] = cleanName(comic[x])
            # print(comic[x],end=' ')
            # print((comic[x]+'.cbr'  in allcomic))
            if ((comic[x]+'.cbr') in allcomic) == True:
                print(comic[x],'.cbr已经存在。')
            else:
                if (comic[x] in allcomic) == True: #匹配图片数量跟文件名上的数量是不是一样,一样就不需要重新下载
                    resultList = re.findall(r'([\d]*)P', comic[x])
                    imageCntInTitle = int(resultList[-1])
                    dir = os.path.join(rootPath, comic[x])
                    imageCnt = len(os.listdir(dir))
                    if(imageCnt == imageCntInTitle):
                        print(comic[x] + "无需重复下载")
                        if (os.name != 'nt'):
                            command = 'rar a -r -s -m5\'' + comic[x] + '.cbr\' \'' + comic[x] + '\''
                            os.system(command)
                        continue
                print('正在下载: ',comic[x])
                if (os.path.exists(comic[x])) == True:
                    print('目录已经存在。')
                    os.chdir(comic[x])
                    downloadComic(x)
                    if (os.name != 'nt'):
                        command = 'rar a -r -s -m5\''+comic[x]+'.cbr\' \''+comic[x]+'\'' # -df deleted because we need remain the folder
                        os.system(command)
                    # os.system('clear')
                else:
                    os.mkdir(comic[x])
                    os.chdir(comic[x])
                    downloadComic(x)
                    if(os.name != 'nt'):
                        command = 'rar a -r -s -m5\''+comic[x]+'.cbr\' \''+comic[x]+'\''  # -df deleted because we need remain the folder
                        os.system(command)
                    # os.system('clear')

def cleanName(arbitrary_string): #windows has some invalid charater in directory or filename should be removed
    # arbitrary_string = "File!name?.txt"
    cleaned_up_filename = re.sub(r'[/\\:*?"<>|]', '', arbitrary_string)
    # filepath = os.path.join("/tmp", cleaned_up_filename)
    return cleaned_up_filename

def downloadComic1(comic_link):
    print("downloadComic1 running successfully");

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def getExistedComicPacks():
    tmp = os.popen('ls').readlines()
    allcomic = []
    for i in tmp:
        allcomic.append(i) # 读取目录列表，保存以便判断漫画是否下载
    return allcomic

def downloadSingleComic(url):
    comicName = cleanName(getSourceName(url))
    allcomic = getExistedComicPacks();
    if ((comicName + '.cbr') in allcomic) == True:
        print(comicName, '.cbr已经存在。')
        return
    else:
        print('正在下载: ', comicName)
        if (os.path.exists(comicName)) == True:
            print('目录已经存在。')
            os.chdir(comicName)
            downloadComic(url)
            if (os.name != 'nt'):
                command = 'rar a -r -s -m5\'' + comicName + '.cbr\' \'' + comicName + '\''
                os.system(command)
        else:
            os.mkdir(comicName)
            os.chdir(comicName)
            downloadComic(url)
            if (os.name != 'nt'):
                command = 'rar a -r -s -m5\'' + comicName + '.cbr\' \'' + comicName + '\'' # -df deleted because we need remain the folder
                os.system(command)
        print(os.path.join(rootPath, comicName + '.cbr'))

if __name__ == '__main__':
    # comicName = '[クリムゾン] JK強制操作 -スマホで長期間弄ばれた風紀委員長-【完全版】 [中国翻訳]'
    # command = 'rar a -r -s -m5 -df \'' + comicName + '.cbr\' \'' + comicName + '\''
    # print(command)
    # print(cur_file_dir())

    # connect via socks
    # print(requests.get('http://ipip.net', proxies=proxies).text)


    rootPath = os.path.join(cur_file_dir(), 'all')
    if (os.path.exists(rootPath)) == False:
        os.mkdir(rootPath)
    os.chdir(rootPath)

    newParser = argparse.ArgumentParser();
    newParser.add_argument("-u", "--url", type=str, help="put the target url")
    newParser.add_argument("-H", "--host", type=str, help="put the source host. eg: 177pic.com")
    newParser.add_argument("-R", "--reset", action='store_true', help="delete the recode file and restart downloading")
    newParser.add_argument("-P", "--part", type=str, help="Specify the recode part number") #多个脚本开启,使用的recode文件
    args = newParser.parse_args()


    if args.part:
        recodeFileName += args.part
        print ("recode as:" + recodeFileName)
    if args.reset:
        if os.path.exists(recodeFileName):
            os.remove(recodeFileName)
            print('reset the record successfully')
    if args.host:
        if "http://" in str(args.host) or "https://" in str(args.host):
            print("host should not contain http://")
        sourceHost = args.host
        exit(-1)
    if args.url:
        val = URLValidator()
        try:
            val(args.url)
        except ValidationError as e:
            print("url validation failed, try another one")
            sys.exit(-1)
        print("Download with url: " + args.url)
        downloadSingleComic(args.url)
    else:
        print("Running in full website download mode")
        main()