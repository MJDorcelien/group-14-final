from flask.testing import FlaskClient


def test_signup_page_loads_correctly(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response was successful
    assert response.status_code == 200

    # Check that the response contains the expected content
    assert "Sign Up To Enlighten" in response.data.decode("utf-8")
    assert "Username" in response.data.decode("utf-8")
    assert "Password" in response.data.decode("utf-8")
    assert "Join Your University" in response.data.decode("utf-8")
    assert "Email" in response.data.decode("utf-8")
    assert "Bio" in response.data.decode("utf-8")
    assert "Have An Account" in response.data.decode("utf-8")
    assert "UNC Charlotte" in response.data.decode("utf-8")

def test_signup_page_contains_signup_form(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response contains a form with the expected action and method
    assert "form action = \"/signup\" method = \"post\">" in response.data.decode("utf-8")


# test that a user cannot register twice
def test_signup_page_contains_username_input_field(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response contains an input field with the expected name and placeholder
    assert "<input type=\"text\" class=\"form-control\" name = \"username\" id = \"username\" placeholder=\"Username\" aria-label=\"Username\" aria-describedby=\"basic-addon2\">" in response.data.decode("utf-8")


def test_signup_page_contains_password_input_field(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response contains an input field with the expected name and placeholder
    assert "<input type=\"password\" class=\"form-control\" name = \"password\" id = \"password\" placeholder=\"Password\" aria-label=\"Password\" aria-describedby=\"basic-addon2\">" in response.data.decode("utf-8")


def test_signup_page_contains_signup_button(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response contains a button with the expected text
    assert "<button type=\"submit\" class=\"btn btn-warning\" value = \"signup\" name = \"button\" >Sign Up</button>" in response.data.decode("utf-8")


def test_signup_page_contains_login_link(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response contains a link with the expected text
    assert '<p4>Have An Account<a href=\"/login\" style = \"color:goldenrod;\">Log In</a></p>' in response.data.decode("utf-8")

def test_email_input_field(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response contains a link with the expected text
    assert "<input type=\"email\" class=\"form-control\" name = \"email\" id = \"email\" placeholder=\"Email\" aria-label=\"Email\" aria-describedby=\"basic-addon2\">" in response.data.decode("utf-8")

def test_bio_input_field(test_client: FlaskClient):
    # Make a request to the sign up page
    response = test_client.get("/signup")

    # Check that the response contains a link with the expected text
    assert "<input type=\"text\" class=\"form-control\" name = \"bio\" id = \"bio\" placeholder=\"Bio\" aria-label=\"Bio\" aria-describedby=\"basic-addon2\">" in response.data.decode("utf-8")