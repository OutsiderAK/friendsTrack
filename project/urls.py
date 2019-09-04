"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, re_path
from django.contrib import admin
from proj_twit import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', views.RenderMainPage.as_view()),
    path('login/', views.RenderLoginPage.as_view()),
    path('logout/', views.LogoutUser.as_view()),
    path('register/', views.RegisterUser.as_view()),
    path('comments/<int:id>', views.RenderComments.as_view()),
    path('messages/', views.RenderMessages.as_view()),
    path('easter_egg/', views.easter_egg)

]
