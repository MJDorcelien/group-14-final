from app import app
import pytest

from src.models import Person, Section, Post, person_section,user_following, db
from src.project_repository import project_repository_singleton

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        project_repository_singleton.delete_all_person_section()
        project_repository_singleton.delete_all_posts()
        Section.query.delete()
        Post.query.delete()
        Person.query.delete()
        db.session.commit()
        yield app.test_client()