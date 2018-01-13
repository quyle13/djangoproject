from django.conf.urls import patterns, url
from rango import views
from django.conf import settings

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$',views.about,name="About"),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.category,name="Category"),
        url(r'^add_category/$',views.add_category,name = "Add category"),	
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page,name = "Add page"),
        url(r'^register/$',views.register,name="Register"),
        url(r'^login/$',views.user_login,name="User Login"),
        url(r'^logout/$',views.user_logout,name="Logout"),
        )
	
if settings.DEBUG:
	urlpatterns += patterns('django.views.static',(r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),)
