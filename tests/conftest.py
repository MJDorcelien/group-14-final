import pytest
from app import app
from src.models import Person, Section, Post, person_section,user_following, db

@pytest.fixture(scope = 'module')
def test_app():
    with app.app_context():
        Person.query.delete()
        Section.query.delete()
        Post.query.delete()
        db.session.commit()
        yield app.test_client()
