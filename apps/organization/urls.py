# -*- encoding:utf-8 -*-
# @author: ZhangYu
# Created on 2017/8/24

from django.conf.urls import include, url

from organization.views import OrgListView, AddUserAskView, OrgHomeView, OrgCoursesView, OrgDescView, OrgTeachersView, \
    AddFavView, TeacherListView, TeacherDetailView

urlpatterns = [
    # 机构列表页
    url(r'^org_list/$', OrgListView.as_view(), name='org_list'),
    url(r'^user_ask/$', AddUserAskView.as_view(), name='user_ask'),
    url(r'^org_home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^org_courses/(?P<org_id>\d+)/$', OrgCoursesView.as_view(), name='org_courses'),
    url(r'^org_desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teachers/(?P<org_id>\d+)/$', OrgTeachersView.as_view(), name='org_teachers'),

    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 讲师列表页
    url(r'^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]