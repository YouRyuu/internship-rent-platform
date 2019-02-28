from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import time


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
    tel = request.session.get('tel')
    if tel:
        test = {'tel': tel}
    else:
        test = None
    return render(request, 'index.html', test)


# user operation
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
            return render(request, 'change_pwd.html',
                          {'msg': '!data not complete', 'username': request.session.get('nickname')})
        if old_pwd == new_pwd or new_pwd != re_new_pwd:
            return render(request, 'change_pwd.html',
                          {'msg': 'password not match', 'username': request.session.get('nickname')})
        user_old_pwd_verify = User.objects.filter(tel=request.session.get('tel'), passwd=old_pwd)
        if user_old_pwd_verify:
            user_old_pwd_verify.update(passwd=new_pwd)
        del request.session['isLogin']
        return render(request, 'index.html', {'msg': 'change_pwd_success'})
    else:
        return render(request, 'change_pwd.html', {'username': request.session.get('nickname')})


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
    return render(request, 'register.html')


def logout(request):
    request.session.clear()
    return redirect('/index')


def find_pwd(request):
    if request.method == 'POST':
        tel = request.POST['tel']
        captcha = request.POST['captcha']
        new_pwd = request.POST['new_password']
        if not all([tel, captcha, new_pwd]):
            return render(request, 'find_pwd.html', {'msg': 'data not complete'})
        # this is captcha verify program
        user = User.objects.filter(tel=tel)
        if user:
            user.update(passwd=new_pwd)
            return render(request, 'find_pwd.html', {'msg': 'find new password success'})
        return render(request, 'find_pwd.html', {'msg': 'user not exists'})
    else:
        return render(request, 'find_pwd.html', {'msg': 'testttt'})


@login_required
def edit_user_msg(request):
    user = User.objects.filter(tel=request.session.get('tel'))
    if request.method == 'POST':
        nickname = request.POST['nickname']
        email = request.POST['email']
        idcard = request.POST['idcard']
        type = request.POST.get('type')
        icon = request.POST['icon']
        if not any([nickname, email, idcard, type, icon]):
            return render(request, 'edit_user_msg.html', {'msg': 'please input data'})
        try:
            a = user.update(nickname=nickname, identify_code=idcard, email=email, utype=type, icon=icon)
        except:
            a = 0
        if a == 1:  # success
            return render(request, 'edit_user_msg.html', {'msg': 'success edit message'})
        return render(request, 'edit_user_msg.html', {'msg': 'error data'})
    else:
        user = user[0]
        user_msg = {'user_name': user.nickname, 'user_tel': user.tel, 'user_email': user.email, 'user_icon': user.icon,
                    'user_idcard': user.identify_code}
        return render(request, 'edit_user_msg.html', user_msg)


@login_required
def show_user_msg(request):
    user_tel = request.session.get('tel')
    user = User.objects.filter(tel=user_tel)
    user = user[0]
    user_msg = {'user_name': user.nickname, 'user_tel': user.tel, 'user_email': user.email, 'user_icon': user.icon}
    return render(request, 'user_msg.html', user_msg)


# room operation
@login_required
def release_rent_msg(request):
    '''
    <!--房东-->
    房屋地址: <input type="text" name="room_addr"> <br>
    房屋城市: <input type="text" name="room_city"> <br>
    所在区: <input type="text" name="room_area"> <br>
    房屋类型: <input type="text" name="room_type"> <br>
    租金价格: <input type="text" name="room_price"> <br>
    <!-- 纬度-->:
    <!-- 经度:-->
    房屋大小: <input type="text" name="room_size"> <br>
    <!--是否合租-->:
    房屋细节: <input type="text" name="room_details"> <br>
    <!--房屋排名:-->
    房屋名称: <input type="text" name="room_name"> <br>
    <!--房屋状态(发布是否成功):-->
    :param request:
    :return:
    '''
    rentee_tel = request.session.get('tel')
    rentee = User.objects.filter(tel=rentee_tel)
    rentee_nickname = rentee[0].nickname
    if request.method == 'POST':
        # get room message
        room_location = request.POST.get('room_location')
        room_city = request.POST.get('room_city')
        room_district = request.POST.get('room_district')
        room_type = request.POST.get('room_type')
        room_rent_amount = request.POST.get('room_rent_amount')
        room_size = request.POST.get('room_size')
        room_detail = request.POST.get('room_detail')
        room_name = request.POST.get('room_name')
        # deal room message
        if not all([room_location, room_city, room_district, room_type, room_rent_amount, room_size, room_detail,
                    room_name]):
            return HttpResponse('please complete data!')
        rentee_id = rentee[0].id
        room = Room()
        room.location = room_location
        room.user_id = rentee_id
        room.city = room_city
        room.district = room_district
        room.house_type = room_type
        room.rent_amount = room_rent_amount
        room.size = room_size
        room.detail = room_detail
        room.name = room_name
        room.save()
        return HttpResponse('release ok!')
    return render(request, 'release_rent_msg.html', {'rentee_name': rentee_nickname})


