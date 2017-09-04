import pytest
from uuid import uuid4
from django.core import mail
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404

from matcher.views import (register, create_jobs, update_post, index, delete_post,
                           view_job, get_jobs, save_potential, get_matched_applicants,
                           send_invitation_email)
from matcher.forms import RegistrationForm
from matcher.models import JOB_TYPE, DEGREE, SINGLE

pytestmark = pytest.mark.django_db


@pytest.fixture
def db_user():
    user = mixer.blend('auth.User')
    return user


@pytest.fixture
def db_jobpost(db_user):
    post = mixer.blend('matcher.JobPost', user=db_user)
    return post


@pytest.fixture
def db_potential(db_jobpost):
    potential = mixer.blend('matcher.Potential', job_post=db_jobpost)
    return potential


class TestAuthentication:
    def test_index(self):
        req = RequestFactory().get('/')
        res = index(req)
        assert res.status_code == 200, 'Should check if home page works as desired'
        assert b'Home' in res.content

    def test_register_invalid_form(self):
        req = RequestFactory().post('/')
        resp = register(req)
        assert resp.status_code == 200, 'Should check form is invalid'

    def test_register_get_method(self):
        req = RequestFactory().get('/')
        resp = register(req)
        assert resp.status_code == 200, 'Should check empty form returned if method GET is used'

    def test_register(self, db_user):
        data = {
            'username': 'name',
            'email': 'abc@gmail.com',
            'password': 'pass',
            'confirmpassword': 'pass',
            'reg_type': 'employer'
        }
        user = db_user

        #  Here Forms return is_valid as false if no data is passed to constructor
        reg_form = RegistrationForm(data, instance=user)
        req = RequestFactory().post('/', data=data)

        """
        RequestFactory does not support sessions. Here we simulate a logged in user by setting the logged in user manually This is well explained in the documentation which states that
        'it(RequestFactory) does not support middleware. Session and authentication attributes must be supplied by the test
         itself if required for the view to function properly.'. Another way would be use the SessionMiddleware explicitly to simulate a session as  shown
            from django.contrib.sessions.middleware import SessionMiddleware
            middleware = SessionMiddleware()
            middleware.process_request(req)
            req.session.save()
        """
        from django.contrib.sessions.middleware import SessionMiddleware
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        # req.user = user
        resp = register(req)
        assert reg_form.is_valid() is True
        assert '/' in resp.url, 'Should check if redirect url is home'
        assert resp.status_code == 302, 'Should check successful registration and redirect to home page'

    def test_create_jobs_get_method(self, db_user):
        user = db_user
        req = RequestFactory().get('/')
        req.user = user
        req.user.is_superuser = True
        resp = create_jobs(req)
        assert resp.status_code == 200, 'Should get method returns empty form'

    def test_create_jobs(self, db_user):
        user = db_user
        data = {
            'category': 'category',
            'title': 'title',
            'description': 'desc',
            'requirements': 'req',
            'start_date': '9/2/2017 10:30 am',
            'end_date': '10/2/2017 10:30 pm'
        }
        req = RequestFactory().post('/', data=data)
        req.user = AnonymousUser()
        assert 'login' in create_jobs(req).url, 'Should check user not logged in is redirected to login page'

        req.user = user
        assert create_jobs(req).status_code == 403, 'Should return error if user does not have permissions'

        req.user.is_superuser = True
        resp = create_jobs(req)
        assert resp.status_code == 302, 'Should redirect to home page after job creation'
        assert '/' in resp.url, 'Should check if redirect url is home'

    def test_update_post_get_method(self, db_user, db_jobpost):
        user = db_user
        post = db_jobpost
        req = RequestFactory().get('/')
        req.user = user
        req.user.is_superuser = True
        resp = update_post(req, post.id)
        assert resp.status_code == 200, 'Should check get returns empty form'

    def test_update_post(self, db_user, db_jobpost):
        user = db_user
        post = db_jobpost
        data = {
            'csrfmiddlewaretoken': 'token'
        }
        req = RequestFactory().post('/', data=data)
        req.user = AnonymousUser()
        assert 'login' in update_post(req, post.id).url, 'Should check user not logged in is redirected to login page'

        req.user = user
        assert update_post(req, post.id).status_code == 403, 'Should return error if user does not have permissions'

        req.user.is_superuser = True
        resp = update_post(req, post.id)
        assert '/' in resp.url, 'Should check if redirect url is home'
        assert resp.status_code == 302, 'Should confirm redirect after update'

    def test_delete_post_not_exist(self, db_user, db_jobpost):
        req = RequestFactory().post('/')
        req.user = db_user
        req.user.is_superuser = True
        random_uuid = uuid4()
        resp = delete_post(req, random_uuid)
        assert isinstance(resp, Http404), 'Should check Http404 error thrown when object does not exist'

    def test_delete_post(self, db_user, db_jobpost):
        user = db_user
        post = db_jobpost
        req = RequestFactory().post('/')
        req.user = AnonymousUser()
        assert 'login' in delete_post(req, post.id).url, 'Should check user not logged in is redirected to login page'

        req.user = user
        assert delete_post(req, post.id).status_code == 403, 'Should return error if user does not have permissions'

        req.user.is_superuser = True
        resp = delete_post(req, post.id)
        assert resp.status_code == 200, 'Should check successful deletion'

    def test_view_jobs(self, db_jobpost):
        post = db_jobpost
        req = RequestFactory().post('/', data={'job_id': post.id})
        # req = RequestFactory().post('/', data={'category': post.category})
        # req.user = user
        resp = view_job(req)
        assert resp.status_code == 200, 'Should successfully load page to be viewed by user'

    def test_get_jobs_404(self, db_jobpost):
        post = db_jobpost
        req = RequestFactory().post('/', data={'category': post.category})
        resp = get_jobs(req)
        assert isinstance(resp, Http404), 'Should check 404 error if object does not exist'

    def test_get_jobs(self, db_jobpost):
        post = db_jobpost
        category = [x[1] for x in JOB_TYPE if x[0] == post.category]
        req = RequestFactory().post('/', data={'category': category})
        resp = get_jobs(req)
        assert resp.status_code == 200, 'Should check matched jobs are returned'

    def test_save_potential_form_invalid(self, db_jobpost):
        req = RequestFactory().post('/')
        resp = save_potential(req, db_jobpost.id)
        assert resp.status_code == 200, 'Should check empty form loaded successfully when form is invalid'
        assert b'Save Potential Employee' in resp.content, 'Should check correct page loaded when form is invalid'

    def test_save_potential_get_method(self, db_jobpost):
        req = RequestFactory().get('/')
        resp = save_potential(req, db_jobpost.id)
        assert resp.status_code == 200, 'Should check 200 status code for empty form loaded when get method is used'
        assert b'Save Potential Employee' in resp.content, 'Should check correct page loaded when get method is used'

    def test_save_potential(self, db_jobpost):
        post = db_jobpost
        data = {
            'first_name': 'fname',
            'last_name': 'lname',
            'phone': '28377324',
            'email': 'abc@gmail.com',
            'dob': '5/4/1994',
            'nationality': 'Kenya',
            'marital_status': 'single',
            'experience': 4,
            'salary': 1000,
            'edu_level': 'masters'
        }
        req = RequestFactory().post('/', data=data)
        resp = save_potential(req, post.id)
        assert resp.status_code == 302, 'Should check that user saves profile and redirects to home'

    def test_get_matched_applicants(self, db_user, db_jobpost, db_potential):
        user = db_user
        post = db_jobpost
        data = {
            'salary': 1000,
            'age': 20,
            'marital_status': SINGLE,
            'experience': 3,
            'edu_level': DEGREE
        }
        req = RequestFactory().post('/', data=data)
        req.user = user
        req.user.is_superuser = True
        resp = get_matched_applicants(req, post.id)
        assert resp.status_code == 200, 'Should check matching applicants are returned to user'
        assert b'Matched' in resp.content, 'Should check correctness of matched url'

        data = {
            'salary': 1000,
            'marital_status': SINGLE,
            'experience': 3,
            'edu_level': DEGREE
        }
        req = RequestFactory().post('/', data=data)
        req.user = user
        req.user.is_superuser = True
        resp = get_matched_applicants(req, post.id)
        assert resp.status_code == 200, 'Should check if age not in payload age is set to constant 18'

    def test_get_matched_applicants_get_method(self,  db_user,  db_jobpost):
        req = RequestFactory().get('/')
        req.user = db_user
        req.user.is_superuser = True
        resp = get_matched_applicants(req, db_jobpost.id)
        assert resp.status_code == 200, 'Should check correct page loaded when wrong request method is used'
        assert b'Applications' in resp.content, 'Should check correctness of page loaded when wrong request method is used'

    def test_get_matched_applicants_invalid_form(self, db_user,  db_jobpost):
        user = db_user
        post = db_jobpost
        data = {}
        req = RequestFactory().post('/', data=data)
        req.user = AnonymousUser()
        resp = get_matched_applicants(req, post.id)
        assert resp.status_code == 302, 'Should check user not logged in can"t access the view function'
        assert 'login' in resp.url, 'Should check not logged in user redirected to login page'

        req.user = user
        resp = get_matched_applicants(req, post.id)
        assert resp.status_code == 403, 'Should check logged in user without view permissions cannot view applicants'

        req.user.is_superuser = True
        resp = get_matched_applicants(req, post.id)
        assert resp.status_code == 200, 'Should check matching applicants are returned to user'
        assert b'Applications' in resp.content, 'Should check correctness of matched url'

        resp = get_matched_applicants(req, uuid4())
        assert isinstance(resp, Http404), 'Should check that post if post does not exist, 404 error is returned'

        random_user = mixer.blend('auth.User')
        req.user = random_user
        req.user.is_superuser = True
        resp = get_matched_applicants(req, post.id)
        assert resp.status_code == 403, 'Should check that user that did not create a post cannot get applicants for the post'

    def test_send_invitation_email(self, db_user, db_potential):
        user = db_user
        potential = db_potential
        req = RequestFactory().post('/', data={'mail': potential.id})
        req.user = AnonymousUser()
        assert 'login' in send_invitation_email(req).url, 'Should check user not logged in is redirected to login page'
        req.user = user
        req.user.is_superuser = True
        resp = send_invitation_email(req)
        assert resp.status_code == 200, 'Should check email sent successfully'
        assert len(mail.outbox) == 1, 'Should verify email is sent to recipient'
