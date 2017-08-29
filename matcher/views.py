from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from matcher.services import (
    create_posts,
    create_potential
)
from matcher.forms import RegistrationForm


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
    return render(request, 'matcher/home.html', {})


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
            # _success_msg = 'User {0} added'.format(user.username)
            # feed = Feed(user=user, posts=_success_msg)
            # feed.save()
            return redirect('home')
        else:
            return render(request, 'matcher/register.html', {'form': user_form})
    else:
        user_form = RegistrationForm()

    return render(request, 'matcher/register.html', {'form': user_form})




