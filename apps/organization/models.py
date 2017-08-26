# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'城市名称')
    desc = models.CharField(max_length=300, verbose_name=u'城市描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(max_length=20, choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')),
                                verbose_name='机构类别', default='pxjg')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    student_nums = models.IntegerField(default=0, verbose_name=u'学生人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程人数')
    click_nums = models.IntegerField(default=0, verbose_name=u'机构点击数')
    image = models.ImageField(upload_to='image/course_org/%Y/%m', max_length=100, verbose_name=u'封面图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    # 获取课程机构教室数量
    def get_teacher_nums(self):
        return self.teacher_set.all()

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    name = models.CharField(max_length=20, verbose_name=u'教师名字')
    desc = models.CharField(max_length=100, verbose_name=u'教师简介', default='')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name=u'教师点击数')
    image = models.ImageField(upload_to='image/teacher/%Y/%m', max_length=100, verbose_name=u'封面图', null=True,
                              blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    age = models.IntegerField(default=18, verbose_name=u'收藏人数')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def get_courses(self):
        return self.course_set.all()

    def __unicode__(self):
        return self.name
