# -*- encoding:utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from MxOnline.settings import MEDIA_ROOT
from organization.views import OrgListView
from users.views import LoginView, IndexView, RegisterView, ActiveView, ForgetView, ResetView, ModifyView, LogoutView

urlpatterns = [
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='active'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),
    url(r'^forget/$', ForgetView.as_view(), name='forget_pwd'),

    # 课程机构
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程
    url(r'^courses/', include('courses.urls', namespace='courses')),

    # 用户
    url(r'^users/', include('users.urls', namespace='users')),

    # 验证码url
    url(r'^captcha/', include('captcha.urls')),

    # 资源文件url
    url(r'^media/(?P<path>.*)/$', serve, {'document_root':MEDIA_ROOT}, name='media'),
]
