from django.conf.urls import url

from matcher.views import (
    index,
    user_login,
    register,
    create_jobs,
    view_job
)


urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^create_jobs/$', create_jobs, name='create_job'),
    url(r'view_post/$', view_job, name='view_job')
]
