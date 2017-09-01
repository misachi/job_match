from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from matcher.models import JobPost, Potential, JOB_TYPE,MARITAL_STATUS, EDUCATION


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


class PotentialForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
            'name': 'first_name'
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
            'name': 'last_name'
        })
    )
    phone = forms.CharField(
        label='phone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'phone',
            'name': 'phone'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'name': 'email'
        })
    )
    dob = forms.DateField(
        label='Birth Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Data of birth DD/MM/YYYY',
            'name': 'dob'
        })
    )
    nationality = forms.CharField(
        label='Nationality',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Place of birth',
            'name': 'nationality'
        })
    )
    marital_status = forms.ChoiceField(
        label='Status',
        choices=MARITAL_STATUS,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'marital_status',
        })
    )
    edu_level = forms.ChoiceField(
        label='Education',
        choices=EDUCATION,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'edu_level',
        })
    )
    experience = forms.IntegerField(
        label='Experience',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Work experience',
            'name': 'experience'
        })
    )
    salary = forms.DecimalField(
        label='Salary',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Salary expectations',
            'name': 'salary'
        })
    )

    class Meta:
        model = Potential
        fields = ['first_name', 'last_name', 'phone', 'email', 'dob', 'nationality', 'marital_status', 'experience', 'salary', 'edu_level']


class SearchForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=JOB_TYPE,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-live-search': 'true',
            'name': 'category'
        })
    )

    class Meta:
        model = JobPost
        fields = ['category']


class MatchedForm(forms.ModelForm):
    age = forms.IntegerField(
        label='Age',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum required age',
            'name': 'age'
        }),
    )
    marital_status = forms.ChoiceField(
        label='Marital status',
        choices=MARITAL_STATUS,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'marital_status'
        }),
    )
    experience = forms.IntegerField(
        label='Experience',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum work experience',
            'name': 'experience'
        }),
    )
    salary = forms.DecimalField(
        label='Salary',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum salary expectations',
            'name': 'salary'
        }),
    )
    edu_level = forms.ChoiceField(
        label='Education',
        choices=EDUCATION,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'edu_level',
        }),
    )

    class Meta:
        model = Potential
        fields = ['age', 'marital_status', 'experience', 'salary', 'edu_level']
