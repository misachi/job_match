from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from matcher.models import JOB_TYPE, JobPost


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'name': 'username',
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'name': 'password',
            }
        )
    )


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'name': 'username',
        }),
        max_length=30,
        required=True,
        help_text='Username may contain <strong>alphanumeric</strong>, <strong>_</strong> and '
                  '<strong>.</strong> characters'
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
            'name': 'email',
        }),
        required=True,
        max_length=75

    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'name': 'password',
        })
    )
    confirmpassword = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'name': 'confirmpassword',
        }),
        required=True
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        confirmpassword = self.cleaned_data.get('confirmpassword')

        if not confirmpassword:
            raise forms.ValidationError('You must Confirm Your password')

        if password != confirmpassword:
            raise forms.ValidationError('Your passwords Do not match!')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmpassword']


class JobPostForm(forms.ModelForm):
    category = forms.ChoiceField(
        label='Category',
        choices=JOB_TYPE,
        initial='',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'category'
        }),
        required=True
    )
    title = forms.CharField(
        label='Job title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Job title',
            'name': 'title'
        })
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Job Description',
            'name': 'description'
        })
    )
    requirements = forms.CharField(
        label='Requirements',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Job requirements',
            'name': 'requirements'
        })
    )
    start_date = forms.DateTimeField(
        label='Start date',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Application start date',
            'name': 'start'
        })
    )
    end_date = forms.DateTimeField(
        label='End Date',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Application end date',
            'name': 'end'
        })
    )

    class Meta:
        model = JobPost
        fields = ['category', 'title', 'description', 'requirements', 'start_date', 'end_date']


class UpdateForm(forms.ModelForm):
    category = forms.ChoiceField(
        label='Category',
        choices=JOB_TYPE,
        initial='',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'category'
        }),
        required=True
    )
    title = forms.CharField(
        label='Job title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Job title',
            'name': 'title'
        })
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Job Description',
            'name': 'description'
        })
    )
    requirements = forms.CharField(
        label='Requirements',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Job requirements',
            'name': 'requirements'
        })
    )
    start_date = forms.DateTimeField(
        label='Start date',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Application start date',
            'name': 'start'
        })
    )
    end_date = forms.DateTimeField(
        label='End Date',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Application end date',
            'name': 'end'
        })
    )

    class Meta:
        model = JobPost
        fields = ['category', 'title', 'description', 'requirements', 'start_date', 'end_date']
