#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'wopiserver'
urlpatterns = [
    url(r'^files/(?P<fileid>[^/]+)$',views.wopiGetFileInfo),
    url(r'^files/(?P<fileid>[^/]+)/contents$',views.wopiFileContents),

]