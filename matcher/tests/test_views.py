import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from matcher.views import user_login

pytestmark = pytest.mark.django_db


class TestLogin:
    def test_login(self):
        user = mixer.blend('auth.User')
        kwargs = {
            'username': user.username,
            'password': user.password
        }
        req = RequestFactory().post('/', data=kwargs)
        resp = user_login(req)
        assert resp.status_code == 400, 'Should check if login is unsuccessful'
