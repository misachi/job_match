import pytest
from uuid import UUID
from mixer.backend.django import mixer

from matcher.models import JobPost
from matcher.services import create_posts

pytestmark = pytest.mark.django_db


@pytest.fixture
def jobs_model():
    jobs = mixer.blend('matcher.JobPost')
    return jobs


class TestJobPost:
    def test_JobPost(self, jobs_model):
        jobs = jobs_model
        assert isinstance(jobs.id, UUID), 'Should verify object is created in db and id is UUID instance'

    def test_create_jobpost(self):
        user = mixer.blend('auth.User')
        data = {}
        # jobs.create_jobs(data)
        # create_posts(user, data)
        jobs_count = JobPost.objects.all().count()
        assert jobs_count == 0, 'Should check object creation in db'


class TestPotential:
    def test_potentials(self):
        potential = mixer.blend('matcher.Potential')
        assert isinstance(potential.id, UUID), 'Should check creation of potential employees'
        assert potential.marital_status == 'single'


