# 新浪微博签到页爬虫

[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()

## 1.功能简介
以城市为单位爬取新浪微博移动端POI下的所有微博，存入对应csv文件。爬取的信息有：
信息 | 含义
:-: | :-:
user_id | 用户ID
user_name | 昵称
gender | 性别
tweets | 微博文本
textLength | 微博文本长度
created_at | 发布时间
source | 发布端
followers_count | 粉丝数
follow_count | 关注数
statuses_count | 历史微博数
profile_url | 主页链接
pic_num | 图片数
pics_url | 图片链接
reposts_count | 转发数
comments_count | 评论数
attitudes_count | 态度数

## 2.文件说明
buildip.py，爬取 [西刺高匿代理](https://www.xicidaili.com/nn/) 构建代理池。  
myemail.py，爬取完毕后发邮件给自己的邮箱。  
wifi.py，确保网络连接不断开（网络断开后自动重连）。  
crawler.py，爬虫本体。  
**config.ini**，配置文件，配置项有邮箱，wifi名称，城市名称，城市编码。

## 3.程序思路
爬取网站为 [新浪微博移动端](https://m.weibo.cn) ，相对于PC端而言网页结构简单而且限制较少，而且签到页不需要模拟登录。

首先，爬取城市页面，比如武汉市的url为： https://m.weibo.cn/p/1001018008642010000000000  ，获取城市下的所有POI，写入<cityName>.csv文件。   

然后，读取生成的csv文件读出POI的name和id，再构造url爬取POI下的微博信息，url示例： https://m.weibo.cn/p/index?containerid=100101B2094655D464A3FF439C
![SinaWeibo Mobile 武汉市](http://qab3yd0rl.bkt.clouddn.com/%E6%AD%A6%E6%B1%89%E5%B8%82.png)
![SinaWeibo Mobile 黄鹤楼](http://qab3yd0rl.bkt.clouddn.com/%E9%BB%84%E9%B9%A4%E6%A5%BC.png)

## 4.使用方法
修改config.ini文件，email_address填写自己的邮箱，wifi填写已连接过的wifi名称，cityName填写爬取的城市名称，cityId填写城市编码。

城市编码参考新浪微博开放平台的 [省份城市编码表](https://open.weibo.com/wiki/%E7%9C%81%E4%BB%BD%E5%9F%8E%E5%B8%82%E7%BC%96%E7%A0%81%E8%A1%A8)， 举例如下：湖北省的省份编码为42，武汉市编码为1，则武汉市的编码为4201。值得注意的一点是：北京、上海、天津、重庆四个直辖市的编码后两位均为0，不再继续向下区分，北京市：1100，例如北京海淀区对应代码为1108，爬取不到内容。

## 5.依赖的第三方库
- **requests**    
- **pandas**  
- **configparser**  
- **fake_useragent**  

## 6.Contact Me
如果有什么建议，欢迎联系我 zixinwan@foxmail.com 或提issue。欢迎star!
