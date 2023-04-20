# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.python.org/3/library/datetime.html

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

person_section=db.Table(
    'person_seciton',
    db.Column("person", db.Integer, db.ForeignKey('person.person_id'), nullable=False),
    db.Column("course",db.Integer, db.ForeignKey('section.section_id'), nullable=False)
)

user_following=db.Table(
    'user_following',
    db.Column("follower",db.Integer, db.ForeignKey('person.person_id'), nullable=False),
    db.Column("followee",db.Integer, db.ForeignKey('person.person_id'), nullable=False)
)

class Person(db.Model):
    person_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name=db.Column(db.String(50), nullable=False)
    bio=db.Column(db.String(255), nullable=False)
    email=db.Column(db.String(255), nullable=False)
    password=db.Column(db.String(50), nullable=False)
    university=db.Column(db.String(50), nullable=False)
    course=db.relationship('Section',backref='courses',secondary=person_section,lazy=True)

    def __init__(self,user_name:str,bio:str,email:str,password:str,university:str) -> None:
        self.user_name=user_name
        self.bio=bio
        self.email=email
        self.password=password
        self.university=university
        
class Section(db.Model):
    section_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(50), nullable=False)
    description=db.Column(db.Text, nullable=False)
    university=db.Column(db.String(50), nullable=False)
    course=db.Column(db.String(50), nullable=False)

    def __init__(self,title:str,description:str,university:str,course:str) -> None:
        self.title=title
        self.description=description
        self.university=university
        self.course=course

class Post(db.Model):
    post_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    poster=db.Column(db.Integer, db.ForeignKey('person.person_id'), nullable=False)
    course=db.Column(db.Integer, db.ForeignKey('section.section_id'), nullable=False)
    date_time=db.Column(db.DateTime, nullable=False)
    content=db.Column(db.Text, nullable=False)
    parent_post=db.Column(db.Integer, nullable=True)

    def __init__(self,poster:int,course:int,date_time:datetime,content:str,parent_post:int) -> None:
        self.poster=poster
        self.course=course
        self.date_time=date_time
        self.content=content
        self.parent_post=parent_post