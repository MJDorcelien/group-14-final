from flask.testing import FlaskClient

def test_welcome_page(test_client: FlaskClient):
    # Make a request to the login page
    response = test_client.get("/")

    # Check response data has most of the required elements where we can assume
    # Everything loaded correctly
    assert "Welcome to Enlighten!" in response.data.decode("utf-8")
    assert "We make staying in the loop look easy!" in response.data.decode("utf-8")
    assert "Make an account or login to get started." in response.data.decode("utf-8")
    assert "Make an account or login to get started." in response.data.decode("utf-8")
    assert "<a class=\"btn btn-lg btn-outline-warning mt-3\" href=\"/login\">Login</a>" in response.data.decode("utf-8")
    assert "<a class=\"btn btn-lg btn-outline-warning mt-3\" href=\"/signup\">Sign Up</a>" in response.data.decode("utf-8")

def test_status_code_is_200(test_client: FlaskClient):
    response = test_client.get('/')
    assert response.status_code == 200