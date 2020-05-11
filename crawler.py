# code: utf-8
# version: python3.7
# author: Zixin Wan

import random
import requests
import json
import time
import re
import os
import pandas as pd
import configparser
from fake_useragent import UserAgent
from buildip import build_ippool
from myemail import Email
from wifi import make_network_ok

class SinaCrawler(object):
    def __init__(self,cityInfo):
        self.cityInfo = cityInfo
        self.user_id = []
        self.user_name = []
        self.gender = []
        self.tweets = []
        self.textLength = []
        self.created_at = []
        self.source = []    
        self.followers_count = []
        self.follow_count = []
        self.statuses_count = []
        self.profile_url = []
        self.pic_num = []
        self.pics_url = []
        self.reposts_count = []
        self.comments_count = []
        self.attitudes_count = []
    
    # 获取武汉市（编码：4201）的推荐poiid，并写入 <cityName>-poiid.csv
    # cityInfo = {'name':'武汉市','cid':4201}
    def get_poi(self,ippool):
        cityURL = 'https://m.weibo.cn/api/container/getIndex?containerid=10010180086'+str(self.cityInfo['cityId'])+'0000000000_-_poilist'
        pois_name = []
        pois_id = []

        for page in range(1,10):
            # 每次更换代理与请求头
            proxy_ip = random.choice(ippool)
            headers ={'User-Agent': UserAgent(use_cache_server=False).random}

            res = requests.get(cityURL+'&page='+str(page),proxies = proxy_ip,headers = headers)
            if res.status_code == 200:
                info = json.loads(res.text)

                if info['ok'] == 1:
                    card_group = info['data']['cards'][0]['card_group']
                    
                    for i in range(0,len(card_group)):
                        poi_id = re.search(r'100101B2094[A-Z0-9]{15}',card_group[i]['scheme'])
                        pois_id.append(poi_id.group())
                        pois_name.append(card_group[i]['title_sub'])
                else:
                    print('这座城市poi已经爬取完毕了。')
        
        df = pd.DataFrame({
            'poiname':pois_name,
            'poiid':pois_id
        })

        mkdir('cityPOI')
        df.to_csv('cityPOI/'+self.cityInfo['cityName']+'poi.csv',sep=',',index=False)
        print('cityPOI/'+self.cityInfo['cityName']+'poi.csv文件已生成。')


    def get_tweets(self,URL,page,ippool):    
        # 每次更换代理与请求头
        proxy_ip = random.choice(ippool)
        headers ={'User-Agent': UserAgent(use_cache_server=False).random}

        res = requests.get(URL,proxies=proxy_ip,headers=headers)
        # print('----------------------------------------------------')
        print('状态码为：',str(res.status_code))
        print('请求头为： ',headers['User-Agent'])
        print('代理为： ',proxy_ip['http'])
        print('url: ',URL)
        
        ok=''
        if res.status_code == 200:    
            # 将获取到的文件转为json
            info = json.loads(res.text)

            ok = info['ok']
            if ok == 1:
                pass
            else:
                return
            cards = info['data']['cards']
            cardsLength = len(cards)
            card_group = {}  

            # page=1时从下标1开始，page>=2时下标从0开始，坑：有的地点第一页的cards长度只有1
            if page == 1 and cardsLength == 2:
                card_group = cards[1]['card_group']
            elif cardsLength == 1:
                card_group = cards[0]['card_group']
            else:
                return

            num = len(card_group)
            for i in range(num):
                print('本页共有',num,'条微博，正在爬取本页第',i+1,'条……')

                if 'mblog' in card_group[i]:
                    self.user_id.append(card_group[i]['mblog']['user']['id'])
                    self.user_name.append(card_group[i]['mblog']['user']['screen_name'])
                    self.gender.append(card_group[i]['mblog']['user']['gender'])
                    self.tweets.append(card_group[i]['mblog']['text'])
                    self.textLength.append(card_group[i]['mblog']['textLength'])
                    self.created_at.append(card_group[i]['mblog']['created_at'])                    
                    self.source.append(card_group[i]['mblog']['source'])
                    self.followers_count.append(card_group[i]['mblog']['user']['followers_count'])
                    self.follow_count.append(card_group[i]['mblog']['user']['follow_count'])
                    self.statuses_count.append(card_group[i]['mblog']['user']['statuses_count'])
                    self.profile_url.append(card_group[i]['mblog']['user']['profile_url'])

                    picNum=card_group[i]['mblog']['pic_num']
                    self.pic_num.append(picNum)

                    self.reposts_count.append(card_group[i]['mblog']['reposts_count'])
                    self.comments_count.append(card_group[i]['mblog']['comments_count'])
                    self.attitudes_count.append(card_group[i]['mblog']['attitudes_count'])

                    picurl = ''
                    if picNum and 'pics' in card_group[i]['mblog']:
                        # 坑：len(card_group[i]['mblog']['pics'])和picNum不一定相等
                        for j in range(len(card_group[i]['mblog']['pics'])):                    
                            picurl = picurl + card_group[i]['mblog']['pics'][j]['url'] + ';'
                    else:
                        picurl = 'no picture'
                    self.pics_url.append(picurl)   

                else:
                    print('到底啦～看看其他地点吧')

        else:
            print('------------避免出现418，暂停十秒再爬取--------------')
            time.sleep(10)
            # 更新ip池
            ippool = build_ippool()
        
        # 降低爬取频率
        time.sleep(2.5)
        return ok


    # 从csv文件中读取poiid和poiname
    def get_poiInfo(self,filepath):
        poiids=[]
        poinames=[]
        csv = pd.read_csv(filepath)
        for poiid in csv['poiid']:
            poiids.append(poiid)
        for poiname in csv['poiname']:
            poinames.append(poiname)

        return poiids,poinames

    def clearList(self):
        self.user_id.clear()
        self.user_name.clear()
        self.gender.clear()
        self.tweets.clear()
        self.textLength.clear()
        self.created_at.clear()
        self.source.clear()
        self.followers_count.clear()
        self.follow_count.clear()
        self.statuses_count.clear()
        self.profile_url.clear()
        self.pic_num.clear()
        self.pics_url.clear()
        self.reposts_count.clear()
        self.comments_count.clear()
        self.attitudes_count.clear()

    def savePOIcsv(self,poiname):
        df = pd.DataFrame({
            'user_id':self.user_id,
            'user_name':self.user_name,
            'gender':self.gender,
            'tweets':self.tweets,
            'textLength':self.textLength,
            'created_at':self.created_at,
            'source':self.source,
            'followers_count':self.followers_count,
            'follow_count':self.follow_count,
            'statuses_count':self.statuses_count,
            'profile_url':self.profile_url,
            'pic_num':self.pic_num,
            'pics_url':self.pics_url,
            'reposts_count':self.reposts_count,
            'comments_count':self.comments_count,
            'attitudes_count':self.attitudes_count
        })
        mkdir('tweets')
        mkdir(self.cityInfo['cityName'])
        df.to_csv('tweets/'+self.cityInfo['cityName']+'/'+poiname+'.csv',sep=',',index=False)

