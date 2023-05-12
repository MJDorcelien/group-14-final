from flask.testing import FlaskClient
from src.models import db, Person
from src.project_repository import get_user_followers, get_user_following, create_user_follow

def test_follow(test_client: FlaskClient):
    # Create a user in the database
    user_a = Person(user_name='testuser_a', email = 'testemail@gmail.com', bio = 'testbio', university = 'testuniversity', password='password')
    user_b = Person(user_name='testuser_a', email = 'testemail@gmail.com', bio = 'testbio', university = 'testuniversity', password='password')
    db.session.add(user_a)
    db.session.add(user_b)
    db.session.commit()

    followers_a = get_user_followers(user_a.person_id)
    following_b = get_user_following(user_b.person_id)

    # check user_a has no followers
    assert len(followers_a) == 0

    # check user_b has no followees
    assert len(following_b) == 0

    create_user_follow(user_a, user_b)
    
    # check user_a has 1 follower
    assert len(followers_a) == 1

    # check user_b has 1 followee
    assert len(following_b) == 1