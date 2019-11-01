"""examOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url,include
from exam_online.views import index,main,userlogout,create_exam,exam_temp,iframe_main,my_exam,file_upload\
    ,edit_exam,edit_exam_json,check_exam,delete_exam,start_test,test_record,test_analysis,analysisinfo,\
    check_test,check_doc,upload_doc,edit_user_info,public_office,person_setting,person_meassage,backup_setting,\
    check_user,delete_doc,edit_doc,create_doc,get_doc,edit_project,download_file,create_group
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',index,name='login'),
    url(r'^backup_setting/$', backup_setting, name='backup_setting'),
    url(r'^public_office/$', public_office, name='public_office'),
    url(r'^person_setting/$', person_setting, name='person_setting'),
    url(r'^person_meassage/$', person_meassage, name='person_meassage'),
    url(r'userlogout/$', userlogout, name='user_logout'),
    url(r'edit_user_info/$', edit_user_info, name='edit_user_info'),
    url(r'^main/$',main,name='main'),
    url(r'^create_exam/$',create_exam,name='create_exam'),
    url(r'^exam_temp/$',exam_temp,name='exam_temp'),
    url(r'^iframe_main/$',iframe_main,name='iframe_main'),
    url(r'^my_exam/$',my_exam,name='my_exam'),
    url(r'^edit_exam/$', edit_exam, name='edit_exam'),
    url(r'^check_exam/$', check_exam, name='check_exam'),
    url(r'^check_test/$', check_test, name='check_test'),
    url(r'^delete_exam/$', delete_exam, name='delete_exam'),
    url(r'^start_test/$', start_test, name='start_test'),
    url(r'^test_record/$', test_record, name='test_record'),
    url(r'^test_analysis/$', test_analysis, name='test_analysis'),
    url(r'^check_doc/$', check_doc, name='check_doc'),
    url(r'^upload_doc/$', upload_doc, name='upload_doc'),
    url(r'^edit_exam_json/$', edit_exam_json, name='edit_exam_json'),
    url(r'^analysisinfo/$', analysisinfo, name='analysisinfo'),
    url(r'^edit_doc/$', edit_doc, name='edit_doc'),
    #js url
    url(r'^check_user/$', check_user, name='check_user'),
    url(r'^delete_doc/$', delete_doc, name='delete_doc'),
    url(r'^create_doc/$', create_doc, name='create_doc'),
    url(r'^get_doc/$', get_doc, name='get_doc'),
    url(r'^edit_project/$', edit_project, name='edit_project'),
    url(r'^create_group/$', create_group, name='create_group'),
    #image url
    url(r'^upload/',file_upload),
    url(r'^download_file/$', download_file, name='download_file'),
    url(r'^uploads/(?P<path>.*)$',serve,{'document_root':settings.UPLOAD_ROOT}),
    #office online url
    url(r'^wopi/', include('exam_online.urls')),
]
