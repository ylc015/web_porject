from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'polls'


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^detail/(?P<user_key>\w+)/$', views.detail, name='detail'),
	url(r'about/$', views.aboutView, name='about'),
	url(r'^about_edit/$', views.updateUser, name='about_edit'),

    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),


	url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),


	#invite function
	url(r'^invite_user/$', views.invite_user, name='invite_user'),

	url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),



]


