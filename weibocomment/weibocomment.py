# -*- coding: utf-8 -*-

import requests
import time
import os
import csv
import random
import json

from bokeh.core.json_encoder import pd
from bs4 import BeautifulSoup
import importlib


# 要爬取热评的起始url
url = 'https://m.weibo.cn/comments/hotflow?id=4514782050289970&mid=4514782050289970&max_id_type=0'
# cookie UA要换成自己的
headers = {
    'Cookie': 'WEIBOCN_WM=9006_2001; WEIBOCN_FROM=1110006030; ALF=1597055017; SCF=AlFfFFXPNaDKgqx85KrtJ_D4OlIDpYusd-srzgU9N7wdCuyDFlppseRiusFDb6VRiMrfS6O-MldlxaC2qF-nBwM.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhLoqxGA9SeGA8PL_rcQ1Pv5JpX5K-hUgL.Fo-fSonEe05R1h52dJLoIE5LxK.L1K.LBoqLxKqL1K.LBKnLxKqL1KMLB-Bc1KnReBtt; SSOLoginState=1594463025; SUB=_2A25yDeNtDeRhGeNK7VIW-CrLyDqIHXVR8Y0lrDV6PUJbkdAKLXDQkW1NSUzFjEmYMYOtxSc6SOoyOceWns7NlhqM; SUHB=0vJIObHKmWEkoX; _T_WM=73630556534; MLOGIN=1; M_WEIBOCN_PARAMS=sourceType%3Dqq%26from%3D10A7095010%26featurecode%3Dnewtitle%26oid%3D4514782050289970%26luicode%3D20000061%26lfid%3D4514782050289970%26uicode%3D20000061%26fid%3D4514782050289970; XSRF-TOKEN=b85cc4',
    'Referer': 'https://m.weibo.cn/status/4514782050289970?sourceType=qq&from=10A7095010&wm=9006_2001&featurecode=newtitle',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_page(max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('请检查网络', e.args)


def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        global item_max_id
        item_max_id = {}
        try:
            if items != None:
                item_max_id['max_id'] = items['max_id']
                item_max_id['max_id_type'] = items['max_id_type']
                return item_max_id
        except TypeError:
            print('有可能是IP被封了，若之后一直出现此消息，请更换IP')

def write_csv(jsondata):
    dataone = jsondata.get('data')
    global datas
    try:
        if dataone != None:
            datas = dataone.get('data')
    except AttributeError:
        print('这页没有东西了')
        pass

    if datas != None:
        for data in datas:
            created_at = data.get("created_at")
            like_count = data.get("like_count")
            source = data.get("source")
            total_number = data.get("total_number")
            username = data.get("user").get("screen_name")
            gender = data.get("user").get("gender")
            if gender == 'f':
                gender = '女'
            elif gender == 'm':
                gender = '男'
            comment = data.get("text")
            #print(comment)
            emoji = BeautifulSoup(comment, 'lxml').find('img')
            #print(emoji)
            if emoji is None:
                continue
            elif emoji is not None:
                emoj = emoji.get('alt')
                #if emoj is not None:
                    #continue
                #print(emoj)
           # elif emoji is None:
                #continue
            #elif emoji == '':
                #ontinue
                #print(emoj)
            comment = BeautifulSoup(comment, 'lxml').get_text()
            writer.writerow([username, gender, created_at, like_count, total_number, emoj,
                             json.dumps(comment,  ensure_ascii=False)])

# 存为csv
path = "C:\\Users\\pc\\Desktop\\mojitocomment2.csv"
csvfile = open(path, 'w', encoding = 'utf-8-sig')
writer = csv.writer(csvfile)
writer.writerow(['用户名', '性别', '发表时间', '点赞数', '评论数', '表情', '评论内容'])

maxpage = 3100 #爬取的数量
max_id = 0
id_type = 0
for page in range(0, maxpage):
    print(page)
    jsondata = get_page(max_id, id_type)
    write_csv(jsondata)
    results = parse_page(jsondata)
    x = random.randint(6,8)
    time.sleep(x)
    if results != None:
        max_id = results['max_id']
        id_type = results['max_id_type']
    else:
        print('翻页方式错误')
        time.sleep(10)
        max_id = max_id
        id_type = id_type


