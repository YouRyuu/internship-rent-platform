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
            return redirect('/user/login')

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
    # need modify
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
        # need modify
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
    <!--房屋状态():-->
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
        is_co_rent = request.POST.get('rent_type')
        room_floor = request.POST.get('room_floor')
        room_rent_amount = request.POST.get('room_rent_amount')
        room_size = request.POST.get('room_size')
        room_detail = request.POST.get('room_detail')
        room_name = request.POST.get('room_name')
        # deal room message
        if not all([room_location, room_city, room_district, room_type, room_rent_amount, room_size, room_detail,
                    room_name, room_floor]):
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
        room.floor = room_floor
        room.is_co_rent = is_co_rent
        room.status = 1
        room.state = 0
        room.save()
        return HttpResponse('release ok!')
    return render(request, 'release_rent_msg.html', {'rentee_name': rentee_nickname})


@login_required
def update_rent_msg(request, room_id):
    rentee_tel = request.session.get('tel')
    rentee = User.objects.filter(tel=rentee_tel)
    rentee_nickname = rentee[0].nickname
    room_base_msg_set = Room.objects.filter(user_id=rentee[0].id, id=room_id)
    if len(room_base_msg_set) <= 0:
        return HttpResponse('no this room!')
    else:
        room_base_msg = room_base_msg_set[0]
    if request.method == 'POST':
        # get room message
        room_location = request.POST.get('room_location')
        room_city = request.POST.get('room_city')
        room_district = request.POST.get('room_district')
        room_type = request.POST.get('room_type')
        is_co_rent = request.POST.get('rent_type')
        room_floor = request.POST.get('room_floor')
        room_rent_amount = request.POST.get('room_rent_amount')
        room_size = request.POST.get('room_size')
        room_detail = request.POST.get('room_detail')
        room_name = request.POST.get('room_name')
        # deal room message
        if not all([room_location, room_city, room_district, room_type, room_rent_amount, room_size, room_detail,
                    room_name]):
            return HttpResponse('please complete data!')
        try:
            a = room_base_msg_set.update(location=room_location, city=room_city, district=room_district,
                                         house_type=room_type, rent_amount=room_rent_amount, size=room_size,
                                         detail=room_detail, name=room_name, is_co_rent=is_co_rent, floor=room_floor)
        except:
            a = 0
        if a == 0:
            return HttpResponse('error')
        else:
            return HttpResponse('ok')
    return render(request, 'update_rent_msg.html', {'room_base_msg': room_base_msg})


def show_all_rent_msg(request):
    rooms = Room.objects.filter(status=1)
    return render(request, 'rooms_msg.html', {'rooms': rooms})


def search_room(request):
    '''
    筛选条件: <br>
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
                                        rent_amount__lt=search_price, is_co_rent__contains=search_hz, state=0, status=1)
        else:
            rooms = Room.objects.filter(city__contains=search_city, house_type__contains=search_type,
                                        rent_amount__lt=search_price, is_co_rent=search_hz, floor=search_floor, state=0,
                                        status=1)
        if len(rooms) > 0:
            return render(request, 'rooms_msg.html', {'rooms': rooms})
        return HttpResponse('<script>alert("no result")</script>')
    return render(request, 'rooms_operate/search_rooms.html')


@login_required
def rent_room(request):
    if request.method == 'POST':
        user_tel = request.session.get('tel')
        room_id = request.POST.get('room_id')
        rent_time = request.POST.get('rent_time')
        user_id = User.objects.filter(tel=user_tel)[0].id
        click_room = Order.objects.filter(room_id=room_id)
        if len(click_room) > 0:
            if click_room[0].is_over == 0:
                return HttpResponse('this room is been rent!')
        create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        order = Order()
        order.room_id = room_id
        order.user_id = user_id
        order.create_time = create_time
        order.rent_time = rent_time
        order.is_over = 0
        order.save()
        return HttpResponse('ok')
    return render(request, 'rent_room.html')


@login_required
def order_list(request):
    user_tel = request.session.get('tel')
    user_id = User.objects.filter(tel=user_tel)[0].id
    orders = Order.objects.filter(user_id=user_id)
    rooms = []
    for i in range(len(orders)):
        room_id = orders[i].room_id
        room = Room.objects.filter(id=room_id)
        rooms.append(room)
    # comment = Message.objects.filter(user_id=user_id, room_id=room_id)
    # comment_over = 0
    # if len(comment) > 0:
    #     comment_over = 1
    return render(request, 'order_list.html',
                  {'orders': orders, 'user_id': user_id, 'rooms': rooms})


@login_required
def exit_rent(request):
    '''退租'''
    user_id = request.POST.get('user_id')
    room_id = request.POST.get('room_id')
    order = Order.objects.filter(user_id=user_id, room_id=room_id, is_over=0)
    if len(order) > 0:
        if order[0].is_over == 0:
            order = order[0]
            order.is_over = 1
            order.save()
            return HttpResponse("ok")
        else:
            return HttpResponse("aleady exit this room!")
    return HttpResponse("error")


def room_details(request, room_id):
    room = Room.objects.filter(id=room_id)
    icon = Img.objects.filter(room_id=room_id)
    comments = Message.objects.filter(room_id=room[0].id)
    if len(icon) > 0:
        icon = icon[0].url
    else:
        icon = ''
    if len(room) > 0:
        room = room[0]
        return render(request, 'room_details.html', {'room': room, 'icon': icon, 'comments': comments})
    return HttpResponse('error')


@login_required
def room_comment(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        room_id = request.POST.get('room_id')
        context = request.POST.get('comment')
        create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        comment = Message()
        comment.user_id = user_id
        comment.room_id = room_id
        comment.content = context
        comment.post_time = create_time
        comment.save()
        return redirect('/user/order_list')
    else:
        return redirect('/user/order_list')


@login_required
def release_list(request):
    '''房东 utype = 0'''
    user_tel = request.session.get('tel')
    user_id = User.objects.filter(tel=user_tel)[0].id
    release_rooms = Room.objects.filter(user_id=user_id)
    return render(request, 'release_list.html', {'release_rooms': release_rooms})


@login_required
def user_comments(request):
    user_tel = request.session.get('tel')
    user_id = User.objects.filter(tel=user_tel)[0].id
    comments = Message.objects.filter(user_id=user_id)
    return render(request, 'user_comments.html', {'comments': comments})
