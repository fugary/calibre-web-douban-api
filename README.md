# calibre-web-douban-api

新版calibre-web已经移除douban-api了，而且把从get_meta.js中直接发起请求获取数据改成了从服务端使用python获取数据。

此项目是添加一个豆瓣api provider实现，需要放到metadata_provider目录下

### 使用方法（新）

复制`src/NewDouban.py`到`calibre-web/cps/metadata_provider/`目录下，重启项目即可。

此应用是基于Python抓取网页的形式获取书籍信息，频率过高访问可能被屏蔽。

### 使用方法（已废弃）

~~修改`src/douban.py`中的`doubanUrl`地址后，复制`src/douban.py`到`calibre-web/cps/metadata_provider/`目录下，重启项目。~~

~~由于豆瓣api已经不开放使用了，这个豆瓣api需要连接`simple-boot-douban-api`使用~~



