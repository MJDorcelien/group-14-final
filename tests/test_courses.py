from flask.testing import FlaskClient

def test_get_all_courses_empty(test_client: FlaskClient):
    
    resp=test_client.post(f'/signup', data={
        'username' : 'bobert',
        'password' : 'abc123',
        'bio' : 'uncle bob',
        'email' : 'b@b.com',
        'university' : 'UNC Charlotte',
    }, follow_redirects=True)

    assert resp.status_code == 200

    data = resp.data.decode('utf-8')
    assert '<h3 class="text-white">No Courses Added</h3>' in data
    assert '<div class="col">' not in data

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

    assert resp2.status_code == 200

    resp3=test_client.get('/courses')
    assert resp3.status_code == 200

    data = resp3.data.decode('utf-8')
    assert '<div class="col">' in data
    assert '<h5 class="card-title text-start text-white">ITIS 3155</h5>' in data
    assert '<h3 class="text-white">No Courses Added</h3>' not in data


