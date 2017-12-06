from django.conf.urls import url
from twitty import views

urlpatterns = [

url(r'^search/$', views.tweet_search, name='search'),

]