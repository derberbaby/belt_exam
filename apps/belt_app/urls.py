from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'register$', views.register, name='register'),
  url(r'login$', views.login, name='login'),
  url(r'logout$', views.logout, name='logout'),
  url(r'travels$', views.travels, name='travels'),
  url(r'travels/add$', views.add, name='add'),
  url(r'add_new$', views.add_new, name='add_new'),
  url(r'destination/(?P<trip_id>\d+)$', views.destination, name='destination'),
  # url(r'enroll$', views.enroll, name='enroll'),
  url(r'join_trip/(?P<trip_id>\d+)$', views.join_trip, name='join_trip'),
  # url(r'drop_class/(?P<course_id>\d+)$', views.drop_class, name='drop_class'),
  # url(r'delete_class/(?P<course_id>\d+)$', views.delete_class, name='delete_class')
]
