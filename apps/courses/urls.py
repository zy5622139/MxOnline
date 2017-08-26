# -*- encoding:utf-8 -*-
# @author: ZhangYu
# Created on 2017/8/24

from django.conf.urls import include, url

from courses.views import CourseListView, CourseDetailView, CourseCaseView, CourseCommentView, AddCommentView

urlpatterns = [
    url(r'^course_list/$', CourseListView.as_view(), name='course_list'),
    url(r'^course_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^course_case/(?P<course_id>\d+)/$', CourseCaseView.as_view(), name='course_case'),
    url(r'^course_comments/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comments'),
    url(r'^course_add_comment/$', AddCommentView.as_view(), name='course_add_comment'),

]