def mkdir(dirpath):
    # 若 dirpath 文件夹不存在则创建，若存在就不做操作
    if os.path.exists(dirpath):
        pass
    else:
        os.mkdir(dirpath)

def read_ini(inipath='config.ini'):
    config = configparser.ConfigParser()
    config.read(inipath,encoding='utf-8')
    cityName=config.get('parameter','cityName')
    cityId=config.get('parameter','cityId')
    return {'cityName':cityName,'cityId':cityId}

def main():
    startTime = time.perf_counter()
    ippool = build_ippool()
    
    #cityInfo={'cityName':'北京市','cityId':1100} # 写进config文件
    cityInfo=read_ini()
    spider=SinaCrawler(cityInfo)
    spider.get_poi(ippool)
    filepath='cityPOI/'+cityInfo['cityName']+'poi.csv'
    poiids,poinames=spider.get_poiInfo(filepath)

    for poiid,poiname in zip(poiids,poinames):
        page=1 # 记录当前爬取微博的页数
        while True:
            make_network_ok()
            print('------------------POI： '+poiname+',第',page,'页------------------')
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=%s_-_weibofeed&page=%d'%(poiid,page)
            spider.get_tweets(url,page,ippool)
            page+=1
        spider.savePOIcsv(poiname)
        spider.clearList()
    
    endTime = time.perf_counter()
    em = Email()
    em.send('微博已爬取完成！爬取过程总共 %.3f 分钟。'%(float)((endTime-startTime)/60))

if __name__ == "__main__":
    main()