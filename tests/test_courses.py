from flask.testing import FlaskClient

from flask import session

from src.models import Person, Section, Post, person_section,user_following, db
from src.project_repository import project_repository_singleton

def test_get_all_courses_empty(test_client: FlaskClient):
    
    resp=test_client.post(f'/signup', data={
        'username' : 'bobert',
        'password' : 'abc123',
        'bio' : 'uncle bob',
        'email' : 'b@b.com',
        'university' : 'UNC Charlotte',
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert '<div class="row align-items-start">' in resp.data.decode('utf-8')
    assert '<div class="col">' not in resp.data.decode('utf-8')

def test_get_all_courses_not_empty(test_client: FlaskClient):
    resp=test_client.post(f'/signup', data={
        'username' : 'bobert',
        'password' : 'abc123',
        'bio' : 'uncle bob',
        'email' : 'b@b.com',
        'university' : 'UNC Charlotte',
    }, follow_redirects=True)

    assert resp.status_code == 200

    resp2=test_client.post(f'/join', data={
        'join-class' : 'ITIS 3155',
    }, follow_redirects=True)

    # assert resp2.status_code == 200
