# -*- conding:utf-8 -*-
from django.urls import path
from . import views
from .views import IndexViews,EastViews,WestViews,FirstViews,first

app_name = 'nba'
urlpatterns = [
    path('',IndexViews.as_view(),name='nba'),
    path('east/',EastViews.as_view(),name='east'),
    path('west/',WestViews.as_view(),name='west'),
    path('homepage/',views.homepage,name='homepage'),
    path('<int:pk>/',first,name='first'),
    path('renew/',views.renew,name='renew'),
    path('predict/', views.predict, name='predict'  )
]