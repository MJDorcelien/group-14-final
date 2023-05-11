from flask.testing import FlaskClient

def test_page_loads_correctly(test_client: FlaskClient):
    # Make a request to the login page
    response = test_client.get("/login")

    # Check that the response was successful
    assert response.status_code == 200

    # Check that the response contains the expected content
    assert "Login To Enlighten" in response.data.decode("utf-8")
    assert "Username" in response.data.decode("utf-8")
    assert "Password" in response.data.decode("utf-8")
    assert "Log In" in response.data.decode("utf-8")
    assert "Sign Up" in response.data.decode("utf-8")


def test_page_contains_login_form(test_client: FlaskClient):
    # Make a request to the login page
    response = test_client.get("/login")

    # Check that the response contains a form with the expected action and method
    # Error here
    assert "<form action = \"/login\" method = POST>" in response.data.decode("utf-8")


def test_page_contains_username_input_field(test_client: FlaskClient):
    # Make a request to the login page
    response = test_client.get("/login")

    # Check that the response contains an input field with the expected name and placeholder
    # Error Here
    assert "<input type=\"text\" class=\"form-control\" name = \"username\" id = \"username\" placeholder=\"Username\" aria-label=\"Username\" aria-describedby=\"basic-addon2\">" in response.data.decode("utf-8")


def test_page_contains_password_input_field(test_client: FlaskClient):
    # Make a request to the login page
    response = test_client.get("/login")

    # Check that the response contains an input field with the expected name and placeholder
    assert "<input type=\"password\" class=\"form-control\" name = \"password\" id = \"password\" placeholder=\"Password\" aria-label=\"Password\" aria-describedby=\"basic-addon2\">" in response.data.decode("utf-8")


def test_page_contains_login_button(test_client: FlaskClient):
    # Make a request to the login page
    response = test_client.get("/login")

    # Check that the response contains a button with the expected text
    assert "<button type=\"submit\" class=\"btn btn-warning\" value = \"login\" name = \"button\">Log In</button>" in response.data.decode("utf-8")


def test_page_contains_signup_link(test_client: FlaskClient):
    # Make a request to the login page
    response = test_client.get("/login")

    # Check that the response contains a link with the expected text
    assert "<p4>Don't Have An Account? <a href=\"/signup\" style = \"color:goldenrod;\">Sign Up</a></p4>" in response.data.decode("utf-8")
