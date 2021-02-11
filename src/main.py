import json
import requests
import time
import random
import os
import urllib.request
import ssl

print('================================')
print('     _    _                     ')
print(' ___| | _| | ___ ___   ___ __ _ ')
print('|_  / |/ / |/ __/ _ \ / __/ _` |')
print(' / /|   <| | (_| (_) | (_| (_| |')
print('/___|_|\_\_|\___\___/ \___\__,_|')
print('                                ')
print('================================')

content = []
picnum = 0
Rank = [
    'daily', 'daily_r18', 'weekly', 'weekly_r18', 'r18g', 'monthly', 'rookie',
    'male', 'male_r18', 'female', 'female_r18'
]
Api = [
    'https://www.pixiv.net/ranking.php?mode=daily&content=illust&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=daily_r18&content=illust&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=weekly&content=illust&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=weekly_r18&content=illust&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=r18g&content=illust&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=monthly&content=illust&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=rookie&content=illust&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=male&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=male_r18&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=female&format=json&p=',
    'https://www.pixiv.net/ranking.php?mode=female_r18&format=json&p='
]
Maxpage = [10, 2, 10, 2, 1, 5, 6, 10, 6, 10, 6]
NowDate = time.strftime('%Y.%m.%d')
Logtime = time.strftime('%Y-%m-%d %H %M %S', time.localtime(time.time()))

with open('cofing.json', 'r') as f:
    cofing = json.load(f)
    print('读取配置完成')

qwq = 0
while qwq < 11:
    if os.path.exists(cofing['Download-Path'] + Rank[qwq]):
        print(Rank[qwq] + '目录检查成功')
    else:
        os.mkdir(cofing['Download-Path'] + Rank[qwq])
        print(Rank[qwq] + '目录创建成功')
    qwq += 1

if cofing['Ranklist_Maxpage'][0] != 'ALL' and len(
        cofing['Ranklist_Maxpage']) == 11:
    i = 0
    while i < len(Maxpage):
        if cofing['Ranklist_Maxpage'][i] <= Maxpage[i]:
            Maxpage[i] = cofing['Ranklist_Maxpage'][i]
        i += 1

print('预计爬取 ' + str((Maxpage[0] + Maxpage[1] + Maxpage[2] + Maxpage[3] +
                     Maxpage[4] + Maxpage[5] + Maxpage[6] + Maxpage[7] +
                     Maxpage[8] + Maxpage[9] + Maxpage[10]) * 50) + ' 张图片')

Ranknum = 0
while Ranknum < 11:
    Pagenum = 0
    print('开始爬取 ' + NowDate + '|' + Rank[Ranknum])
    while Pagenum < Maxpage[Ranknum]:
        print('    |Page:' + str(Pagenum + 1) + '开始爬取')
        headers = {
            'authority':
            'www.pixiv.net',
            'method':
            'GET',
            'scheme':
            'https',
            'accept':
            'application/json, text/javascript, */*; q=0.01',
            'accept-encoding':
            'gzip, deflate, br',
            'accept-language':
            'zh-CN,zh;q=0.9,en;q=0.8',
            'sec-ch-ua':
            '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'cookie':
            cofing['Cookie'],
            'referer':
            Api[0].split('&format=json&p=')[0],
            'sec-ch-ua-mobile':
            '?0',
            'sec-fetch-dest':
            'empty',
            'sec-fetch-mode':
            'cors',
            'sec-fetch-site':
            'same-origin',
            'user-agent':
            cofing['User-Agent'][random.randint(0,
                                                len(cofing['User-Agent']) -
                                                1)],
            'x-requested-with':
            'XMLHttpReques',
        }
        res = requests.get(Api[Ranknum] + str(Pagenum + 1),
                           headers=headers,
                           timeout=30).text
        illustjson = json.loads(res)
        i = 0
        while i < len(illustjson['contents']):
            illust = illustjson['contents'][i]
            content.append({
                'illust_id': illust['illust_id'],
                'illust_page_count': illust['illust_page_count'],
                'url': illust['url'],
                'rank': Rank[Ranknum]
            })
            i += 1
        print('    |Page:' + str(Pagenum + 1) + '爬取完毕')
        print('    |Page:' + str(Pagenum + 1) + '爬取到 ' + str(len(content)) +
              ' 张图片')
        n = 0
        while n < len(content):
            illust_download = [
                content[n]['url'], content[n]['illust_page_count'],
                content[n]['illust_id'], content[n]['rank']
            ]
            illust_download[0] = illust_download[0].split(
                str(illust_download[2]))[0]
            illust_download[0] = illust_download[0].split(
                'c/240x480/')[0] + illust_download[0].split('c/240x480/')[1]
            x = 0
            while x < int(illust_download[1]):
                print('开始下载图片:' + str(illust_download[2]) + '_p' + str(x) +
                      '_master1200.jpg')
                ssl._create_default_https_context = ssl._create_unverified_context
                url = illust_download[0] + str(
                    illust_download[2]) + '_p' + str(x) + '_master1200.jpg'
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('Referer', 'https://www.pixiv.net/artworks/' +
                     str(illust_download[2]))
                ]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(
                    url, cofing['Download-Path'] + illust_download[3] + '/' +
                    str(illust_download[2]) + '_p' + str(x) +
                    '_master1200.jpg')
                picnum += 1
                print('图片:' + str(illust_download[2]) + '_p' + str(x) +
                      '_master1200.jpg以下载完成 将在几秒后开始下载下一p')
                time.sleep(random.randint(5, 15))
                x += 1
            n += 1
        content = []
        time.sleep(random.randint(5, 15))
        print()
        Pagenum += 1
    print('爬取完毕 ' + NowDate + '|' + Rank[Ranknum])
    print()
    print()
    Ranknum += 1
print('预计爬取: ' + str((Maxpage[0] + Maxpage[1] + Maxpage[2] + Maxpage[3] +
                      Maxpage[4] + Maxpage[5] + Maxpage[6] + Maxpage[7] +
                      Maxpage[8] + Maxpage[9] + Maxpage[10]) * 50) + ' 实际爬取:' +
      str(picnum))
os.system('pause')
