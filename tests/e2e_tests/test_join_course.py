from flask.testing import FlaskClient
from src.models import db, Person, Section
from src.project_repository import project_repository_singleton

def test_get_join_class_empty(test_client:FlaskClient):
    #Login User
    test_client.post(f'/signup', data={
        'username' : 'dev',
        'password' : 'abc123',
        'bio' : "cs is so fun!",
        'university' : "UNCC",
        'email' : "dev@uncc.edu" 
    }, follow_redirects=True)
    
    res = test_client.get('/join')
    page_data = res.data.decode()
    
    assert res.status_code == 200
    assert '<p>No joined classes!</p><br>' in page_data
    

def test_post_join_class(test_client: FlaskClient):
#setup
    
    #Create a user and a class
    #Login User
    res = test_client.post(f'/signup', data={
        'username' : 'dev',
        'password' : 'abc123',
        'bio' : "cs is so fun!",
        'university' : "UNCC",
        'email' : "dev@uncc.edu" 
    }, follow_redirects=True)
    
    assert res.status_code == 200 
    
   
    
    resp2 = test_client.post('/join', data={
        'join-class' : 'ITIS 3155',
    }, follow_redirects=True)
    
    assert resp2.status_code == 200
    
    res = test_client.get('/join')
    page_data = res.data.decode()
    
    #Make sure the class shows up in page data
    assert res.status_code == 200
    assert '<p>ITIS 3155</p><br>' in page_data
    

    
    
    
    