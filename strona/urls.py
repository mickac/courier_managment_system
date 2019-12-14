from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from . import views

app_name='strona'
urlpatterns = [
    path('<int:pk>/delete', views.delete, name='delete'),
    path('search', views.searchresultview, name='search_results'),
    path('packagelist', views.package_list, name='packagelist'),
    path('deliveredlist', views.deliveredpackages_list, name='deliveredlist'),
    path('packageadd', views.package_add, name='packageadd'),
    path('<int:pk>/package_delivered', views.package_delivered, name='package_delivered'),
    path('removedpackage', views.removedpackages_list, name='removedpackage'),
    path('removedpackagesearch', views.removedpackages_searchlist, name='removedpackagesearch'),
]