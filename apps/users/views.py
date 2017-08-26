# -*- encoding:utf-8 -*-
import json

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetForm, ResetForm, ImageUploadForm, UserInfoForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from utils.mixin_view import LoginRequiredMixin

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': u'用户未激活', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': u'用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'msg': u'用户名或密码错误', 'login_form': login_form})


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return redirect('/login/')
        else:
            return HttpResponse('链接已失效')


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return HttpResponse('链接已失效')


class ModifyView(View):
    def post(self,request):
        reset_form = ResetForm(request.POST)
        email = request.POST.get('email','')
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1!=pwd2:
                return render(request, 'password_reset.html', {'email': email,'msg':'两次输入的密码不一样'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'email': email, 'reset_form': reset_form})


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if not UserProfile.objects.filter(email=email):
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '用户不存在'})
            send_register_email(email, 'forget')
            return HttpResponse('邮件已发送')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '请检查红框内容'})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            new_user = UserProfile()
            new_user.username = email
            new_user.email = email
            new_user.password = make_password(pass_word)
            new_user.is_active = False
            new_user.save()
            # UserProfile.objects.create(username=user_name, password=make_password(pass_word), is_active=False)

            #x写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = new_user.id
            user_message.message = '欢迎注册慕学在线网'
            user_message.save()

            send_register_email(email, 'register')
            return redirect('/login/')
        else:
            return render(request, 'register.html', {'register_form': register_form, 'msg': '请检查红框内容'})


class UserInfoView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def post(self, request):

        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"修改成功"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    '''
    个人中心修改密码
    '''
    def post(self,request):
        modify_form = ResetForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1!=pwd2:
                return HttpResponse('{"status":"fail","msg":"两次密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''
    发送邮箱验证码
    '''
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''
    修改个人邮箱
    '''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = CourseOrg.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id).order_by('has_read')
        unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False).order_by('has_read')
        for msg in unread_message:
            msg.has_read = True
            msg.save()



        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 5, request=request)
        all_message = p.page(page)

        return render(request, 'usercenter-message.html', {
            'all_message': all_message,
        })
