from dutymanager.web.objects import UrlPath
from dutymanager.web import viewers

urlpatterns = [
    UrlPath.add_get('', viewers.index, name='index'),
    UrlPath.add_get('/home', viewers.index),

    UrlPath.add_get('/login', viewers.login, name='login'),
    UrlPath.add_post('/login', viewers.login),
    UrlPath.add_get('/logout', viewers.logout, name='logout'),
]
