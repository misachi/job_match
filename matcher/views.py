from django.shortcuts import render, redirect
from django.http import (
    HttpResponseForbidden,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from matcher.services import (
    create_user,
    create_posts,
    create_potential,
    update_jobpost,
    delete,
    get_jobs_per_category
)
from matcher.forms import RegistrationForm, JobPostForm, UpdateForm, PotentialForm, SearchForm
from matcher.models import JobPost


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

            #  All transactions must be committed to database i.e all or nothing
            with transaction.atomic():
                create_user(request, username, email, password)

            return redirect('home')
        else:
            return render(request, 'matcher/register.html', {'form': user_form})
    else:
        user_form = RegistrationForm()

    return render(request, 'matcher/register.html', {'form': user_form})


@login_required(login_url='login')
def create_jobs(request):
    if not request.user.has_perm('matcher.add_jobpost'):
        return HttpResponseForbidden('User cannot create job post')
    if request.method == 'POST':
        jobs_form = JobPostForm(request.POST)
        user = request.user
        data = request.POST
        with transaction.atomic():
            create_posts(user, data)
        return redirect('home')
    else:
        jobs_form = JobPostForm()
    return render(request, 'matcher/post.html', {'form': jobs_form})


@login_required(login_url='login')
def update_post(request, post_id):
    user = request.user
    if not user.has_perm('matcher.change_jobpost'):
        return HttpResponseForbidden('User not allowed to edit post')

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        data = request.POST
        with transaction.atomic():
            update_jobpost(post_id, data)
        return redirect('home')
    else:
        form = UpdateForm()
        job_data = JobPost.objects.get(id=post_id)
    return render(request, 'matcher/update.html', {'form': form, 'job_data': job_data})


@login_required(login_url='login')
def delete_post(request, post_id):
    user = request.user
    if not user.has_perm('matcher.delete_jobpost'):
        return HttpResponseForbidden('Users not allowed to delete post')

    try:
        delete(post_id)
    except JobPost.DoesNotExist:
        pass


def view_job(request):
    job_id = request.POST.get('job_id')
    job = JobPost.objects.get(id=job_id)
    return render(request, 'matcher/display.html', {'details': job})


def get_jobs(request):
    """
    
    :param request: 
    :param category: 
    Description: retrieves posts based on specific categories 
    """
    print('Amen!')
    # if request.method == 'POST':
    #     search_form = SearchForm(request.POST)
    #     if search_form.is_valid():
    #         category = search_form.cleaned_data.get('category')
    #         jobs = get_jobs_per_category(category)
    #
    #         if jobs is None:
    #             return HttpResponseBadRequest('Jobs matching query do not exist')
    #         return redirect('home')
    #     else:
    #         return render(request, 'matcher/home.html', {'form': search_form})
    # else:
    # search_form = SearchForm()
    category = request.POST.get('category')
    jobs = get_jobs_per_category(category)

    if jobs is None:
        return HttpResponseBadRequest('Jobs matching query do not exist')

    return render(request, 'matcher/categories.html', {'jobs': jobs})


def save_potential(request):
    if request.method == 'POST':
        pot_form = PotentialForm(request.POST)
        if pot_form.is_valid():
            post_id = pot_form.cleaned_data.get('post_id')
            data = pot_form.cleaned_data
            with transaction.atomic():
                create_potential(post_id, data)
            return redirect('home')
        else:
            render(request, 'matcher/potential.html', {'form': pot_form})
    else:
        pot_form = PotentialForm()
    return render(request, 'matcher/potential.html', {'form': pot_form})


