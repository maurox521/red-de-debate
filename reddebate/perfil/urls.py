from django.conf.urls import url, include

from . import views

# ex: /polls/5/
urlpatterns = [

	#url(r'^post_arg$', views.post_arg, name='post_arg'),
	#url(r'^(?P<id_debate>[0-9]+)/$', views.showDebate, name='showDebate'),
    url(r'^(?P<id_usr>[0-9]+)/$', views.username, name='username'),
    url(r'^alias/(?P<alias>[-\w]+)/$', views.alias, name='alias'),
    url(r'^debates$', views.userDebates, name='debates'),
    url(r'^listas$', views.userList, name='userList'),
    url(r'^list/(?P<id_list>[0-9]+)/$', views.memberList, name='memberList'),
    url(r'^', include('resumen.urls', namespace='resumen'))
]
