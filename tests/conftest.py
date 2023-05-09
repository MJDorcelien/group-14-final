from app import app
import pytest

from src.models import Person, Section, Post, person_section,user_following, db

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        Person.query.delete()
        Section.query.delete()
        Post.query.delete()
        db.session.commit()
        yield app.test_client()