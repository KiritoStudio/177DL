## 说明

从某网站下载所有中文漫画，下载完自动打包成cbr漫画格式。

Mac下可以通过DrawnStrip Reader阅读。

Linux推荐Comix。



## 依赖

需要

python3.4

rar 

lxml 

beautifulsoup

``` bash
brew install homebrew/binary/rar
pip install lxml
pip install beautifulsoup4
pip install requests[socks]
pip install django
```

For Windows

``` bash
set STATICBUILD=true && pip install lxml
pip install beautifulsoup4  
pip install requests[socks]
pip install django
```

## 使用

``` bash
chmod +x 177dl.py
./177dl.py
```

然后就慢慢等吧。