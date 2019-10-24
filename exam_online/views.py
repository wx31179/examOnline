from __future__ import unicode_literals
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth import authenticate, login, logout
from .models import loginuser,type,exam,exam_answers,test_content,test_answer,doc_info,setting,roles,group_permissions
#from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, HttpResponse,redirect,render
from django.http import JsonResponse,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from examOnline.settings import DOC_ROOT
from django.contrib.auth.hashers import make_password, check_password
from xpinyin import Pinyin
import json
import datetime
import hashlib
import base64
import os
import ldap
import re
import time

# Create your views here.
email = "guest"

def index(request):
    next = request.GET.get("next")
    if next:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if "@" in username:
                ldapserver = setting.objects.get(strings="LDAP_SERVER").string_value
                ldapbinddn = setting.objects.get(strings="LDAP_BIND_DN").string_value
                ldapconn = ldap.initialize(ldapserver)
                try:
                    ldap_auth = ldapconn.simple_bind_s('cn=%s,' % username + ldapbinddn, password)
                    if ldap_auth:
                        request.session["username"] = username
                        request.session["password"] = password
                        user = loginuser.objects.filter(username=username)
                        if not user:
                            loginuser.objects.create(username=username,
                                                     create_Time=datetime.datetime.now(),
                                                     last_login_time=datetime.datetime.now())
                            roles.objects.create(user_name=username,role_name="User")
                            request.session["role"] = roles.objects.get(user_name=username).role_name
                            return HttpResponseRedirect('/edit_user_info/')
                        else:
                            loginuser.objects.filter(username=username).update(last_login_time=datetime.datetime.now())
                            request.session["role"] = roles.objects.get(user_name=username).role_name
                            return HttpResponseRedirect('/%s/'%next)
                except BaseException as e:
                    Message = {"message": "用户名或密码错误，请重新输入。"}
                    return render(request, '../templates/login.html', {"message": json.dumps(Message)})
            else:
                user = loginuser.objects.filter(username=username)
                if user:
                    password_auth = check_password(password, loginuser.objects.get(username=username).password)
                    if password_auth:
                        request.session["username"] = username
                        request.session["password"] = password
                        loginuser.objects.filter(username=username).update(last_login_time=datetime.datetime.now())
                        request.session["role"] = roles.objects.get(user_name=username).role_name
                        return HttpResponseRedirect('/main/')
                    else:
                        Message = {"message": "密码错误，请重新输入。"}
                        return render(request, '../templates/login.html', {"message": json.dumps(Message)})
                else:
                    Message = {"message": "用户名错误，请重新输入。"}
                    return render(request, '../templates/login.html', {"message": json.dumps(Message)})
        else:
            return render(request, '../templates/login.html')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if "@" in username:
                ldapserver = setting.objects.get(strings="LDAP_SERVER").string_value
                ldapbinddn = setting.objects.get(strings="LDAP_BIND_DN").string_value
                ldapconn = ldap.initialize(ldapserver)
                try:
                    ldap_auth = ldapconn.simple_bind_s('cn=%s,'%username + ldapbinddn, password)
                    if ldap_auth:
                        request.session["username"] = username
                        request.session["password"] = password
                        user = loginuser.objects.filter(username=username)
                        if not user:
                            loginuser.objects.create(username=username,
                                                     create_Time=datetime.datetime.now(),
                                                     last_login_time=datetime.datetime.now())
                            roles.objects.create(user_name=username, role_name="User")
                            request.session["role"] = roles.objects.get(user_name=username).role_name
                            return HttpResponseRedirect('/edit_user_info/')
                        else:
                            loginuser.objects.filter(username=username).update(last_login_time=datetime.datetime.now())
                            request.session["role"] = roles.objects.get(user_name=username).role_name
                            return HttpResponseRedirect('/main/')
                except BaseException as e:
                    Message = {"message": "%s"%e}
                    return render(request, '../templates/login.html', {"message": json.dumps(Message)})
            else:
                user = loginuser.objects.filter(username=username)
                if user:
                    password_auth = check_password(password, loginuser.objects.get(username=username).password)
                    if password_auth:
                        request.session["username"] = username
                        request.session["password"] = password
                        loginuser.objects.filter(username=username).update(last_login_time=datetime.datetime.now())
                        request.session["role"] = roles.objects.get(user_name=username).role_name
                        return HttpResponseRedirect('/main/')
                    else:
                        Message = {"message": "密码错误，请重新输入。"}
                        return render(request, '../templates/login.html',{"message":json.dumps(Message)})
                else:
                    Message = {"message": "用户名错误，请重新输入。"}
                    return render(request, '../templates/login.html', {"message": json.dumps(Message)})
        else:
            Message = {"message": "start"}
            return render(request, '../templates/login.html', {"message": json.dumps(Message)})

def backup_setting(request):
    return render(request, '../templates/backup_setting.html')

def public_office(request):
    global email
    email = request.session["username"]
    Message = {"message": "start"}
    return render(request,'../templates/public_office.html', {"message": json.dumps(Message)})

def person_setting(request):
    return render(request, '../templates/person_setting.html')

def person_meassage(request):
    return render(request, '../templates/person_meassage.html')

def main(request):
    return render(request, '../templates/main.html')

def edit_user_info(request):
    if request.method == "GET":
        typelist = type.objects.values("Total_Type_values").filter(Total_Type="P_Type")
        return render(request,'../templates/edit_user_info.html',{"typelist":typelist})
    else:
        project = request.POST.get("project")
        loginuser.objects.filter(username=request.session["username"]).update(P_Type=project)
        return HttpResponseRedirect('/main/')

