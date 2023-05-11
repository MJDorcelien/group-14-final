from flask.testing import FlaskClient

from src.models import Person, Section, Post, person_section,user_following, db
from src.project_repository import project_repository_singleton
import datetime


def test_get_all_posts_empty(test_client: FlaskClient):
    
    resp=test_client.post(f'/signup', data={
        'username' : 'britany',
        'password' : 'abc123',
        'bio' : 'uncle bob',
        'email' : 'b@b.com',
        'university' : 'UNC Charlotte',
    }, follow_redirects=True)

    assert resp.status_code == 200

    resp2=test_client.post(f'/join', data={
        'join-class' : 'ITIS 3155',
    }, follow_redirects=True)

    assert resp2.status_code == 200

    resp3=test_client.get('/courses')
    assert resp3.status_code == 200

    person=project_repository_singleton.get_user_by_name('britany')
    person_id=person.person_id
    sections=project_repository_singleton.get_user_courses(person_id)
    for section in sections:
        section_id=section.section_id
    print(section_id)

    course=project_repository_singleton.get_sections_by_id(section_id)
    response = test_client.get(f'/courses/{section_id}')
    assert response.status_code == 200

    data = response.data.decode('utf-8')
    assert '<h3>ITIS 3155 Course Chat</h3>' in data
    assert '<button type="submit" class="btn btn-warning">Edit</button>' not in data

def test_posts_not_empty(test_client: FlaskClient):
    
    resp=test_client.post(f'/signup', data={
        'username' : 'jessica',
        'password' : 'abc123',
        'bio' : 'uncle bob',
        'email' : 'b@b.com',
        'university' : 'UNC Charlotte',
    }, follow_redirects=True)

    assert resp.status_code == 200

    resp2=test_client.post(f'/join', data={
        'join-class' : 'ITIS 3146',
    }, follow_redirects=True)

    assert resp2.status_code == 200

    resp3=test_client.get('/courses')
    assert resp3.status_code == 200

    person=project_repository_singleton.get_user_by_name('jessica')
    person_id=person.person_id
    sections=project_repository_singleton.get_user_courses(person_id)
    for section in sections:
        section_id=section.section_id
    print(section_id)

    course=project_repository_singleton.get_sections_by_id(section_id)
    response = test_client.get(f'/courses/{section_id}')
    assert response.status_code == 200

    date=datetime.datetime.now()
    post=project_repository_singleton.create_post(person_id,section_id,date,"new message")
    print(project_repository_singleton.get_all_posts())
    response2 = test_client.get(f'/courses/{section_id}')
    print(post)
    print()

    assert response2.status_code == 200

    data = response2.data.decode('utf-8')
    assert '<h3>ITIS 3146 Course Chat</h3>' in data
    assert '<button type="submit" class="btn-sm btn-danger">Delete</button>' in data
    assert '<h4>No posts have been made</h4>' not in data

def test_edit_post(test_client: FlaskClient):
    resp=test_client.post(f'/signup', data={
        'username' : 'jessica',
        'password' : 'abc123',
        'bio' : 'uncle bob',
        'email' : 'b@b.com',
        'university' : 'UNC Charlotte',
    }, follow_redirects=True)

    assert resp.status_code == 200

    resp2=test_client.post(f'/join', data={
        'join-class' : 'ITIS 3146',
    }, follow_redirects=True)

    assert resp2.status_code == 200

    resp3=test_client.get('/courses')
    assert resp3.status_code == 200

    person=project_repository_singleton.get_user_by_name('jessica')
    person_id=person.person_id
    sections=project_repository_singleton.get_user_courses(person_id)
    for section in sections:
        section_id=section.section_id
    print(section_id)

    course=project_repository_singleton.get_sections_by_id(section_id)
    response = test_client.get(f'/courses/{section_id}')
    assert response.status_code == 200

    date=datetime.datetime.now()
    post=project_repository_singleton.create_post(person_id,section_id,date,"new message")
    print(project_repository_singleton.get_all_posts())
    response2 = test_client.get(f'/courses/{section_id}')
    print(post)
    print()

    assert response2.status_code == 200

    response3=test_client.get(f'/courses/{post.post_id}/messages/edit')
    assert response3.status_code == 200
    
    data=response3.data.decode('utf-8')
    assert '<h5 class="text-white">Old Message:</h5>' in data

    response4=test_client.post(f'/courses', data={
        'post-id' : post.post_id,
        'new-message' : 'this is a new message',
    }, follow_redirects=True)
    assert response4.status_code == 200 

    response5=test_client.post(f'/courses/{post.post_id}/messages/delete', follow_redirects=True)
    assert response5.status_code == 200

    data = response5.data.decode('utf-8')
    assert '<h3>ITIS 3146 Course Chat</h3>' in data
    assert '<button type="submit" class="btn btn-warning">Edit</button>' not in data
