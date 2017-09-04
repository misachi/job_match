from django.shortcuts import render, redirect
from django.http import (
    HttpResponseForbidden,
    Http404,
    HttpResponse
)
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from matcher.services import (
    create_user,
    create_posts,
    create_potential,
    update_jobpost,
    delete,
    get_jobs_per_category, get_matches, verify_job,
)
from matcher.forms import (RegistrationForm, JobPostForm,
                           UpdateForm, PotentialForm, SearchForm, MatchedForm)
from matcher.models import (JobPost, DEGREE, MASTERS, PHD,
                            TERTIARY_COLLEGE, SINGLE, MARRIED)

SUBJECT = 'YOUR JOB APPLICATION'
MESSAGE = 'Greetings applicant, we are happy to inform you that you have been ' \
          'shortlisted for this position. ' \
          'We hereby invite for an interview tomorrow at 1000hrs.'


def index(request):
    """
    Home page view
    :param request:  
    """
    jobs = JobPost.objects.all().order_by('-created')
    paginator = Paginator(jobs, 4)
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
            reg_type = user_form.cleaned_data.get('reg_type')

            permissions = ['Can view potential employees applications',
                           'Can change job post', 'Can delete job post',
                           'Can add job post']

            #  All transactions must be committed to database i.e all or nothing
            with transaction.atomic():
                create_user(request, username, email, password,
                            reg_type, permissions)

            return redirect('home')
        else:
            # return HttpResponseBadRequest()
            return render(request, 'matcher/register.html', {'form': user_form})
    else:
        user_form = RegistrationForm()

    return render(request, 'matcher/register.html', {'form': user_form})


@login_required(login_url='login')
def create_jobs(request):
    """
    Permissions: only users with add_jobpost permission can create new job posts
    :param request:  
    """
    if not request.user.has_perm('matcher.add_jobpost'):
        return HttpResponseForbidden('User not authorised to create job post')
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
    """
    Permissions: only users with change_jobpost permission can update new job posts
    :param request: 
    :param post_id: id for post to update
    :return: 
    """
    user = request.user
    if not user.has_perm('matcher.change_jobpost'):
        return HttpResponseForbidden('User not authorised to edit post')

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
    """
    Permissions: only users with delete_jobpost permission can delete job posts
    :param request: 
    :param post_id: job post to delete 
    """
    user = request.user
    if not user.has_perm('matcher.delete_jobpost'):
        return HttpResponseForbidden('User not authorised to delete post')
    # post = delete(post_id)
    # if not post:
    #     return Http404()
    # return HttpResponse()

    try:
        delete(post_id)
    except JobPost.DoesNotExist:
        raise Http404()
    return HttpResponse()


def view_job(request):
    job_id = request.POST.get('job_id')
    job = JobPost.objects.get(id=job_id)
    return render(request, 'matcher/display.html', {'details': job})


def get_jobs(request):
    """
    
    :param request: 
    Description: retrieves posts based on given categories 
    """

    category = request.POST.get('category')
    jobs = get_jobs_per_category(category)

    if jobs is None:
        raise Http404()

    return render(request, 'matcher/categories.html', {'jobs': jobs})


def save_potential(request, job_id):
    """
    
    :param request: 
    :param job_id: the id of the job being applied for
    Description: Method creates details for all applicants
    """
    if request.method == 'POST':
        pot_form = PotentialForm(request.POST)
        if pot_form.is_valid():
            data = pot_form.cleaned_data
            with transaction.atomic():
                create_potential(job_id, data)
            return redirect('home')
        else:
            render(request, 'matcher/potential.html', {'form': pot_form})
    else:
        pot_form = PotentialForm()
    return render(request, 'matcher/potential.html', {'form': pot_form})


@login_required(login_url='login')
def get_matched_applicants(request, job_id):
    """
    
    :param request: 
    :param job_id: id for the specified job post
    :return: list of matched job posts
    """
    user = request.user
    if not user.has_perm('matcher.can_view_potential'):
        return HttpResponseForbidden('User not authorised to view applications')

    """
    User should choose at least 3 parameters to filter applicants
    """
    verify = verify_job(user, job_id)

    if verify == False:
        raise Http404()

    if verify is None:
        return HttpResponseForbidden('This is not your job post. Please look '
                                     'for post that you have created')
    if request.method == 'POST':
        app_form = MatchedForm(request.POST)
        if app_form.is_valid():
            age = app_form.cleaned_data.get('age')
            marital_status = app_form.cleaned_data.get('marital_status')
            experience = app_form.cleaned_data.get('experience')
            salary = app_form.cleaned_data.get('salary')
            edu_level = app_form.cleaned_data.get('edu_level')

            applicants = get_matches(job_id, age, marital_status,
                                     experience, salary, edu_level)

            return render(request, 'matcher/matched.html', {'applicants': applicants})
        else:
            return render(request, 'matcher/applications.html', {'form': app_form})
    else:
        app_form = MatchedForm()

    return render(request, 'matcher/applications.html', {'form': app_form})


@login_required(login_url='login')
def send_invitation_email(request):
    """
    
    :param request: 
    :return: empty HttpResponse object
    """
    from matcher.models import Potential
    app_id = request.POST['mail']

    applicant = Potential.objects.get(id=app_id)

    sender = request.user.email
    send_mail(SUBJECT, MESSAGE, sender, [applicant.email])
    return HttpResponse()
