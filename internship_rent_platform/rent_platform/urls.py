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
]