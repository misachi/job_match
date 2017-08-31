from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from matcher.models import JobPost, Potential


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


def create_potential(post, data):
    job_obj = JobPost.objects.get(id=post)
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
    print(dict_obj)
    print(job_id)
    foo = JobPost.objects.filter(id=job_id).update(**dict_obj)
    print(foo)


def delete(post_id):
    

