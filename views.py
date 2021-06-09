from django.shortcuts import render, HttpResponse, redirect
from app01.my_forms.register_forms import Reg_forms
from django.http import JsonResponse
from app01 import models
from django.contrib import auth


# Create your views here.


# 注册view
def register(request):
    form_obj = Reg_forms()
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': ''}
        form_obj = Reg_forms(request.POST)
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data
            clean_data.pop('confirm_password')
            file_obj = request.FILES.get('avatar')
            if file_obj:
                clean_data['avatar'] = file_obj
            models.Userinfo.objects.create_user(**clean_data)
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request, 'register.html', locals())


# 登录view
def login(request):
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': ''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if request.session.get('code').upper() == code.upper():
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                auth.login(request, user_obj)
                back_dic['url'] = '/home/'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)
    return render(request, 'login.html')


# 随机图片三基色
import random


def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# 随机图片验证码
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO, StringIO


def get_code(request):
    img_obj = Image.new('RGB', (605, 35), get_random())
    img_draw = ImageDraw.Draw(img_obj)
    img_font = ImageFont.truetype('static/font/222.ttf', 30)

    code = ''
    for i in range(5):
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        tmp = random.choice([random_int, random_lower, random_upper])
        img_draw.text((i * 90 + 60, 0), tmp, get_random(), img_font)
        code += tmp
    request.session['code'] = code
    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


# 首页view
def home(request):
    article_queryset = models.Article.objects.all()
    return render(request, 'home.html', locals())


# 修改密码view
def set_password(request):
    if request.is_ajax():
        back_dic = {'code': 1000, 'msg': ''}
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            is_right = request.user.check_password(old_password)
            if is_right:
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                else:
                    back_dic['code'] = 1001
                    back_dic['msg'] = '两次密码不一致'
            else:
                back_dic['code'] = 1002
                back_dic['msg'] = '原密码错误'
        return JsonResponse(back_dic)


# 退出登录view
def logout(request):
    auth.logout(request)
    return redirect('home')


# 个人站点
def site(request, username, **kwargs):
    user_obj = models.Userinfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request, 'error.html')
    blog = user_obj.blog
    article_list = models.Article.objects.filter(blog=blog)
    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'category':
            article_list = article_list.filter(category_id=param)
        elif condition == 'tag':
            article_list = article_list.filter(tags__pk=param)
        else:
            year, month = param.split('-')
            article_list = article_list.filter(create_time__year=year, create_time__month=month)
    return render(request, 'site.html', locals())


def article_detail(request, username, article_id):
    user_obj = models.Userinfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request, 'error.html')
    article_obj = models.Article.objects.filter(pk=article_id).first()
    return render(request, 'article_detail.html', locals())
