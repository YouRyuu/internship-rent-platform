from django.urls import path
from django.conf.urls import url, include
from rent_platform import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # url(r'^userview/login$', views.LoginView.as_view(), name='login'),
    url(r'^index$', views.index, name='index'),
    url(r'^user/login$', views.login, name='login'),
    url(r'^user/register$', views.register, name='register'),
    url(r'^user/change_pwd$', views.change_pwd, name='change_pwd'),
    url(r'^user/logout$', views.logout, name='logout'),
    url(r'^user/find_pwd$', views.find_pwd, name='find_pwd'),
    url(r'^user/edit_user_msg$', views.edit_user_msg, name='edit_user_msg'),
    url(r'^user/user_msg$', views.show_user_msg, name='show_user_msg'),
    url(r'^user/release_list$', views.release_list),
    url(r'^user/order_list$', views.order_list),
    url(r'^user/user_comments$', views.user_comments),
    url(r'^room/release_rent_msg$', views.release_rent_msg),
    url(r'^room/update_rent_msg/(?P<room_id>\d+)$', views.update_rent_msg),
    url(r'^room/rooms_msg$', views.show_all_rent_msg),
    url(r'^room/search_room$', views.search_room, name='search_room'),
    url(r'^room/rent_room$', views.rent_room),
    url(r'^room/exit_rent$', views.exit_rent),
    url(r'^room/room_comment$', views.room_comment),
    url(r'room/(?P<room_id>\d+)$', views.room_details),
    url(r'^$', views.index),
]
