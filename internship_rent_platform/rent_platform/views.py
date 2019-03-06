from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404
from .models import *
from internship_rent_platform import settings
from django.views.generic import View
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
    rooms = Room.objects.all()
    imgs = Img.objects.all()
    if tel:
        test = {'tel': tel, 'rooms': rooms, 'imgs': imgs}
    else:
        test = {'rooms': rooms, 'imgs': imgs}
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
            return render(request, 'personal.html',
                          {'msg': '!data not complete', 'username': request.session.get('nickname')})
        if old_pwd == new_pwd or new_pwd != re_new_pwd:
            return render(request, 'personal.html',
                          {'msg': 'password not match', 'username': request.session.get('nickname')})
        user_old_pwd_verify = User.objects.filter(tel=request.session.get('tel'), passwd=old_pwd)
        if user_old_pwd_verify:
            user_old_pwd_verify.update(passwd=new_pwd)
        del request.session['isLogin']
        return redirect('/index')
    else:
        return render(request, 'personal.html', {'username': request.session.get('nickname')})


def register(request):
    if request.method == 'POST':
        tel = request.POST['tel']
        password = request.POST['pwd']
        repwd = request.POST.get('repwd')
        nickname = request.POST.get('nickname')
        if not all([tel, password, repwd, nickname]):
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
        user.nickname = nickname
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
            return render(request, 'rooms_operate/find_pwd.html', {'msg': 'data not complete'})
        # this is captcha verify program
        user = User.objects.filter(tel=tel)
        if user:
            user.update(passwd=new_pwd)
            return render(request, 'rooms_operate/find_pwd.html', {'msg': 'find new password success'})
        return render(request, 'rooms_operate/find_pwd.html', {'msg': 'user not exists'})
    else:
        return render(request, 'rooms_operate/find_pwd.html', {'msg': 'testttt'})


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
            return render(request, 'rooms_operate/edit_user_msg.html', {'msg': 'please input data'})
        try:
            a = user.update(nickname=nickname, identify_code=idcard, email=email, utype=type, icon=icon)
        except:
            a = 0
        if a == 1:  # success
            return render(request, 'personal.html', {'msg': 'success edit message'})
        return render(request, 'rooms_operate/edit_user_msg.html', {'msg': 'error data'})
    else:
        user = user[0]
        user_msg = {'user_name': user.nickname, 'user_tel': user.tel, 'user_email': user.email,
                    'user_icon': user.icon,
                    'user_idcard': user.identify_code}
        return render(request, 'rooms_operate/edit_user_msg.html', user_msg)


@login_required
def show_user_msg(request):
    user_tel = request.session.get('tel')
    user = User.objects.filter(tel=user_tel)
    user = user[0]
    user_id = user.id
    orders = Order.objects.filter(user_id=user_id).order_by('is_over')
    rooms = []
    for i in range(len(orders)):
        room_id = orders[i].room_id
        room = Room.objects.filter(id=room_id)
        rooms.append((orders[i], room))
    comments = Message.objects.filter(user_id=user_id)
    user_msg = {'user_name': user.nickname, 'user_id': user_id, 'user_tel': user.tel, 'user_email': user.email,
                'user_icon': user.icon,
                'rooms': rooms, 'comments': comments}
    return render(request, 'personal.html', user_msg)


# room operation
@login_required
def release_rent_msg(request):
    rentee_tel = request.session.get('tel')
    rentee = User.objects.filter(tel=rentee_tel)
    rentee_nickname = rentee[0].nickname
    if request.method == 'POST':
        # get room message
        pic = request.FILES.get('pic')

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

        roompic = UploadImg()
        roompic.pic = "../static/media/images/" + pic.name
        fpath = settings.MEDIA_ROOT + "/images/" + pic.name
        with open(fpath, 'wb') as f:
            for content in pic.chunks():
                f.write(content)
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
        roompic.room_id = room.id
        roompic.save()
        img = Img()
        img.room_id = room.id
        img.url = roompic.pic
        img.save()
        return HttpResponse('release ok!')
    release_rooms = Room.objects.filter(user_id=rentee[0].id)
    return render(request, 'rent-host.html', {'release_rooms': release_rooms})


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
                                         detail=room_detail, name=room_name, is_co_rent=is_co_rent,
                                         floor=room_floor)
        except:
            a = 0
        if a == 0:
            return HttpResponse('error')
        else:
            return HttpResponse('ok')
    return render(request, 'rooms_operate/update_rent_msg.html', {'room_base_msg': room_base_msg})


