# -*- encoding:utf-8 -*-
# @author: ZhangYu
# Created on 2017/8/24

from django.conf.urls import include, url

from users.views import UserInfoView, ImageUploadView, UpdatePwdView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, \
    MyMessageView
from users.views import SendEmailCodeView, UpdateEmailView, MyCourseView

urlpatterns = {
    # 个人中心页
    url(r'^user_info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 用户个人中心修改邮箱
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 个人中心我的课程页
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 个人中心我的课程页
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),

    # 个人中心我的收藏页
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav/org'),
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav/teacher'),
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav/course'),
}