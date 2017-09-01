from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType

from matcher.models import (
    JobPost,
    Potential,
    JOB_TYPE,
)


def add_user_permissions(user, codename, name, model_obj):
    ct = ContentType.objects.get_for_model(type(model_obj))
    Permission.objects.create(
        codename=codename,
        name=name,
        content_type=ct
    )
    if user.is_active and user.is_staff:
        pass


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
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        email=data['email'],
        dob=data['dob'],
        nationality=data['nationality'],
        marital_status=data['marital_status'],
        experience=data['experience'],
        salary=data['salary'],
        edu_level=data['edu_level'],
    )


def update_jobpost(job_id, data):
    dict_obj = {}
    for key, val in data.items():
        if val != '':
            dict_obj[key] = val

    #  remove csrfmiddlewaretoken as it is not to be saved to database
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


def get_matches(user,  job_id, birth_year, marital_status, experience, salary, edu_level):
    try:
        verify_user = JobPost.objects.get(id=job_id)
    except:
        raise JobPost.DoesNotExist

    if verify_user.user.id != user.id:
        return None
    nationality = 'Kenya'

    birth_yr_q = Q(dob__year__lte=birth_year)
    marital_q = Q(marital_status=marital_status)
    nationality_q = Q(nationality=nationality)
    experience_q = Q(experience__gte=experience)
    salary_q = Q(salary__lte=salary)
    edu_level_q = Q(edu_level=edu_level)

    applicants = Potential.objects.filter(
        birth_yr_q &
        marital_q &
        nationality_q &
        experience_q &
        salary_q &
        edu_level_q
    )

    return applicants

