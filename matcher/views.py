import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from matcher.services import (
    create_posts,
    create_potential
)
from matcher.forms import RegistrationForm, JobPostForm
from matcher.models import JobPost, Potential


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            login(request, user)
        except:
            return HttpResponseBadRequest

        return redirect('/')
    return HttpResponseNotAllowed


def index(request):
    jobs = JobPost.objects.all().order_by('-created')
    paginator = Paginator(jobs, 12)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    context = {
        'all_jobs': jobs,
    }
    return render(request, 'matcher/home.html', context)


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'matcher/register.html', {'form': user_form})
    else:
        user_form = RegistrationForm()

    return render(request, 'matcher/register.html', {'form': user_form})


@login_required(login_url='login')
@transaction.atomic
def create_jobs(request):
    if request.method == 'POST':
        jobs_form = JobPostForm(request.POST)
        user = request.user
        data = request.POST
        create_posts(user, data)
        return redirect('home')
        # if jobs_form.is_valid():
        #
        # else:
        #     render(request, 'matcher/post.html', {'form': jobs_form})
    else:
        jobs_form = JobPostForm()
    return render(request, 'matcher/post.html', {'form': jobs_form})


def view_job(request):
    job_id = request.POST.get('job_id')
    # print(job_id)
    # print(request.POST)
    job = JobPost.objects.get(id=job_id)
    # data = json.dumps([x for x in job])
    # print(data)
    # return JsonResponse(json.loads(data), safe=False)
    return render(request, 'matcher/display.html', {'details': job})

def get_jobs(request, category):
    pass