def show_all_rent_msg(request):
    rooms = Room.objects.all()
    return render(request, 'rooms_msg.html', {'rooms': rooms})


def search_room(request):
    '''
    筛选条件: <br>
    地理位置: 城市<input type="text" name="search_city"> <br>
            小区<input type="text" name="search_community"> <br>
    户型: <p>1shi1ting：<input type="radio" name="type" value="11"></p>
         <p>2shi1ting：<input type="radio" name="type"  value="21"></p>
         <p>3shi1ting：<input type="radio" name="type"  value="31"></p>
         <p>4shi1ting：<input type="radio" name="type"  value="41"></p>
         <p>4shi2ting：<input type="radio" name="type"  value="42"></p>
    价格: <p>0~1000<input type="radio" name="price" value="1000"></p>
         <p>1001~2000<input type="radio" name="price"  value="2000"></p>
         <p>2001~3000<input type="radio" name="price"  value="3000"></p>
         <p>3001~4000<input type="radio" name="price"  value="4000"></p>
         <p>4000+<input type="radio" name="price"  value="4001"></p>
    楼层: <input type="text" name="search_floor"> <br>
    是否合租: <p>是：<input type="radio" name="hz" value="1"></p>
             <p>否：<input type="radio" name="hz"  value="0"></p><br>
    '''
    room_type_dict = {'11': '一室一厅', '21': '二室一厅', '31': '三室一厅', '41': '四室一厅', '42': '四室二厅'}

    if request.method == 'POST':
        search_city = request.POST.get('search_city')
        search_type = room_type_dict[request.POST.get('roomtype')]
        search_price = request.POST.get('price')
        search_floor = request.POST.get('search_floor')
        search_hz = request.POST.get('hz')
        if search_floor is '':
            rooms = Room.objects.filter(city__contains=search_city, house_type__contains=search_type,
                                        rent_amount__lt=search_price, is_co_rent__contains=search_hz)
        else:
            rooms = Room.objects.filter(city__contains=search_city, house_type__contains=search_type,
                                        rent_amount__lt=search_price, is_co_rent=search_hz, floor=search_floor)
        if len(rooms) > 0:
            return render(request, 'rooms_msg.html', {'rooms': rooms})
        return HttpResponse('not result')
    return render(request, 'rooms_operate/search_rooms.html')


@login_required
def rent_room(request):
    if request.method == 'POST':
        user_tel = request.session.get('tel')
        room_id = request.POST.get('room_id')
        rent_time = request.POST.get('rent_time')
        user_id = User.objects.filter(tel=user_tel)[0].id
        is_exist = Order.objects.filter(user_id=user_id, room_id=room_id)
        if len(is_exist) > 0:
            return HttpResponse('you have already rent this room!')
        create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        order = Order()
        order.room_id = room_id
        order.user_id = user_id
        order.create_time = create_time
        order.rent_time = rent_time
        order.save()
        return HttpResponse('ok')
    return render(request, 'rent_room.html')


@login_required
def order_list(request):
    user_tel = request.session.get('tel')
    user_id = User.objects.filter(tel=user_tel)[0].id
    orders = Order.objects.filter(user_id=user_id)
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def exit_rent(request):
    '''退租'''
    pass
