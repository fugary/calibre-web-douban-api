# calibre-web-douban-api

**2023-07-15**

最新豆瓣屏蔽直接访问封面图片，自动实现使用本地代理封面图片，保存时使用requests下载并保存

**2022-10-08**

原douban列表url被屏蔽，老版本不能访问，建议更新最新的[NewDouban.py](https://github.com/fugary/calibre-web-douban-api/releases/latest)

**2022-08-10**

**最新V0.6.19版本的calbire-web的豆瓣插件已经回来了，除了标签外，应该都有数据了，可以不用此插件了**

新版calibre-web已经移除douban-api了，而且把从get_meta.js中直接发起请求获取数据改成了从服务端使用python获取数据。

此项目是添加一个豆瓣api provider实现，需要放到metadata_provider目录下

### 使用方法

复制`src/NewDouban.py`到`calibre-web/cps/metadata_provider/`目录下，重启项目即可。

此应用是基于Python抓取网页的形式获取书籍信息，频率过高访问可能被屏蔽。

参考文档：https://fugary.com/?p=238

**新版calibre-web 0.6.17以上使用**

小于0.6.17版本，请下载：https://github.com/fugary/calibre-web-douban-api/releases/tag/0.6.16



