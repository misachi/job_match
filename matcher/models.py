import uuid

from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User,Group
from django.db import models

SINGLE = 'single'
MARRIED = 'married'

DEGREE = 'degree'
MASTERS = 'masters'
PHD = 'phd'
TERTIARY_COLLEGE = 'tertiary_college'

ENGINEERING = 'eng'
ACCOUNTING = 'acc'
CATERING = 'cat'
ART = 'art'
MUSIC = 'music'

MARITAL_STATUS = (
    (SINGLE, 'Single'),
    (MARRIED, 'Married')
)

EDUCATION = (
    (DEGREE, 'Degree'),
    (MASTERS, 'Masters'),
    (PHD, 'Phd'),
    (TERTIARY_COLLEGE, 'Tertiary Institution')
)

JOB_TYPE = (
    (ENGINEERING, 'Computer and Engineering'),
    (ACCOUNTING, 'Finance and Accounting'),
    (CATERING, 'Catering'),
    (ART, 'Art'),
    (MUSIC, 'Music')
)


class JobPost(models.Model):
    """
    Holds data related to a particular job
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User)
    category = models.CharField(max_length=20, choices=JOB_TYPE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    requirements = ArrayField(models.CharField(max_length=255), default=list)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Potential(models.Model):
    """
    Holds data for potential employees
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    job_post = models.ForeignKey(JobPost, related_name='potential_jobs')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    dob = models.DateField()
    nationality = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS,
                                      default=SINGLE)
    experience = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(0)])
    edu_level = models.CharField(max_length=20, choices=EDUCATION)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



