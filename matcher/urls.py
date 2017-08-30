from django.conf.urls import url

from matcher.views import index, user_login, register


urlpatterns = [
    url(r'^register/$', register, name='register'),
]
