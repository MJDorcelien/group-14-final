from security import bcrypt
from flask.testing import FlaskClient
from src.models import db, Person

def test_login_route_happy_route(test_client: FlaskClient):
    # Create a user in the database
    person = Person(user_name='testuser', email = 'testemail@gmail.com', bio = 'testbio', university = 'testuniversity', password= bcrypt.generate_password_hash('testpassword').decode('utf-8'))
    db.session.add(person)
    db.session.commit()

    # Make a request to the login page with valid credentials
    response = test_client.post("/login", data={"username": "testuser", "password": "testpassword"})

    # Check that the response was successful
    assert response.status_code == 302

    # Check that the user was redirected to the courses page
    assert response.headers["Location"] == "/courses"
    

def test_login_route_unhappy_route(test_client: FlaskClient):
    # Make a request to the login page with invalid credentials
    response = test_client.post("/login", data={"username": "invalid_username", "password": "invalid_password"})
    page_data = response.data.decode()

    # Check that the response was unsuccessful, and we are redirected to login again
    assert response.status_code == 302 
    
    