def userlogout(request):
    request.session.delete("session_key")
    request.session.clear()
    return HttpResponseRedirect('/')

@csrf_exempt
def create_exam(request):
    if request.method == "GET":
        Type = request.GET.get("Type")
        typelist = type.objects.values("Total_Type_values").filter(Total_Type="P_Type")
        levellist = type.objects.values("Total_Type_values").filter(Total_Type="T_Level")
        return render(request, "../templates/create_exam.html", {"typelist": typelist,
                                                             "levellist": levellist,
                                                             "type": Type})

    else:
        ipstamp = request.META["REMOTE_ADDR"].replace(".", "")
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        ran_str = ipstamp + timestamp
        exam_id = "exam_%s" % ran_str
        exam_type = request.POST.get("exam_type")
        if exam_type == "R":
            project = request.POST.get("project")
            content = request.POST.get("content")
            level = request.POST.get("level")
            all_answer = request.POST.getlist("R_all_answer")
            right_answer = request.POST.get("R_right_answer")
            exam.objects.create(exam_id=exam_id, P_Type=project, T_type=exam_type,
                                content=content,
                                T_Level=level,
                                submitter=request.session["username"],
                                create_Time=datetime.datetime.now())
            for i in all_answer:
                exam_answers.objects.create(exam_id=exam_id, answers=i, answers_values=False)
            exam_answers.objects.filter(answers=right_answer).update(answers_values=True)
        elif exam_type == "M":
            project = request.POST.get("project")
            content = request.POST.get("content")
            level = request.POST.get("level")
            all_answer = request.POST.getlist("M_all_answer")
            right_answer = request.POST.getlist("M_right_answer")
            exam.objects.create(exam_id=exam_id, P_Type=project, T_type=exam_type,
                                content=content,
                                T_Level=level,
                                submitter=request.session["username"],
                                create_Time = datetime.datetime.now())
            for i in all_answer:
                exam_answers.objects.create(exam_id=exam_id, answers=i, answers_values=False)
            for j in right_answer:
                exam_answers.objects.filter(answers=j).update(answers_values=True)
        elif exam_type == "W":
            project = request.POST.get("project")
            content = request.POST.get("content")
            level = request.POST.get("level")
            right_answer = request.POST.get("W_right_answer")
            exam.objects.create(exam_id=exam_id, P_Type=project, T_type=exam_type,
                                content=content,
                                T_Level=level,
                                submitter=request.session["username"],
                                create_Time=datetime.datetime.now())
            if right_answer:
                exam_answers.objects.create(exam_id=exam_id, answers=right_answer, answers_values="")
            else:
                pass
        return render(request, "../templates/my_exam.html", {"exams": exam.objects.filter(
            submitter=request.session["username"]).all()})

def iframe_main(request):
    return render(request, '../templates/iframe_main.html')

def my_exam(request):
    if request.method == "POST":
        ipstamp = request.META["REMOTE_ADDR"].replace(".","")
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        ran_str = ipstamp+timestamp
        exam_id = "exam_%s"%ran_str
        exam_type = request.POST.get("exam_type")
        if exam_type == "R":
            project = request.POST.get("project")
            content = request.POST.get("content")
            level = request.POST.get("level")
            all_answer = request.POST.getlist("R_all_answer")
            right_answer = request.POST.get("R_right_answer")
            exam.objects.create(exam_id=exam_id,P_Type=project,T_type=exam_type,
                                        content=content,
                                        T_Level=level,
                                        submitter=request.session["username"],
                                        create_Time=datetime.datetime.now())
            for i in all_answer:
                exam_answers.objects.create(exam_id=exam_id,answers=i,answers_values=False)
            exam_answers.objects.filter(answers=right_answer).update(answers_values=True)

        elif exam_type == "M":
            project = request.POST.get("project")
            content = request.POST.get("content")
            level = request.POST.get("level")
            all_answer = request.POST.getlist("M_all_answer")
            right_answer = request.POST.getlist("M_right_answer")
            exam.objects.create(exam_id=exam_id, P_Type=project, T_type=exam_type,
                                content=content,
                                T_Level=level,
                                submitter=request.session["username"],
                                create_Time = datetime.datetime.now())
            for i in all_answer:
                exam_answers.objects.create(exam_id=exam_id, answers=i, answers_values=False)
            for j in right_answer:
                exam_answers.objects.filter(answers=j).update(answers_values=True)
        elif exam_type == "W":
            project = request.POST.get("project")
            content = request.POST.get("content")
            level = request.POST.get("level")
            right_answer = request.POST.get("W_right_answer")
            exam.objects.create(exam_id=exam_id, P_Type=project, T_type=exam_type,
                                content=content,
                                T_Level=level,
                                submitter=request.session["username"],
                                create_Time=datetime.datetime.now())
            if right_answer:
                exam_answers.objects.create(exam_id=exam_id, answers=right_answer, answers_values="")
            else:
                pass
        typelist = type.objects.values("Total_Type_values").filter(Total_Type="P_Type")
        levellist = type.objects.values("Total_Type_values").filter(Total_Type="T_Level")
        return render(request, "../templates/my_exam.html", {"typelist": typelist,
                                                             "levellist": levellist,
                                                             "exams":exam.objects.filter(
                                                                 submitter=request.session["username"]).all()})
    else:
        if request.session["role"] == "user":
            return render(request,"../templates/my_exam.html",{"exams":exam.objects.filter(
                                                                submitter=request.session["username"]).all()})
        else:
            return render(request,"../templates/my_exam.html",{ "exams":exam.objects.all()})

