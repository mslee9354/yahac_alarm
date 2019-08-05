import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, timedelta

webhook = 'https://discordapp.com/api/webhooks/607836586402643970/zRubGSGvIRwt9YLreWuuaYz64LdbWThNyz0h6eN3QgFtA_arUeHJ5gkVTsu0jxozLShP'

tomorrow = datetime.today()
while True:
    with requests.get('https://coding.yah.ac/live.html') as r:
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.select('a')
        today = datetime.today()
        date = '{0}년 {1}월 {2}일'.format(today.year, today.month, today.day)
        id_ = ''
        link = ''
        for elem in links:
            if date in elem.text:
                link = elem.get('href')
                id_ = link.split('/')[-1]
                break
        if today.day == tomorrow.day:
            while True:
                with requests.get('http://youtube.com/heartbeat?video_id={id}&heartbeat_token&c=WEB_EMBEDDED_PLAYER&cver=20190730&utc_offset_minutes=540&upg_content_filter_mode=false&sequence_number=0&time_zone=Asia%%2FSeoul&cpn=BRz7ZfMPp6TxW-_I'.format(id=id_)) as r:
                    data = r.json()
                    if data['status'] != 'live_stream_offline':
                        requests.post(webhook, {'content':'{0}의 코딩야학이 시작되었습니다!!\n바로가기 : {1}'.format(date, link)})
                        print('started!')
                        tomorrow = today + timedelta(days=1)
                        break
                sleep(5)
