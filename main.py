import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, timedelta

webhook = 'https://discordapp.com/api/webhooks/607836586402643970/zRubGSGvIRwt9YLreWuuaYz64LdbWThNyz0h6eN3QgFtA_arUeHJ5gkVTsu0jxozLShP'


tomorrow = datetime.today()
while True:
    today = datetime.today()
    if today.day == tomorrow.day:
        with requests.get('https://coding.yah.ac/live.html') as r:
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.select('a')
            date = '{0}년 {1}월 {2}일'.format(today.year, today.month, today.day)
            id_ = ''
            link = ''
            reason = ''
            form_link = ''
            reason_count = 0
            elem = soup.select('ul > li')[0]
            if date in elem.text:
                link = elem.select('a')[0].get('href')
                id_ = link.split('/')[-1]
                form_link = elem.select('a')[1].get('href')
                requests.post(webhook, {'content':'[Live 알림]\n**{0}의 코딩야학 라이브 방송이 등록되었습니다!!**\n아래의 바로가기를 통하여 채팅에 참여 하실 수 있습니다.\n\n[바로가기] {1}'.format(date, link)})
            while True:
                with requests.get('http://youtube.com/heartbeat?video_id={id}&heartbeat_token&c=WEB_EMBEDDED_PLAYER&cver=20190730&utc_offset_minutes=540&upg_content_filter_mode=false&sequence_number=0&time_zone=Asia%%2FSeoul&cpn=BRz7ZfMPp6TxW-_I'.format(id=id_)) as r:
                    data = r.json()
                    if data['status'] == 'live_stream_offline':
                        if reason != data['reason']:
                            if reason_count % 10 == 0 and reason_count != 0:
                                requests.post(webhook, {'content':'[Live 알림]\n**{0}의 코딩야학 라이브 방송알림**\n{1}\n\n[바로가기] {2}'.format(date, data['reason'], link)})
                                print(data['reason'])
                            reason = data['reason']
                            reason_count += 1
                            print(reason_count)
                    else:
                        assert data['status'] != 'error', 'error! '+ id_
                        
                        requests.post(webhook, {'content':'[Live 알림]\n**{0}의 코딩야학 라이브 방송이 시작되었습니다!!**\n아래의 바로가기를 통하여 라이브를 확인 하실 수 있습니다.\n\n[바로가기]{1}'.format(date, link)})
                        print('started!')
                        while True:
                            with requests.get('https://www.youtube.com/live_chat?continuation=0ofMyAM6GiBDZzhLRFFvTFExRkZSVmR3VVdzd1NUUWdBUSUzRCUzRDABaASCAQQIBBAAiAEBoAGP2eq04_LjAg%253D%253D', header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}) as r:
                                if form_link in r.text:
                                    requests.post(webhook, {'content':'[Live 알림]\n**{0}의 코딩야학 이벤트가 시작되었습니다!!**\n아래의 바로가기를 통하여 이벤트에 참여 하실 수 있습니다.\n\n[바로가기] {1}'.format(date, form_link)})
                                    break
                            sleep(5)
                        tomorrow = today + timedelta(days=1)
                        break
                sleep(5)
