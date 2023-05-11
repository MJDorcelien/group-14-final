from flask import Flask, abort, redirect, render_template, request
from src.models import db, Person, Section, Post
import datetime

class ProjectRepository:

    # methods for the Person Table
    def get_all_user(self):
        return Person.query.all()
    
    def create_user(self,user_name,bio,email,password,university) -> Person:
        new_user=Person(user_name,bio,email,password,university)

        db.session.add(new_user)
        db.session.commit()

        return new_user
    
    def get_user_courses(self,person_id) -> Person:
        user = self.get_user_by_id(person_id)
        user_courses=user.course
        return user_courses
    
    def get_user_by_id(self, person_id) -> Person:
        return Person.query.filter_by(person_id=person_id).first()
    
    def get_user_by_name(self, user_name) -> Person:
        person=Person.query.filter_by(user_name=user_name).first()
        return person
    
    def delete_all_person_section(self) -> None:
        users=self.get_all_user()
        for user in users:
            courses=self.get_user_courses(user.person_id)
            if courses:
                for course in courses:
                    user.course.remove(self.get_sections_by_id(course.section_id))
            db.session.add(user)
            db.session.commit()
    
    # methods for the Post Table
    def get_post_by_id(self, post_id) -> Post:
        return  Post.query.filter_by(post_id=post_id).first()
    
    def get_all_posts(self) -> Post:
        posts= Post.query.all()
        return posts
    
    def create_post(self, person_id: int, section_id: int, date: datetime, message:str):
        post=Post(person_id,section_id,date,message)
        db.session.add(post)
        db.session.commit()

        return post
    
    def update_post(self, post_id: int, message:str) -> Post:
        post=Post.query.filter_by(post_id=post_id).first()
        if not post:
            raise ValueError(f'post with id {post_id} not found')
        post.content=message
        db.session.commit()
        return post
    
    def delete_post(self, post_id: int) -> None:
        old_post=Post.query.filter_by(post_id=post_id).first()
        if not old_post:
            raise ValueError(f'post with id {post_id} not found')
        db.session.delete(old_post)
        db.session.commit()

    def delete_all_posts(self) -> None:
        posts= Post.query.all()
        for post in posts:
            old_post=Post.query.filter_by(post_id=post.post_id).first()
            if not old_post:
                raise ValueError(f'post with id {post.post_id} not found')
            db.session.delete(old_post)
            db.session.commit()
    
    # methods for the Section Table
    def get_all_courses(self):
        courses=Section.query.all()
        return courses
    
    def get_sections_by_id(self, section_id):
        return Section.query.filter_by(section_id=section_id).first()
    
    def clear_db(self) -> None:
            """Clears all movies out of the database, only to be used in tests"""
            self._db = {}

project_repository_singleton = ProjectRepository()
    
