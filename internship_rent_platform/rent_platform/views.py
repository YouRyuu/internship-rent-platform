from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages


# Create your views here.

def login_required(func):
    '''
    :param func:
    :return:
    '''

    def wrapper(request, *args, **kwargs):
        if request.session.has_key('isLogin'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')

    return wrapper


def index(request):
    nickname = request.session.get('nickname')
    if nickname:
        test = {'name': nickname}
    else:
        test = None
    return render(request, 'index.html', test)


def login(request):
    if request.method == 'POST':
        tel = request.POST['tel']
        pwd = request.POST['password']
        if not all([tel, pwd]):
            return render(request, 'login.html', {'msg': 'not complete data'})
        user = User.objects.filter(tel=tel, passwd=pwd)
        if len(user) > 0:  # success
            request.session['isLogin'] = True
            request.session['nickname'] = user[0].nickname
            request.session['tel'] = user[0].tel
            return redirect('/index')
        else:  # fail
            return render(request, 'login.html', {'msg': 'Error tel or pwd'})
    else:
        return render(request, 'login.html')


@login_required
def change_pwd(request):
    if request.method == 'POST':
        old_pwd = request.POST.get('oldpwd')
        new_pwd = request.POST.get('newpwd')
        re_new_pwd = request.POST.get('repwd')
        if not all([old_pwd, new_pwd, re_new_pwd]):
            return render(request, 'change_pwd.html', {'msg': '!data not complete', 'username':request.session.get('nickname')})
        if old_pwd == new_pwd or new_pwd != re_new_pwd:
            return render(request, 'change_pwd.html', {'msg': 'password not match', 'username':request.session.get('nickname')})
        user_old_pwd_verify = User.objects.filter(tel=request.session.get('tel'), passwd=old_pwd)
        if user_old_pwd_verify:
            user_old_pwd_verify.update(passwd=new_pwd)
        del request.session['isLogin']
        return render(request, 'index.html', {'msg': 'change_pwd_success'})
    else:
        return render(request, 'change_pwd.html', {'username':request.session.get('nickname')})


def register(request):
    if request.method == 'POST':
        tel = request.POST['tel']
        password = request.POST['pwd']
        repwd = request.POST.get('repwd')
        # captcha = request.POST['captcha']
        if not all([tel, password, repwd]):
            return render(request, 'register.html', {'msg': 'data not complete'})
        if password != repwd:
            return render(request, 'register.html', {'msg': 'password not same'})
        try:
            user = User.objects.get(tel=tel)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'msg': 'user already exists'})
        user = User()
        user.tel = tel
        user.passwd = password
        user.save()
        return render(request, 'login.html')
    else:
        return render(request, 'register.html')

def logout(request):
    request.session.clear()
    return render(request, 'index.html')
