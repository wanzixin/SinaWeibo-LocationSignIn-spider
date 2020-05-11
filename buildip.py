# code: utf-8
# version: python3.7
# author: Zixin Wan

import requests
import re
import time
import random
from fake_useragent import UserAgent

class Proxies:
    def __init__(self):
        self.proxy_list = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/45.0.2454.101 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate, sdch',
        }

    # 爬取西刺高匿代理
    def get_proxy(self,page):
        proxy_list = []
        proxy_ip = {}

        if self.proxy_list:            
            proxy_ip = random.choice(self.proxy_list)
        else:
            proxy_ip = {'http':'223.241.119.42:47972'}

        print('----------------爬取代理使用的ip为: ',proxy_ip,'--------------------')

        url = 'https://www.xicidaili.com/nn/' + str(page)

        res = requests.get(url,proxies=proxy_ip,headers = {'User-Agent': UserAgent(use_cache_server=False).random})
        if res.status_code == 200:
            ip_list = []
            port_list = []
            ip_list = (re.findall(r'\d+\.\d+\.\d+\.\d+',res.text))
            port_list = (re.findall(r'\d{3,5}',res.text))

            for ip,port in zip(ip_list,port_list):                
                proxy_list.append(ip + ':' + port)

        return proxy_list

    # 验证代理是否可用，并添加入成员变量proxy_list
    def verify_proxy(self,proxy_list):
        t1 = time.perf_counter()

        for index,proxy in enumerate(proxy_list):
            try:                
                if requests.get('https://www.baidu.com',proxies={'http':proxy},timeout=3).status_code == 200:
                    print('这是第 {} 个代理， '.format(index) + proxy + ' is useful')          
            except:
                print('正在测试下一个代理，请稍后……')
            finally:
                if proxy not in self.proxy_list:
                    self.proxy_list.append(proxy)
        
        t2 = time.perf_counter()
        print('测试代理可用性总耗时 %f 秒。'%(t2-t1))

    # 保存到ippool这个list里
    def save_proxy(self):
        ippool = []
        for proxy in self.proxy_list:
            proxies = {'http':proxy}
            ippool.append(proxies)
        return ippool

# 使用上面的类建立代理池
def build_ippool():
    p = Proxies()
    results = []

    page = random.randint(1,1000)

    results = p.get_proxy(page)
    print('爬取到的代理数量: ',len(results))
    print('---------------------------------------------\n开始验证……')

    p.verify_proxy(results)
    print('验证完毕，可用代理数量为: ',len(p.proxy_list))

    ippool = p.save_proxy()

    return ippool

if __name__ == '__main__':
    build_ippool()  