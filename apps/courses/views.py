# -*- encoding:utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import View

from courses.models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_view import LoginRequiredMixin


# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        search_keywords = request.GET.get('keywords', '')
        # 课程搜索
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        # 取出课程排名类型
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)
        all_courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': all_courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    '''
    课程详情页
    '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()
        tag = course.tag
        relate_courses = []

        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=int(2)):
                has_fav = True

        has_fav_course = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=int(1)):
                has_fav = True
        if tag:
            relate_courses = Course.objects.filter(tag=tag).order_by('-click_nums')[:2]
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_org': has_fav_org,
            'has_fav_course': has_fav_course,
        })


class CourseCaseView(LoginRequiredMixin, View):
    '''
    课程章节信息页
    '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询该用户是否关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resources = CourseResource.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出学生学过的其他课程id
        course_ids = {user_course.course.id for user_course in all_user_courses}
        course_ids.remove(course.id)
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:4]
        return render(request, 'course-case.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    '''
    课程章节信息页
    '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询该用户是否关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出学生学过的其他课程id
        course_ids = {user_course.course.id for user_course in all_user_courses}
        course_ids.remove(course.id)
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:4]
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    '''
    用户添加课程评论
    '''

    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '0')

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        else:
            course_id = int(request.POST.get('course_id', '0'))
            comments = request.POST.get('comments', '')

            if course_id and comments.strip() != '':
                course_comments = CourseComments()
                course = Course.objects.get(id=course_id)
                course_comments.course = course
                course_comments.comments = comments
                course_comments.user = request.user
                course_comments.save()
                return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')
