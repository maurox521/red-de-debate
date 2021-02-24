from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^resumen/', views.index, name='index'),
    url(r'^closedIndex/$', views.closedIndex, name='closedIndex'),
    url(r'^tag/(?P<slug>[-\w]+)/$', views.tagged, name='tagged'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^search/', views.searchView, name='searchView'),

]
