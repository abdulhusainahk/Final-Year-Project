from django.conf.urls import url
from Tester import views

urlpatterns=[
    url(r'^$',views.home,name='home'),
]