def edit_exam(request):
    if request.method == 'GET':
        all_answer = {}
        id = request.GET.get("id")
        types = request.GET.get("type")
        exam_info = exam.objects.get(exam_id=id)
        answers = exam_answers.objects.filter(exam_id=id)
        for i in answers:
            all_answer[i.answers] = i.answers_values
        typeinfo = {"type":{id:types}}
        typeinfo = json.dumps(typeinfo)
        all_answer= json.dumps(all_answer)
        typelist = type.objects.values("Total_Type_values").filter(Total_Type="P_Type")
        levellist = type.objects.values("Total_Type_values").filter(Total_Type="T_Level").\
            exclude(Total_Type_values=exam_info.T_Level)
        return render(request, '../templates/edit_exam.html', {"p_list":typelist,
                                                               "levellist":levellist,
                                                               'exam':exam_info,
                                                               "all_answer":all_answer,
                                                               "type":typeinfo,
                                                               "types":types})

    elif request.method == "POST":
        exam_id = request.POST.get("id")
        exam_type = request.POST.get("type")
        if exam_type == "R":
            project = request.POST.get("%s_project"%exam_id)
            content = request.POST.get("%s_content"%exam_id)
            level = request.POST.get("%s_level"%exam_id)
            all_answer = request.POST.getlist("%s_all_answer"%exam_id)
            right_answer = request.POST.get("%s_right_answer"%exam_id)
            exam_info = exam.objects.get(exam_id=exam_id)
            exam_info.P_Type = project
            exam_info.T_Level = level
            exam_info.content = content
            exam_info.save()
            exam_answers.objects.filter(exam_id=exam_id).delete()
            for i in all_answer:
                exam_answers.objects.create(exam_id=exam_id,answers=i,answers_values=False)
            exam_answers.objects.filter(answers=right_answer).update(answers_values=True)

        elif exam_type == "M":
            project = request.POST.get("%s_project"%exam_id)
            content = request.POST.get("%s_content"%exam_id)
            level = request.POST.get("%s_level"%exam_id)
            all_answer = request.POST.getlist("%s_all_answer"%exam_id)
            right_answer = request.POST.getlist("%s_right_answer"%exam_id)
            exam_info = exam.objects.get(exam_id=exam_id)
            exam_info.P_Type = project
            exam_info.T_Level = level
            exam_info.content = content
            exam_info.save()
            exam_answers.objects.filter(exam_id=exam_id).delete()
            for i in all_answer:
                exam_answers.objects.create(exam_id=exam_id, answers=i, answers_values=False)
            for j in right_answer:
                exam_answers.objects.filter(answers=j).update(answers_values=True)
        elif exam_type == "W":
            project = request.POST.get("%s_project"%exam_id)
            content = request.POST.get("%s_content"%exam_id)
            level = request.POST.get("%s_level"%exam_id)
            right_answer = request.POST.get("%s_right_answer"%exam_id)
            exam_info = exam.objects.get(exam_id=exam_id)
            exam_info.P_Type = project
            exam_info.T_Level = level
            exam_info.content = content
            exam_info.save()
            exam_answers.objects.filter(exam_id=exam_id).delete()
            if right_answer:
                exam_answers.objects.create(exam_id=exam_id, answers=right_answer, answers_values="")
            else:
                pass
        typelist = type.objects.values("Total_Type_values").filter(Total_Type="P_Type")
        return redirect("/my_exam/", {"typelist": typelist, "exams": exam.objects.all()})

