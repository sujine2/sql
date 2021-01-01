import requests
from bs4 import BeautifulSoup


def sendQuery(dicQuery, data):
    '''request 패킷 전송'''
    if dicQuery['method']=='get':
        '''get method'''
        attackSession = requests.session()
        attackSession.cookies.set('PHPSESSID', dicQuery['cookie'])
        '''쿠키설정'''
        print(data)
        res = attackSession.get(url=dicQuery['url'], params=data)
        print(res.elapsed)

        print(res.url)
        return res
    else:
        '''post method'''
        attackSession = requests.session()
        attackSession.cookies.set('PHPSESSID', dicQuery['cookie'])
        res = attackSession.post(url=dicQuery['url'], data=data)
        print(res)
        return res

def findUserKeyword(target, keyword):
    pvalue = keyword.split(',')
    bs = BeautifulSoup(target.text, 'html.parser')
    for value in pvalue:
        bs.get_text()
        #print(value, bs.get_text())
        if value in bs.get_text():
            return 1, target.url
    return 0, target.url


def sendQuery2(dicQuery, data):
    '''request 패킷 전송'''
    if dicQuery['method'] == 'get':
        '''get method'''
        attackSession = requests.session()
        attackSession.cookies.set('PHPSESSID', dicQuery['cookie'])
        '''쿠키설정'''
        print(data)
        res = attackSession.get(url=dicQuery['url'], params=data)
        time = res.elapsed.total_seconds()
        print(type(res.elapsed.total_seconds()),'타입확인--------')
        print(res.elapsed.total_seconds())
        print(res.url)

        if time >= 10.0 :
            return 1
        else :
            return 0
    else:
        '''post method'''
        attackSession = requests.session()
        attackSession.cookies.set('PHPSESSID', dicQuery['cookie'])
        res = attackSession.post(url=dicQuery['url'], data=data)
        print(res)
        print(res.elapsed,'time check')
        return res