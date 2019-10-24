# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class loginuser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100,null=True)
    P_Type = models.CharField(max_length=100,null=True)
    last_login_time = models.DateTimeField("最后登录时间")
    create_Time = models.DateTimeField("创建时间")


class type(models.Model):
    Total_Type = models.CharField(max_length=100)
    Total_Type_values = models.CharField(max_length=100,null=True)


class exam(models.Model):
    exam_id = models.CharField(max_length=100,null=False)
    T_type = models.CharField(max_length=100)
    content = models.TextField()
    P_Type = models.CharField(max_length=100)
    T_Level = models.CharField(max_length=100,null=True)
    comment = models.TextField(null=True)
    submitter = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    create_Time = models.DateTimeField("创建时间")
    mod_Time = models.DateTimeField('最后修改时间', auto_now=True)

class exam_answers(models.Model):
    exam_id = models.CharField(max_length=100, null=False)
    answers = models.CharField(max_length=100, null=False)
    answers_values = models.BooleanField(null=True)

class test_content(models.Model):
    test_id = models.CharField(max_length=100, null=False)
    P_Type = models.CharField(max_length=100)
    test_time = models.CharField(max_length=100)
    test_range = models.CharField(max_length=100)
    submitter = models.CharField(max_length=100)
    create_time = models.DateTimeField("创建时间")
    correct_rate = models.DecimalField(max_digits=11,decimal_places=2,default=0)

class test_answer(models.Model):
    test_id = models.CharField(max_length=100, null=False)
    exam_id = models.CharField(max_length=100, null=False)
    T_type = models.CharField(max_length=100)
    chose_answer = models.CharField(max_length=100,null=True)
    right_answer = models.CharField(max_length=100,null=True)
    is_right = models.BooleanField(null=True)

class setting(models.Model):
    strings = models.CharField(max_length=100)
    string_value = models.CharField(max_length=100)

class doc_info(models.Model):
    doc_id = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=10000)
    type = models.CharField(max_length=100)
    tag = models.CharField(max_length=100,null=True)
    P_Type = models.CharField(max_length=100)
    edit = models.BooleanField(null=True)
    submitter = models.CharField(max_length=100)
    create_time = models.DateTimeField("创建时间")

class roles(models.Model):
    user_name = models.CharField(max_length=100)
    role_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=100,null=True)

class group_permissions(models.Model):
    name = models.CharField(max_length=100)
    add = models.BooleanField(default=0)
    delete = models.BooleanField(default=0)
    edit = models.BooleanField(default=0)
    query = models.BooleanField(default=0)
    view = models.CharField(max_length=10,null=True)