def check_exam(request):
    if request.method == "GET":
        content =""
        T_type = ""
        exam_ids = []
        all_answer = []
        right_answer = []
        id = request.GET.get("id")
        if request.session["role"] == "user":
            exam_id = exam.objects.filter(submitter=request.session["username"]).values("exam_id")
            for j in exam_id:
                exam_ids.append(j["exam_id"])
            exam_index = exam_ids.index(id)
            exam_info = exam.objects.filter(exam_id=id).values("content","T_type")
            exam_all_answers = exam_answers.objects.filter(exam_id=id).values("answers","answers_values")
            exam_right_answers = exam_answers.objects.filter(exam_id=id).values("answers_values","answers")
            for answer in exam_all_answers:
                if answer["answers_values"] == True:
                    all_answer.append(answer["answers"])
                    right_answer.append(answer["answers"])
                elif answer["answers_values"] == False:
                    all_answer.append(answer["answers"])
                elif answer["answers_values"] == None:
                    right_answer.append(answer["answers"])
            for i in exam_info:
                content = i['content']
                T_type = i["T_type"]
            if exam_index == 0:
                try:
                    a = exam_ids[1]
                    return render(request, "../templates/check_exam.html", {'exam': content,
                                                                            "exam_id":id,
                                                                            "T_type":T_type,
                                                                            "all_answer":all_answer,
                                                                            "right_answer":right_answer,
                                                                            "exam_previous":exam_ids[exam_index],
                                                                            "exam_next":exam_ids[exam_index+1]})
                except IndexError as e:
                    return render(request, "../templates/check_exam.html", {'exam': content,
                                                                            "exam_id": id,
                                                                            "T_type": T_type,
                                                                            "all_answer": all_answer,
                                                                            "right_answer": right_answer,
                                                                            "exam_previous": exam_ids[exam_index],
                                                                            "exam_next": exam_ids[exam_index]})
            elif exam_index + 1 > exam_ids.index(exam_ids[-1]):
                return render(request, "../templates/check_exam.html",
                              {'exam': content,
                               "exam_id": id,
                               "T_type": T_type,
                               "all_answer": all_answer,
                               "right_answer": right_answer,
                               "exam_previous": exam_ids[exam_index - 1],
                               "exam_next": exam_ids[exam_index]})
            else:
                return render(request,"../templates/check_exam.html",{'exam': content,
                                                                      "exam_id": id,
                                                                      "T_type": T_type,
                                                                      "all_answer": all_answer,
                                                                      "right_answer": right_answer,
                                                                      "exam_previous":exam_ids[exam_index-1],
                                                                        "exam_next":exam_ids[exam_index+1]})
        else:
            exam_id = exam.objects.all().values("exam_id")
            for j in exam_id:
                exam_ids.append(j["exam_id"])
            exam_index = exam_ids.index(id)
            exam_info = exam.objects.filter(exam_id=id).values("content", "T_type")
            exam_all_answers = exam_answers.objects.filter(exam_id=id).values("answers", "answers_values")
            exam_right_answers = exam_answers.objects.filter(exam_id=id).values("answers_values", "answers")
            for answer in exam_all_answers:
                if answer["answers_values"] == True:
                    all_answer.append(answer["answers"])
                    right_answer.append(answer["answers"])
                elif answer["answers_values"] == False:
                    all_answer.append(answer["answers"])
                elif answer["answers_values"] == None:
                    right_answer.append(answer["answers"])
            for i in exam_info:
                content = i['content']
                T_type = i["T_type"]
            if exam_index == 0:
                try:
                    a = exam_ids[1]
                    return render(request, "../templates/check_exam.html", {'exam': content,
                                                                            "exam_id": id,
                                                                            "T_type": T_type,
                                                                            "all_answer": all_answer,
                                                                            "right_answer": right_answer,
                                                                            "exam_previous": exam_ids[exam_index],
                                                                            "exam_next": exam_ids[exam_index + 1]})
                except IndexError as e:
                    return render(request, "../templates/check_exam.html", {'exam': content,
                                                                            "exam_id": id,
                                                                            "T_type": T_type,
                                                                            "all_answer": all_answer,
                                                                            "right_answer": right_answer,
                                                                            "exam_previous": exam_ids[exam_index],
                                                                            "exam_next": exam_ids[exam_index]})
            elif exam_index + 1 > exam_ids.index(exam_ids[-1]):
                return render(request, "../templates/check_exam.html",
                              {'exam': content,
                               "exam_id": id,
                               "T_type": T_type,
                               "all_answer": all_answer,
                               "right_answer": right_answer,
                               "exam_previous": exam_ids[exam_index - 1],
                               "exam_next": exam_ids[exam_index]})
            else:
                return render(request, "../templates/check_exam.html", {'exam': content,
                                                                        "exam_id": id,
                                                                        "T_type": T_type,
                                                                        "all_answer": all_answer,
                                                                        "right_answer": right_answer,
                                                                        "exam_previous": exam_ids[exam_index - 1],
                                                                        "exam_next": exam_ids[exam_index + 1]})

def check_test(request):
    if request.method == "GET":
        answer_R_list = []
        answer_M_list = []
        answer_W_list = []
        test_id = request.GET.get("id")
        test_info = test_content.objects.filter(test_id=test_id).all()
        test_answers = test_answer.objects.filter(test_id=test_id).values("exam_id","T_type","chose_answer","right_answer",
                                                                          "is_right")
        for info in test_answers:
            answer_R = {}
            answer_M = {}
            answer_W = {}
            if info["T_type"] == "R":
                all_answers = []
                for i in exam.objects.values("content").filter(exam_id=info["exam_id"]):
                    answer_R["content"] = i["content"]
                for j in exam_answers.objects.values("answers").filter(exam_id=info["exam_id"]):
                    all_answers.append(j["answers"])
                answer_R["all_answers"] = all_answers
                answer_R["chose_answer"] = info["chose_answer"]
                answer_R["right_answer"] = info["right_answer"]
                answer_R["is_raght"] = info["is_right"]
                answer_R_list.append(answer_R)
            elif info["T_type"] == "M":
                all_answers = []
                for i in exam.objects.values("content").filter(exam_id=info["exam_id"]):
                    answer_M["content"] = i["content"]
                for j in exam_answers.objects.values("answers").filter(exam_id=info["exam_id"]):
                    all_answers.append(j["answers"])
                answer_M["all_answers"] = all_answers
                answer_M["chose_answer"] = info["chose_answer"]
                answer_M["right_answer"] = info["right_answer"]
                answer_M["is_raght"] = info["is_right"]
                answer_M_list.append(answer_M)
            else:
                all_answers = []
                for i in exam.objects.values("content").filter(exam_id=info["exam_id"]):
                    answer_W["content"] = i["content"]
                for j in exam_answers.objects.values("answers").filter(exam_id=info["exam_id"]):
                    all_answers.append(j["answers"])
                answer_W["all_answers"] = all_answers
                answer_W["chose_answer"] = info["chose_answer"]
                answer_W["right_answer"] = info["right_answer"]
                answer_W["is_raght"] = info["is_right"]
                answer_W_list.append(answer_W)
        return render(request,'../templates/check_test.html',{"test_content":test_info,
                                                              "answer_W_list":answer_W_list,
                                                              "answer_R_list":answer_R_list,
                                                              "answer_M_list":answer_M_list})

def delete_exam(request):
    exam_id = request.GET.get("id")
    try:
        exam.objects.filter(exam_id=exam_id).delete()
        exam_answers.objects.filter(exam_id=exam_id).delete()
        data={"result":True}
    except BaseException as e:
        data = {"result":e}
    return JsonResponse(data,safe=False)

