from django.conf.urls import url

from matcher.views import index, user_login, register


urlpatterns = [
    url(r'^home/$', index, name='home'),
    url(r'^register/$', register, name='register'),
]
