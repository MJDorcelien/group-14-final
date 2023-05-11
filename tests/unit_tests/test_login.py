from security import bcrypt
from flask import session
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

    # Check that the user was redirected to the home page
    assert response.headers["Location"] == "/"
    
    #Logout user
    del session['user']


def test_login_route_unhappy_route(test_client: FlaskClient):
    # Make a request to the login page with invalid credentials
    response = test_client.post("/login", data={"username": "invalid_username", "password": "invalid_password"})

    # Check that the response was unsuccessful
    assert response.status_code == 400

    # Check that the response contains the expected error message
    assert "Invalid username or password" in response.data.decode("utf-8")