def exam_temp(request):
    if request.method == "POST":
        ipstamp = request.META["REMOTE_ADDR"].replace(".","")
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        test_str = ipstamp+timestamp
        test_id = "test_%s"%test_str
        project = request.POST.get("project")
        test_time = request.POST.get("test_time")
        test_range = request.POST.get("test_range")
        test_content.objects.create(test_id=test_id, P_Type=project, test_time=test_time,
                            test_range=test_range,
                            submitter=request.session["username"],
                            create_time=datetime.datetime.now())
        return redirect("/start_test/?test_id=%s"%test_id)

    else:
        typelist = type.objects.values("Total_Type_values").filter(Total_Type="P_Type")
        return render(request, '../templates/Exam_temp.html',{"typelist":typelist})

def start_test(request):
    if request.method == "POST":
        test_id = request.POST.get("test_id")
        test_list = test_answer.objects.values("exam_id","T_type").filter(test_id=test_id)
        for answer_list in test_list:
            right_answer = ""
            right_answers = []
            answer = request.POST.getlist(answer_list["exam_id"])
            if len(answer) > 1:
                answer_str = ",".join(answer)
            else:
                answer_str = "".join(answer)
            test_answer.objects.filter(test_id=test_id,exam_id=answer_list["exam_id"]).\
                                                                            update(chose_answer=answer_str)
            if answer_list["T_type"] == "R":
                right_answer = exam_answers.objects.values("answers").filter(exam_id=answer_list["exam_id"],
                                                                             answers_values=True)
                for answer in right_answer:
                    test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                        right_answer=answer["answers"])
                    if answer["answers"] == answer_str:
                        test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                            is_right=True)
                    elif answer_str == None:
                        test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                            is_right=False)
                    else:
                        test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                            is_right=False)
            elif answer_list["T_type"] == "M":
                right_answer_list = exam_answers.objects.values_list("answers").filter(exam_id=answer_list["exam_id"],
                                                                             answers_values=True)
                for answer in right_answer_list:
                    right_answers.append("%s"%answer)

                right_answer = ",".join(right_answers)
                test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                    right_answer=right_answer)
                if right_answer == answer_str:
                    test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                        is_right=True)
                elif answer_str == None:
                    test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                        is_right=False)
                else:
                    test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                        is_right=False)
            else:
                right_answer = exam_answers.objects.values("answers").filter(exam_id=answer_list["exam_id"]
                                                                            )
                for answer in right_answer:
                    test_answer.objects.filter(test_id=test_id, exam_id=answer_list["exam_id"]).update(
                        right_answer=answer["answers"])
        total_test = test_answer.objects.values_list("is_right").filter(test_id=test_id).exclude(T_type="W")
        total_right_answer = []
        for true_answer in total_test:
            if "%s"%true_answer == "True":
                total_right_answer.append("%s"%true_answer)
        test_content.objects.filter(test_id=test_id).update(correct_rate=
                                                            len(total_right_answer)/len(total_test)*100)
        return  render(request,"../templates/close.html")
    else:
        P_Type = ""
        test_range = ""
        test_time = ""
        test_id = request.GET.get("test_id")
        test_content_info = test_content.objects.filter(test_id=test_id).values("P_Type","test_time",
                                                                                "test_range")
        for test in test_content_info:
            P_Type = test["P_Type"]
            test_range = test["test_range"]
            test_time = test["test_time"]
        exam_infos_R = []
        exam_infos_M = []
        exam_infos_W = []
        answers = []
        exam_ids = exam.objects.all().values("exam_id", "content", "T_type")
        conut_R = 1
        count_M = 1
        count_W = 1
        for i in exam_ids:
            exam_info = {}
            exam_info["T_type"] = i["T_type"]
            if i["T_type"] == "R":
                exam_id = i["exam_id"]
                test_answer.objects.create(test_id=test_id, exam_id=exam_id, T_type=i["T_type"])
                exam_info["content"] = "<p>%s.</p>%s"%(conut_R,i["content"])
                exam_info["exam_id"] = exam_id
                answer = exam_answers.objects.filter(exam_id=exam_id).values("answers", "answers_values")
                for i in answer:
                    answers.append(i["answers"])
                    exam_info["answers"] = answers
                exam_infos_R.append(exam_info)
                answers = []
                conut_R += 1
            elif i["T_type"] == "M":
                exam_id = i["exam_id"]
                test_answer.objects.create(test_id=test_id, exam_id=exam_id, T_type=i["T_type"])
                exam_info["content"] = "<p>%s.</p>%s"%(count_M,i["content"])
                exam_info["exam_id"] = exam_id
                answer = exam_answers.objects.filter(exam_id=exam_id).values("answers", "answers_values")
                for i in answer:
                    answers.append(i["answers"])
                    exam_info["answers"] = answers
                exam_infos_M.append(exam_info)
                answers = []
                count_M += 1
            else:
                exam_id = i["exam_id"]
                test_answer.objects.create(test_id=test_id, exam_id=exam_id, T_type=i["T_type"])
                exam_info["content"] = "<p>%s.</p>%s"%(count_W,i["content"])
                exam_info["exam_id"] = exam_id
                answer = exam_answers.objects.filter(exam_id=exam_id).values("answers", "answers_values")
                for i in answer:
                    answers.append(i["answers"])
                    exam_info["answers"] = answers
                exam_infos_W.append(exam_info)
                answers = []
                count_W += 1
        return render(request, "../templates/start_exam.html", {"test_id": test_id,
                                                                "exam_info_R": exam_infos_R,
                                                                "exam_info_M": exam_infos_M,
                                                                "exam_info_W": exam_infos_W,
                                                                "test_content":test_content_info,
                                                                "P_Type":P_Type,
                                                                "test_range":test_range,
                                                                "test_time":test_time,})

