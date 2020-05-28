from dutymanager.web import views
from dutymanager.web.objects import UrlPath

urlpatterns = [
    UrlPath.add_get('', views.pages.index, name='index'),
    UrlPath.add_get('/home', views.pages.index),
    UrlPath.add_get('/help', views.pages.help, name='help'),

    UrlPath.add_get('/admin', views.admin.admin, name='admin'),
    UrlPath.add_post('/admin', views.admin.api),

    UrlPath.add_get('/login', views.pages.login, name='login'),
    UrlPath.add_post('/login', views.pages.login),
    UrlPath.add_get('/logout', views.pages.logout, name='logout'),

    UrlPath.add_get('/install', views.pages.install, name='install'),
    UrlPath.add_post('/install', views.pages.install),
]
