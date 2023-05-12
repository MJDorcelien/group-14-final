from flask.testing import FlaskClient
from src.models import db, Person
from security import bcrypt

def test_signup_route_happy_route(test_client: FlaskClient):
    # Create a user in the database
    person = Person(user_name='testuser', email = 'testemail@gmail.com', bio = 'testbio', university = 'testuniversity', password= bcrypt.generate_password_hash('testpassword').decode())
    db.session.add(person)
    db.session.commit()

    # Make a request to the sign up page with valid credentials
    response = test_client.post("/signup", data={"username": "testuser", "password": "testpassword", "email" : "testemail@gmail.com", "bio" : "testbio", "university":"testuniversity"})

    # Check that the response was successful
    assert response.status_code == 302

    # Check that the user was redirected to the home page
    assert response.headers["Location"] == "/courses"


def test_signup_route_unhappy_route(test_client: FlaskClient):
    # Make a request to the sign up page with invalid credentials
    response = test_client.post('/signup', data={"username": "wronguser", "password": "wrongpass"})
    page_data = response.data.decode()

    # Check that the response was unsuccessful
    assert response.status_code == 400