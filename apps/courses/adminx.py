# -*- encoding:utf-8 -*-
# @author: ZhangYu
# Created on 2017/8/22
import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times','students', 'fav_nums', 'click_nums', 'image', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times','students', 'fav_nums', 'click_nums', 'image']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times','students', 'fav_nums', 'click_nums', 'image', 'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download_file', 'add_time']
    search_fields = ['course', 'download_file', 'name']
    list_filter = ['course', 'name', 'download_file', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)