def show_all_rent_msg(request):
    return search_room(request)


def search_room(request):
    '''
    筛选条件: <br>
    '''
    tel = request.session.get('tel')
    room_type_dict = {'11': '一室', '21': '二室', '31': '三室', '41': '四室', '42': '四室'}
    if request.method == 'POST':
        search_city = request.POST.get('search_city')
        if request.POST.get('jushi') == '不限':
            search_type = '室'
        else:
            search_type = room_type_dict[request.POST.get('jushi')]
        search_price = request.POST.get('money')
        search_floor = request.POST.get('floor')
        search_hz = request.POST.get('hz')
        if search_city == '不限':
            search_city = '北京'
        if search_floor == '不限':
            rooms = Room.objects.filter(city__contains=search_city, house_type__contains=search_type,
                                        rent_amount__lt=search_price, is_co_rent__contains=search_hz, state=0,
                                        status=1)
        else:
            rooms = Room.objects.filter(city__contains=search_city, house_type__contains=search_type,
                                        rent_amount__lt=search_price, is_co_rent=search_hz, floor=search_floor,
                                        state=0,
                                        status=1)
        if len(rooms) > 0:
            imgs = []
            for room in rooms:
                imgs.append(Img.objects.filter(room_id=room.id)[0])
            return render(request, 'choose.html', {'rooms': rooms, 'imgs': imgs, 'tel': tel})
        return render(request, 'choose.html', {'msg': 'no results', 'tel': tel})
    rooms = Room.objects.all()
    imgs = Img.objects.all()
    return render(request, 'choose.html', {'rooms': rooms, 'imgs': imgs, 'tel': tel})


@login_required
def rent_room(request):
    room_id = request.GET.get('roomid')
    user_tel = request.session.get('tel')
    user = User.objects.filter(tel=user_tel)[0]
    if request.method == 'POST':
        # rent_time = request.POST.get('timevalue')
        user_id = user.id
        click_room = Order.objects.filter(room_id=room_id)
        if len(click_room) > 0:
            for r in click_room:
                if r.is_over == 0:
                    return HttpResponse('this room is been rent!')
        create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        order = Order()
        order.room_id = room_id
        order.user_id = user_id
        order.create_time = create_time
        # order.rent_time = rent_time
        order.is_over = 0
        order.save()
        return render(request, 'pay.html')
    try:
        room = Room.objects.get(id=room_id)
        rentee_id = room.user_id
        rentee = User.objects.get(id=rentee_id)
    except Room.DoesNotExist:
        return Http404('ERROR')
    return render(request, 'sign.html', {'room': room, 'rentee': rentee, 'user': user})


@login_required
def order_list(request):
    user_tel = request.session.get('tel')
    user_id = User.objects.filter(tel=user_tel)[0].id
    orders = Order.objects.filter(user_id=user_id)
    order_rooms = []
    for i in range(len(orders)):
        room_id = orders[i].room_id
        room = Room.objects.filter(id=room_id)
        order_rooms.append((orders[i], room))
    # comment = Message.objects.filter(user_id=user_id, room_id=room_id)
    # comment_over = 0
    # if len(comment) > 0:
    #     comment_over = 1

    return render(request, 'personal.html',
                  {'order_rooms': order_rooms})


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
            return redirect(reverse('show_user_msg'))
        else:
            return HttpResponse("aleady exit this room!")
    return HttpResponse("error")


def room_details(request, room_id):
    tel = request.session.get('tel')
    room = Room.objects.filter(id=room_id)
    icon = Img.objects.filter(room_id=room_id)
    comments = Message.objects.filter(room_id=room[0].id)
    images = Img.objects.filter(room_id=room[0].id)
    if len(icon) > 0:
        icon = icon[0].url
    else:
        icon = ''
    if len(room) > 0:
        room = room[0]
        return render(request, 'detail.html',
                      {'images': images, 'tel': tel, 'room': room, 'icon': icon, 'comments': comments})
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
        return redirect('/user/user_msg')
    else:
        return redirect('/index')


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


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
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


def test(request):
    test = [(1, 'a'), (2, 'b')]
    return render(request, 'test.html', {'test': test})
