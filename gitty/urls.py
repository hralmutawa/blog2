from django.conf.urls import url
from gitty import views

urlpatterns = [

url(r'^members/$', views.member_list, name='member'),
]