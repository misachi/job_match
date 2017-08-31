from django.conf.urls import url

from matcher.views import (
    user_login,
    register,
    create_jobs,
    view_job,
    update_post

)


urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^create_jobs/$', create_jobs, name='create_job'),
    url(r'view_post/$', view_job, name='view_job'),
    url(r'^update_post/(?P<post_id>[\w-]+)/$', update_post, name='update'),
    # url(r'^update_post/$', update_post, name='update'),
]
