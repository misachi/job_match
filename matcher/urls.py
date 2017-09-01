from django.conf.urls import url

from matcher.views import (
    user_login,
    register,
    create_jobs,
    view_job,
    update_post,
    get_jobs,
    save_potential,
    delete_post,
    get_matched_applicants,

)

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^create_jobs/$', create_jobs, name='create_job'),
    url(r'view_post/$', view_job, name='view_job'),
    url(r'^update_post/(?P<post_id>[\w-]+)/$', update_post, name='update'),
    url(r'^get_category/$', get_jobs, name='get_category'),
    url(r'^save_potential/(?P<job_id>[\w-]+)/$', save_potential, name='potential'),
    url(r'^delete_post/(?P<job_id>[\w-]+)/$', delete_post, name='delete'),
    url(r'^matched/(?P<job_id>[\w-]+)/$', get_matched_applicants, name='matched'),
]
