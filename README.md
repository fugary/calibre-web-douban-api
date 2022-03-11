# calibre-web-douban-api

新版calibre-web已经移除douban-api了，而且把从get_meta.js中直接发起请求获取数据改成了从服务端使用python获取数据。

此项目是添加一个豆瓣api provider实现，需要放到metadata_provider目录下

### 使用方法

复制`src/NewDouban.py`到`calibre-web/cps/metadata_provider/`目录下，重启项目即可。

此应用是基于Python抓取网页的形式获取书籍信息，频率过高访问可能被屏蔽。

参考文档：https://fugary.com/?p=238

**新版calibre-web 0.6.17以上使用**

小于0.6.17版本，请下载：https://github.com/fugary/calibre-web-douban-api/releases/tag/0.6.16



