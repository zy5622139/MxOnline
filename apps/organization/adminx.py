# -*- encoding:utf-8 -*-
# @author: ZhangYu
# Created on 2017/8/22
import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'fav_nums', 'click_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'fav_nums', 'click_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'fav_nums', 'click_nums', 'image', 'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums',
                    'add_time']
    search_fields = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums', ]
    list_filter = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'click_nums',
                   'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
