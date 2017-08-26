# -*- encoding:utf-8 -*-
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CourseOrg, CityDict, Teacher
from courses.models import Course


# Create your views here.


class OrgListView(View):
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        search_keywords = request.GET.get('keywords', '')
        # 课程搜索
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        org_nums = all_orgs.count()
        # 城市
        all_city = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 取出筛选机构类型
        category = request.GET.get('category', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 取出机构排名类型
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'student_nums':
                all_orgs = all_orgs.order_by('-student_nums')
            elif sort == 'course_nums':
                all_orgs = all_orgs.order_by('-course_nums')

        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_city,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    '''
    机构首页
    '''

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html', {
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCoursesView(View):
    '''
    机构课程列表
    '''

    def get(self, request, org_id):
        current_page = 'courses'
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True
        all_courses = course_org.course_set.all()

        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 5, request=request)
        all_courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            'course_org': course_org,
            'all_courses': all_courses,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    '''
    机构介绍
    '''

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeachersView(View):
    '''
    机构介绍
    '''

    def get(self, request, org_id):
        current_page = 'teachers'
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=int(2)):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teachers': all_teachers,
            'has_fav': has_fav,
        })


class AddFavView(View):
    '''
    用户收藏
    '''

    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '0')

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        else:
            exiist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exiist_records:
                # 记录已经存在
                exiist_records.delete()
                return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
            else:
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.user = request.user
                    user_fav.save()
                    return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self, request):
        all_teachers = Teacher.objects.all()
        search_keywords = request.GET.get('keywords', '')
        # 课程搜索
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    points__icontains=search_keywords))

        order_teachers = all_teachers.order_by('-click_nums')[:5]
        # 取出教师排名类型
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        all_teachers = p.page(page)
        return render(request, 'teacher-list.html', {
            'all_teachers':all_teachers,
            'order_teachers':order_teachers,
            'sort':sort,
        })


class TeacherDetailView(View):
    '''
    课程讲师列表页
    '''
    def get(self, request, teacher_id):
        all_teachers = Teacher.objects.all()
        order_teachers = all_teachers.order_by('-click_nums')[:5]
        teacher = Teacher.objects.get(id=teacher_id)
        work_org = teacher.org

        has_fav_teacher = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.id), fav_type=int(3)):
                has_fav_teacher = True
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(work_org.id), fav_type=int(2)):
                has_fav_org = True

        return render(request, 'teacher-detail.html', {
            'teacher':teacher,
            'work_org':work_org,
            'order_teachers':order_teachers,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
        })

