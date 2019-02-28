from django.urls import path
from django.conf.urls import url, include
from rent_platform import  views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^change_pwd$', views.change_pwd),
    url(r'^logout$', views.logout),
    url(r'^find_pwd$', views.find_pwd),
    url(r'^edit_user_msg$', views.edit_user_msg),
    url(r'^release_rent_msg$', views.release_rent_msg),
    url(r'^user_msg$', views.show_user_msg),
    url(r'^rooms_msg$', views.show_all_rent_msg),
    url(r'^search_room$', views.search_room),
    url(r'^rent_room$', views.rent_room),
    url(r'^order_list$', views.order_list),

]