from django.urls import path,include
from . import views
# from django.contrib.auth import login

urlpatterns=[
    path('apidataget/',views.index,name='index'),
    path('apidataget/<str:type>/',views.category,name='category'),
    path('apidataget/$',views.search,name='search'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login')
]