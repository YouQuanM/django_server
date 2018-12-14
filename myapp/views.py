# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.sessions import serializers
from django.core import serializers
import json
# from django.core.serializers import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from myapp import models
from myapp.models import Book, Article_comment ,Article

# 装饰器start
@csrf_protect
@require_http_methods(["GET","POST"])   #允许get,post请求
# 装饰器end

# 登录注册接口
@csrf_exempt
def log_up(request):
    response = {}
    password = request.POST.get('password')
    username = request.POST.get('username')
    email = request.POST.get('email')

    ret = User.objects.filter(username=username)
    print "ret",ret
    if not ret:
        user = User.objects.create_user(username, email,password)
        user.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    else:
        response['msg'] = '用户名已存在'
        response['error_num'] = 1
    return JsonResponse(response)

@csrf_exempt
def log_in(request):
    response = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    print "username",username
    print "password",password
    user = authenticate(username=username, password=password)
    print user
    if user is not None:
        if user.is_active:
            response['msg'] = 'success'
            response['error_num'] = 0
            response['username'] = user.username
            response['userid'] = user.pk
            response['email'] = user.email
        else:
            response['msg'] = 'notactive'
            response['error_num'] = 1
    else:
        response['msg'] = '用户名或密码错误'
        response['error_num'] = 1

    return JsonResponse(response)

# 修改密码接口
@csrf_exempt
def change_password(request):
    response = {}
    userid = request.POST.get('userid')
    user = User.objects.get(pk=userid)
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    userpassword = user.password
    check = check_password(old_password,userpassword)
    if check:
        try:
            user.password = make_password(new_password)
            user.save()
            response['msg'] = 'success'
            response['error_num'] = 0
        except Exception,e:
            response['msg'] = str(e)
            response['error_num'] = 1
    else:
        response['msg'] = '密码错误'
        response['error_num'] = 1

    return JsonResponse(response)

def log_out(request):
    response = {}
    auth.logout(request)
    response['msg'] = 'success'
    response['error_num'] = 0

    return JsonResponse(response)


# 图书接口（以后删除，仅作为测试使用）start
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

def delete_book(request):
    response = {}
    try:
        id = Book.objects.get(id=request.GET.get('id'))
        id.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@csrf_exempt                            #防止post方法csrf报错403
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
# 图书接口（以后删除，仅作为测试使用）end


# 博客接口
# 添加接口
def add_article(request):
    response = {}
    try:
        article = Article(article_title=request.GET.get('article_title'),article_body=request.GET.get('article_body'),article_praise=0,article_user=request.GET.get('article_user'))
        article.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

# 显示接口
def show_articles(request):
    response = {}
    try:
        user = request.GET.get('username','all')
        if user == 'all':
            articles = Article.objects.filter()
        else:
            articles = Article.objects.filter(article_user=user)
        response['list'] = json.loads(serializers.serialize("json", articles))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

# 删除接口
def delete_article(request):
    response = {}
    try:
        id = Article.objects.get(id=request.GET.get('id'))
        id.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

# 点赞接口
def add_praise(request):
    response = {}
    try:
        article_id = request.GET.get('article_id')
        article = Article.objects.get(pk=article_id)
        article.article_praise = article.article_praise+1
        article.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
def add_comment(request):
    response = {}
    article_id = request.POST.get('article_id')
    comment_body = request.POST.get('comment_body')
    comment_username = request.POST.get('comment_username','匿名用户')
    article_comment = Article_comment(article_id=article_id,comment_body=comment_body,comment_username=comment_username)
    article_comment.save()
    response['msg'] = 'success'
    response['error_num'] = 0

    return JsonResponse(response)

def show_comment(request):
    response = {}
    try:
        articles = Article_comment.objects.filter(article_id=request.GET.get('article_id'))
        response['list'] = json.loads(serializers.serialize("json", articles))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)