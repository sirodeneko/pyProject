"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from . import web
from .web import page
from .web.entity.areaInfo import views

urlpatterns = [
    url(r'^$', page.index),
    url(r'top/', page.top),
    url(r'menu/', page.menu),
    url(r'default/', page.default),
    url(r'areaInfo/fetch', views.fetch),
    url(r'areaInfo/', views.index),
    url(r'singleChart/getData',views.get_single_chart),
    url(r'singleChart/', page.single_chart),
    url(r'multiChart/', page.multi_chart),

]
