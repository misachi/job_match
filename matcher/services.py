from matcher.models import JobPost, Potential


def create_posts(user, data):
    JobPost.objects.create(
        user=user,
        category=data['category'],
        title=data['title'],
        description=data['description'],
        requirements=data['requirements'],
        start_date=data['start'],
        end_date=data['end']
    )


def create_potential(post, data):
    job_obj = JobPost.objects.get(id=post)
    Potential.objects.create(
        job_post=job_obj,
        first_name=data['fname'],
        last_name=data['lname'],
        phone=data['phone'],
        email=data['email'],
        dob=data['dob'],
        nationality=data['nationality'],
        marital_status=data['marital_status'],
        experience=data['experience'],
        salary=data['salary'],
        edu_level=data['education'],
    )