def test_analysis(request):
    if request.session["role"] == "role":
        return render(request, '../templates/test_analysis.html', {"user": request.session["username"]})
    else:
        user_list = loginuser.objects.all().exclude(username=request.session["username"])
        return render(request,'../templates/test_analysis.html',{"user_list":user_list,
                                                             "user":request.session["username"]})

def test_record(request):
    if request.session["role"] == "user":
        test_info = test_content.objects.all().filter(submitter=request.session["username"])
        return render(request,"../templates/test_record.html",{"test_info":test_info})
    else:
        test_content.objects.filter(correct_rate=None).update(correct_rate=0)
        test_info = test_content.objects.all()
        return render(request, "../templates/test_record.html", {"test_info": test_info})

def analysisinfo(request):
    if request.method == "GET":
        serise = []
        time = request.GET.get("time")
        users = request.GET.getlist("users[]")
        for user in users:
            data = []
            datainfo = {}
            test_info = test_content.objects.filter(submitter=user).values("create_time","correct_rate")
            for i in test_info:
                data.append([i["create_time"], float(i["correct_rate"])])
            datainfo["name"] = user
            datainfo["data"] = data
            serise.append(datainfo)
        timedate = []
        for time in serise:
            for j in time["data"]:
                timedate.append(j[0])
        data = {
            'title': {
                'text': '测试成绩记录（不包含主观问答题）'},
            'xAxis':{
                'title': {
                    'text': '测试时间'
                },
            'categories':timedate
            },
            'chart': {
                'type': 'line'},
            'serise':serise
        }
        return JsonResponse(data,safe=False)

def check_doc(request):
    wopiserver = setting.objects.get(strings="WOPI_SERVER").string_value
    hostip = setting.objects.get(strings="HOST_IP").string_value
    global email
    email = request.session["username"]
    doc_info_all_list = []
    doc_info_all = doc_info.objects.all().exclude(P_Type="Office_Supplies").exclude(P_Type="Grade").exclude(P_Type="Attendance_statistics")
    for doc in doc_info_all:
        doc_info_dic = {}
        if doc.type == "xls" or doc.type =="xlsx":
            doc_info_dic["name"] = doc.name
            doc_info_dic["url"] = "http://%s/x/_layouts/xlviewerinternal.aspx?" \
                                  "ui=zh-CN&rs=zh-CN&WOPISrc=http://%s/wopi/files/%s"% \
                                  (wopiserver,hostip, doc.path)
            doc_info_dic["edit"] = doc.edit
            doc_info_dic["doc_id"] = doc.doc_id
            doc_info_dic["path"] = doc.path.replace(".","")
            doc_info_dic["tag"] = doc.tag
            doc_info_dic["P_Type"] = doc.P_Type
            doc_info_dic["submitter"] = doc.submitter
            doc_info_dic["create_time"] = doc.create_time
            doc_info_all_list.append(doc_info_dic)
        elif doc.type == "doc" or doc.type =="docx":
            doc_info_dic["name"] = doc.name
            doc_info_dic["url"] = "http://%s/wv/wordviewerframe.aspx?" \
                                  "ui=zh-CN&rs=zh-CN&WOPISrc=http://%s/wopi/files/%s"% \
                                  (wopiserver, hostip, doc.path)
            doc_info_dic["edit"] = doc.edit
            doc_info_dic["doc_id"] = doc.doc_id
            doc_info_dic["path"] = doc.path.replace(".","")
            doc_info_dic["tag"] = doc.tag
            doc_info_dic["P_Type"] = doc.P_Type
            doc_info_dic["submitter"] = doc.submitter
            doc_info_dic["create_time"] = doc.create_time
            doc_info_all_list.append(doc_info_dic)
        elif doc.type == "pptx" or doc.type =="ppt":
            doc_info_dic["name"] = doc.name
            doc_info_dic["url"] = "http://%s/p/PowerPointFrame.aspx?PowerPointView=ReadingView&" \
                                  "ui=zh-CN&rs=zh-CN&WOPISrc=http://%s/wopi/files/%s" % \
                                  (wopiserver, hostip, doc.path)
            doc_info_dic["edit"] = doc.edit
            doc_info_dic["doc_id"] = doc.doc_id
            doc_info_dic["path"] = doc.path.replace(".","")
            doc_info_dic["tag"] = doc.tag
            doc_info_dic["P_Type"] = doc.P_Type
            doc_info_dic["submitter"] = doc.submitter
            doc_info_dic["create_time"] = doc.create_time
            doc_info_all_list.append(doc_info_dic)
        else:
            doc_info_dic["name"] = doc.name
            doc_info_dic["url"] = "http://%s/wv/wordviewerframe.aspx?" \
                                  "PdfMode=1&ui=zh-CN&rs=zh-CN&WOPISrc=http://%s/wopi/files/%s" % \
                                  (wopiserver, hostip, doc.path)
            doc_info_dic["edit"] = doc.edit
            doc_info_dic["doc_id"] = doc.doc_id
            doc_info_dic["path"] = doc.path.split(".")[0]
            doc_info_dic["tag"] = doc.tag
            doc_info_dic["P_Type"] = doc.P_Type
            doc_info_dic["submitter"] = doc.submitter
            doc_info_dic["create_time"] = doc.create_time
            doc_info_all_list.append(doc_info_dic)
    return render(request,'../templates/check_doc.html',{"doc_info_all":doc_info_all_list})

