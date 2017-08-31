from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from matcher.models import (
    JobPost,
    Potential,
    JOB_TYPE,
)


def create_user(request, username, email, password):
    User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    user = authenticate(username=username, password=password)
    login(request, user)


def create_posts(user, data):
    print('Were here')
    requirements = data.getlist('requirements')

    start = timezone.make_aware(datetime.strptime(
        data['start_date'], '%m/%d/%Y %H:%M %p'), timezone=timezone.utc)
    end = timezone.make_aware(datetime.strptime(
        (data['end_date']), '%m/%d/%Y %H:%M %p'), timezone=timezone.utc)
    JobPost.objects.create(
        user=user,
        category=data['category'],
        title=data['title'],
        description=data['description'],
        requirements=requirements,
        start_date=start,
        end_date=end
    )


def create_potential(post_id, data):
    job_obj = JobPost.objects.get(id=post_id)
    Potential.objects.create(
        job_post=job_obj,
        first_name=data['fname'],
        last_name=data['lname'],
        phone=data['phone'],
        email=data['email'],
        dob=data['dob'],
        nationality=data['nationality'],
        marital_status=data['marital_status'],
        experience=data['experience'],
        salary=data['salary'],
        edu_level=data['education'],
    )


def update_jobpost(job_id, data):
    dict_obj = {}
    for key, val in data.items():
        if val != '':
            dict_obj[key] = val
    dict_obj.pop('csrfmiddlewaretoken')
    JobPost.objects.filter(id=job_id).update(**dict_obj)


def delete(post_id):
    JobPost.objects.get(id=post_id).delete()


def get_jobs_per_category(category):
    # print([x.category for x in JobPost.objects.all()])
    val = [x[0] for x in JOB_TYPE if x[1] == category]
    jobs = JobPost.objects.filter(category=val[0])
    if not jobs.exists():
        return None
    return jobs





