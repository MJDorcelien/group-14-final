from flask import Flask, abort, redirect, render_template, request
from src.models import db, Person, Section, Post

class ProjectRepository:

    # methods for the Person Table
    def get_all_user(self):
        return Person.query.all()
    
    def create_user(self,user_name,bio,email,password,university):
        new_user=Person(user_name,bio,email,password,university)

        db.session.add(new_user)
        db.session.commit()

        return new_user
    
    def get_user_courses(self,person_id):
        user = self.get_user_by_id(person_id)
        user_courses=user.course
        return user_courses
    
    def get_user_by_id(self, person_id):
        return Person.query.filter_by(person_id=person_id).first()
    
    def get_user_by_name(self, username):
        person=Person.query.filter_by(user_name=username).first()
        users=Person.query.all()
        for user in users:
            if user.user_name==person.user_name and user.password==person.password:
                person=user
        return user
    
    # methods for the Post Table
    def get_post_by_id(self, post_id):
        return  Post.query.filter_by(post_id=post_id).first()
    
    def get_all_posts(self):
        posts= Post.query.all()
        return posts
    
    # methods for the Section Table
    def get_all_courses(self):
        courses=Section.query.all()
        return courses
    
    def get_sections_by_id(self, section_id):
        return Section.query.filter_by(section_id=section_id).first()

project_repository_singleton = ProjectRepository()
    