@csrf_exempt
def upload_doc(request):
    if request.method == "POST":
        doc = request.FILES.get("doc")
        pr = request.POST.get("pr")
        edit = request.POST.get("edit")
        tag = request.POST.get("tag")
        doc_parr = doc.name.strip()
        doc_parr = doc_parr.replace(" ","_")
        parrt = {}
        p = Pinyin()
        regex_str = re.compile(".*?([\u4E00-\u9FA5]+).*?")
        match_obj = regex_str.findall(doc_parr)
        for i in match_obj:
            parrt[i] = p.get_initials(i, "")
        for j, k in parrt.items():
            doc_parr = re.sub(j, k, doc_parr)
        ipstamp = request.META["REMOTE_ADDR"].replace(".", "")
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        doc_id = ipstamp + timestamp + doc_parr.split(".")[0]
        try:
            if doc_parr not in [i for i in os.listdir(DOC_ROOT)]:
                doc_path = os.path.join(DOC_ROOT, doc_parr)
                destination = open(doc_path, 'wb+')
                for chunk in doc.chunks():
                    destination.write(chunk)
                destination.close()
                doc_name_list = doc.name.split(".")
                if edit == "True":
                    doc_info.objects.get_or_create(doc_id=doc_id,name=doc.name,path=doc_parr,
                                            type=doc_name_list[-1],P_Type=pr,
                                            submitter=request.session["username"],
                                            edit=1,
                                            tag=tag,
                                            create_time=datetime.datetime.now())
                else:
                    doc_info.objects.get_or_create(doc_id=doc_id,name=doc.name, path=doc_parr,
                                                   type=doc_name_list[-1], P_Type=pr,
                                                   submitter=request.session["username"],
                                                   edit=0,
                                                   tag=tag,
                                                   create_time=datetime.datetime.now())
                return JsonResponse({"error":""})
            else:
                return JsonResponse({"error":"%s文件名重复，请改名"%doc.name})
        except AttributeError:
            return JsonResponse({"error":"请选择文件之后再上传，谢谢"})
    else:
        user_p = loginuser.objects.get(username=request.session["username"])
        typelist = type.objects.values("Total_Type_values").filter(Total_Type="P_Type").\
                    exclude(Total_Type_values=user_p.P_Type)
        return render(request,'../templates/upload_doc.html',{"typelist":typelist,"user_p":user_p})

def edit_exam_json(request):
    if request.method == "GET":
        all_answer = {}
        id = request.GET.get("id")
        type = request.GET.get("type")
        answers = exam_answers.objects.filter(exam_id=id)
        for i in answers:
            all_answer[i.answers] = i.answers_values
        all_answer= json.dumps(all_answer)
        return HttpResponse(all_answer,content_type="application/json")

#此为处理编辑器处理上传图片的函数
@csrf_exempt  # 取消csrf验证，否则会有403错误
def file_upload(request):
    files = request.FILES.get('upload_file')
    name = files.name
    att = name.split(".")[1]
    ipstamp = request.META["REMOTE_ADDR"].replace(".", "")
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    ran_str = ipstamp + timestamp
    file_name = "image_%s.%s"%(ran_str,att)
    file_dir = settings.UPLOAD_ROOT
    file_path = "%s/%s"%(file_dir,file_name)
    if request.method == "POST":
        open(file_path, 'wb+').write(files.read())  # 上传文件
        # 得到JSON格式的返回值
        upload_info = {"success": True, 'file_path': settings.UPLOAD_URL + file_name}
        upload_info = json.dumps(upload_info)
        return HttpResponse(upload_info, content_type="application/json")

#此为office online处理函数
def file_iterator(filename,chunk_size=512):
    '''read file'''
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break


@csrf_exempt
def wopiGetFileInfo(request,fileid = "test.txt"):
    try:
        '''Get file info. Implements the CheckFileInfo WOPI call'''
        print('Get file info. Implements the CheckFileInfo WOPI call')
        file_path = os.path.join(DOC_ROOT,fileid)
        rf = open(file_path,'rb')
        f = rf.read()
        json_data = {}
        json_data['BaseFileName'] = doc_info.objects.get(path=fileid).name
        json_data['OwnerId'] = 'wrj'
        json_data['Size'] = len(f)
        dig = hashlib.sha256(f).digest()
        json_data['SHA256'] = base64.b64encode(dig).decode()
        json_data['Version'] = '1.0'
        json_data['SupportsUpdate'] = True
        if doc_info.objects.get(path=fileid).edit:
            json_data['UserCanWrite'] = True
        else:
            json_data['UserCanWrite'] = False
        json_data['SupportsLocks'] = True
        json_data['UserFriendlyName'] = email
        return HttpResponse(json.dumps(json_data,ensure_ascii=False), content_type='application/json; charset=utf-8')
    except NameError as e:
        return render(request,'../templates/main.html')

@csrf_exempt
def wopiFileContents(request,fileid='test.txt'):
    '''Request to file contents, Implements the GetFile WOPI call'''
    print('Request to file contents, Implements the GetFile WOPI call')
    file_path = os.path.join(DOC_ROOT,fileid)
    if(request.method == 'GET'):
        print('get file contents',file_path,fileid)
        response=StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename="{0}"'.format(fileid)
        return response
    elif(request.method == 'POST'):
        print('Update file with new contents. Implements the PutFile WOPI call')
        with open(file_path,'wb+') as f:
            f.write(request.body)
            f.close()
        return HttpResponse('')


#此为处理前端js函数
def check_user(request):
    return JsonResponse({"user":email},safe=False)

def delete_doc(request):
    doc_name = request.GET.get("doc_name").replace("+"," ")
    doc_parr = doc_info.objects.get(name=doc_name).path
    doc_submitter = doc_info.objects.get(name=doc_name).submitter
    doc_path = os.path.join(DOC_ROOT, doc_parr)
    try:
        os.remove(doc_path)
        doc_info.objects.get(name=doc_name).delete()
        return JsonResponse({"message":"success"})
    except BaseException as e:
        return JsonResponse({"message": e})

