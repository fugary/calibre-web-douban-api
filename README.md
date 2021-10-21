# calibre-web-douban-api

新版calibre-web已经移除douban-api了，而且把从get_meta.js中直接发起请求获取数据改成了从服务端使用python获取数据。

此项目是添加一个豆瓣api provider实现，需要放到metadata_provider目录下，调用simple-boot-douban-api服务

### 使用方法

复制`src/douban.py`到`calibre-web/cps/metadata_provider/`目录下，重启项目。

**注意：由于豆瓣api已经不开放使用了，这个豆瓣api需要连接`simple-boot-douban-api`使用**

