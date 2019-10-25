#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponseRedirect, HttpResponse,redirect
from .models import roles

#验证用户是否登录，没有登录的话，自动跳转到登录界面，登录后再跳转会登录前访问的界面，用来取代login_required
class user_login_required(MiddlewareMixin):
    def process_request(self,request):
        if not request.session.has_key('username') and request.path != "/":
            if "/wopi/files/" in request.path:
                pass
            else:
                return HttpResponseRedirect('/?next=%s'%request.path)
        elif not request.session.has_key('username') and request.path == "/":
            pass
        elif request.session.has_key('username') and request.path != "/":
            username = request.session["username"]
            request.session["role"] = roles.objects.get(user_name=username).role_name
