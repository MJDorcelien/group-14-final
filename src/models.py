# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.python.org/3/library/datetime.html

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

person_section=db.Table(
    'person_section',
    db.Column("person", db.Integer, db.ForeignKey('person.person_id'), nullable=False),
    db.Column("course",db.Integer, db.ForeignKey('section.section_id'), nullable=False)
)

user_following=db.Table(
    'user_following',
    db.Column("follower",db.Integer, db.ForeignKey('person.person_id'), nullable=False),
    db.Column("followee",db.Integer, db.ForeignKey('person.person_id'), nullable=False)
)

class Person(db.Model):
    __tablename__ = 'person'
    person_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name=db.Column(db.String(50), nullable=False)
    bio=db.Column(db.String(255), nullable=False)
    email=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(255), nullable=False)
    university=db.Column(db.String(50), nullable=False)
    course=db.relationship('Section',backref='courses',secondary=person_section,lazy=True)

    def __init__(self,user_name:str,bio:str,email:str,password:str,university:str) -> None:
        self.user_name=user_name
        self.bio=bio
        self.email=email
        self.password=password
        self.university=university

    def __repr__(self) -> str:
        return f'Person(id={self.person_id},username={self.user_name}, bio={self.bio}, email={self.email}, password={self.password}, university={self.university})'
        
class Section(db.Model):
    section_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(50), nullable=False)
    description=db.Column(db.Text, nullable=False)
    university=db.Column(db.String(50), nullable=False)
    course=db.Column(db.String(50), nullable=False)
    main=db.Column(db.Boolean, nullable=False)


    def __init__(self,title:str,description:str,university:str,course:str,main:bool) -> None:
        self.title=title
        self.description=description
        self.university=university
        self.course=course
        self.main=main

    def __repr__(self) -> str:
        return f'Section(id={self.section_id},title={self.title}, description={self.description},university={self.university}, course={self.course}, main={self.main})'

class Post(db.Model):
    __tablename__="post"
    post_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    poster=db.Column(db.Integer, db.ForeignKey('person.person_id'), nullable=False)
    course=db.Column(db.Integer, db.ForeignKey('section.section_id'), nullable=False)
    date_time=db.Column(db.DateTime, nullable=False)
    content=db.Column(db.Text, nullable=False)
    parent_post=db.Column(db.Integer, nullable=True)

    def __init__(self,poster:int,course:int,date_time:datetime,content:str) -> None:
        self.poster=poster
        self.course=course
        self.date_time=date_time
        self.content=content

    def __repr__(self) -> str:
        return f'Post(id={self.post_id},poster={self.poster}, course={self.course}, date={self.date_time}, content={self.content}, parent={self.parent_post})'
    

