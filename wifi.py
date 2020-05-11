import os
import subprocess
import time
import configparser

def read_ini(inipath='config.ini'):
    config = configparser.ConfigParser()
    config.read(inipath,encoding='utf-8')
    wifiName=config.get('WIFI','wifi')
    return wifiName

def connect_wifi(wifiName):
    # os.system('start netsh wlan connect name=%s' % wifiName)

    child = subprocess.Popen('netsh wlan connect name=%s' % wifiName)
    exit_code = subprocess.Popen.poll(child)
    if exit_code == None:
        time.sleep(1)
    elif exit_code == 0:
        print('wifi成功连接')

    # child.wait()

def disconnect_wifi():
    os.system('netsh wlan disconnect')

def network_detection():
    # exit_code = os.system('start ping https://www.baidu.com') # 加start不阻塞父进程
    childProcess = subprocess.Popen('ping www.baidu.com -n 2')
    exit_code = childProcess.wait()
    if exit_code:
        return False
    else:
        return True

def make_network_ok():
    if network_detection():
        pass
    else:
        wifiName=read_ini()
        connect_wifi(wifiName)

if __name__ == '__main__':
    make_network_ok()
