## 说明

从某网站下载所有中文漫画，下载完自动打包成cbr漫画格式。

Mac下可以通过DrawnStrip Reader阅读。

Linux推荐Comix。


## 依赖

需要

python3.5

rar 

lxml 

beautifulsoup

``` bash
brew install homebrew/binary/rar 
pip3.5 install lxml
pip3.5 install beautifulsoup4
pip3.5 install requests[socks]
pip3.5 install argparse
pip3.5 install django
```

For Windows

Before install pip components, you should install VS compile environment. You can install VS 2015 or install from http://download.microsoft.com/download/5/f/7/5f7acaeb-8363-451f-9425-68a90f98b238/visualcppbuildtools_full.exe


``` bash
set STATICBUILD=true && pip install lxml
pip3.5 install beautifulsoup4
pip3.5 install requests[socks]
pip3.5 install argparse
pip3.5 install django
```

## 使用

``` bash
chmod +x 177dl.py
./177dl.py
```

然后就慢慢等吧。
