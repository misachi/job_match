from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.contrib.auth import authenticate, login

from matcher.models import (
    JobPost,
    Potential,
    JOB_TYPE,
    SINGLE,
    DEGREE,
    MARRIED
)

EMPLOYER = 'employer'
EMPLOYEE = 'employee'

REG_TYPE = (
    (EMPLOYER, 'Employer'),
    (EMPLOYEE, 'Job seeker')
)


def add_user_permissions(user, permissions):
    """
    
    :param user: Current user object
    :param permissions: all permissions to to user
    :return: None
    """
    # permission_obj = Permission.objects.get(name=permissions)
    if user.is_active:
        result = []
        all_perms = Permission.objects.all()
        for perm in permissions:
            perm_obj = all_perms.get(name=perm)
            result.append(perm_obj)
        user.user_permissions.set(result)


def create_user(request, username, email, password, reg_type, permissions=None):
    user_obj = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    user = authenticate(username=username, password=password)

    """
    Only grant permissions if user is an employer 
    """
    if reg_type == EMPLOYER:
        add_user_permissions(user, permissions)
        user_obj.is_staff = True
        user_obj.save(update_fields=['is_staff'])
    login(request, user)


def create_posts(user, data):
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
    """
    
    :param category: Category of jobs to filter on
    :return: Filtered jobs per category
    """
    try:
        val = [x[0] for x in JOB_TYPE if x[1] == category][0]
    except IndexError:
        val = None
    jobs = JobPost.objects.filter(category=val)
    if not jobs.exists():
        return None
    return jobs


def verify_job(user, job_id):
    """
    
    Method checks if current user created job 
    """
    try:
        verify_user = JobPost.objects.get(id=job_id)
    except:
        return False

    if verify_user.user.id == user.id:
        return True
    else:
        return None


def get_matches(job_id, age, marital_status, experience, salary, edu_level):
    """
    
    :param job_id: post to match
    :param age: minimum required age of applicant
    :param marital_status: married or single
    :param experience: active employment
    :param salary: salary expectations
    :param edu_level: Degree, Masters etc
    :return: Matched applicants for the job
    """
    nationality = 'Kenya'

    today = timezone.make_aware(datetime.today())
    if age is None:
        age = 18

    birth_year = today.year - age

    jobpost_id = Q(job_post_id=job_id)
    birth_yr_q = Q(dob__year__lte=birth_year)
    marital_q = Q(marital_status__in=[marital_status] if marital_status is not None else [SINGLE, MARRIED])
    nationality_q = Q(nationality=nationality)
    experience_q = Q(experience__gte=experience if experience is not None else 0)
    salary_q = Q(salary__lte=salary)
    edu_level_q = Q(edu_level=edu_level if edu_level is not None else DEGREE)

    applicants = Potential.objects.filter(
        jobpost_id &
        birth_yr_q &
        marital_q &
        nationality_q &
        experience_q &
        salary_q &
        edu_level_q
    )

    return applicants