@csrf_exempt
def edit_doc(request):
    if request.method == "GET":
        doc = request.GET.get("doc")
        docinfo = doc_info.objects.get(doc_id=doc)
        docdict = {"doc_id":docinfo.doc_id,
                    "P_Type":docinfo.P_Type,
                   "edit":docinfo.edit,
                   "tag":docinfo.tag,
                   "name":docinfo.name}
        typeinfo = type.objects.filter(Total_Type='P_Type').exclude(Total_Type_values=docinfo.P_Type)
        typelist = []
        for i in typeinfo:
            typelist.append(i.Total_Type_values)
        return JsonResponse({"docinfo":docdict,"typelist":typelist},safe=False)
    else:
        doc_id = request.POST.get("doc_id")
        project = request.POST.get("project")
        edit = request.POST.get("edit")
        tag = request.POST.get("tag")
        if edit == "true":
            edit = True
        else:
            edit = False
        doc_info.objects.filter(doc_id=doc_id).update(P_Type=project,edit=edit,tag=tag)
        return JsonResponse({"message":"done"},safe=False)

@csrf_exempt
def create_doc(request):
    if request.method == "POST":
        doc = request.FILES.get("filename")
        type = request.POST.get("type")
        doc_parr = doc.name.strip()
        doc_parr = doc_parr.replace(" ", "_")
        parrt = {}
        p = Pinyin()
        regex_str = re.compile(".*?([\u4E00-\u9FA5]+).*?")
        match_obj = regex_str.findall(doc_parr)
        for i in match_obj:
            parrt[i] = p.get_initials(i, "")
        for j, k in parrt.items():
            doc_parr = re.sub(j, k, doc_parr)
        ipstamp = request.META["REMOTE_ADDR"].replace(".", "")
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        doc_id = ipstamp + timestamp + doc_parr.split(".")[0]
        try:
            if doc_parr not in [i for i in os.listdir(DOC_ROOT)]:
                if doc_parr.endswith("xlsx") or doc_parr.endswith("xls"):
                    doc_path = os.path.join(DOC_ROOT,doc_parr)
                    destination = open(doc_path, 'wb+')
                    for chunk in doc.chunks():
                        destination.write(chunk)
                    destination.close()
                    doc_info.objects.create(name=doc.name,
                                            path=doc_parr,
                                            type="xlsx",
                                            P_Type=type,
                                            edit=True,submitter=request.session["username"],
                                            tag=type,
                                            create_time=datetime.datetime.now(),
                                            doc_id=doc_id)
                    return redirect('/public_office/')
                else:
                    Message = {"message": "该模块只能上传excel文档！"}
                    return render(request, '../templates/public_office.html', {"message": json.dumps(Message)})
            else:
                Message = {"message": "%s文件名重复，请改名" % doc.name}
                return render(request, '../templates/public_office.html', {"message": json.dumps(Message)})
        except BaseException as e:
            Message = {"message": e}
            return render(request, '../templates/public_office.html', {"message": json.dumps(Message)})

def get_doc(request):
    if request.method == "GET":
        type = request.GET.get("type")
        doc_info_all = doc_info.objects.all().order_by("-create_time")
        Office_Supplies_doc_list = []
        Attendance_statistics_doc_list = []
        Grade_doc_list = []
        wopiserver = setting.objects.get(strings="WOPI_SERVER").string_value
        hostip = setting.objects.get(strings="HOST_IP").string_value
        for doc in doc_info_all:
            Office_Supplies_doc_dict = {}
            Attendance_statistics_doc_dict = {}
            Grade_doc_dict = {}
            if doc.P_Type == "Office_Supplies":
                Office_Supplies_doc_dict["name"] = doc.name
                Office_Supplies_doc_dict["url"] = "http://%s/x/_layouts/xlviewerinternal.aspx?" \
                                                  "ui=zh-CN&rs=zh-CN&WOPISrc=http://%s/wopi/files/%s" % \
                                                  (wopiserver, hostip, doc.path)
                Office_Supplies_doc_dict["createtime"] = doc.create_time.strftime("%Y-%m-%d")
                Office_Supplies_doc_list.append(Office_Supplies_doc_dict)
            elif doc.P_Type == "Attendance_statistics":
                Attendance_statistics_doc_dict["name"] = doc.name
                Attendance_statistics_doc_dict["url"] = "http://%s/x/_layouts/xlviewerinternal.aspx?" \
                                                        "ui=zh-CN&rs=zh-CN&WOPISrc=http://%s/wopi/files/%s" % \
                                                        (wopiserver, hostip, doc.path)
                Attendance_statistics_doc_dict["createtime"] = doc.create_time.strftime("%Y-%m-%d")
                Attendance_statistics_doc_list.append(Attendance_statistics_doc_dict)
            elif doc.P_Type == "Grade":
                Grade_doc_dict["name"] = doc.name
                Grade_doc_dict["url"] = "http://%s/x/_layouts/xlviewerinternal.aspx?" \
                                        "ui=zh-CN&rs=zh-CN&WOPISrc=http://%s/wopi/files/%s" % \
                                        (wopiserver, hostip, doc.path)
                Grade_doc_dict["createtime"] = doc.create_time.strftime("%Y-%m-%d")
                Grade_doc_list.append(Grade_doc_dict)
        if type == "doc_Office_Supplies":
            return JsonResponse({"Office_Supplies":Office_Supplies_doc_list},safe=False)
        elif type == "doc_Attendance_statistics":
            return JsonResponse({"Attendance_statistics": Attendance_statistics_doc_list}, safe=False)
        else:
            return JsonResponse({"Grade": Grade_doc_list}, safe=False)