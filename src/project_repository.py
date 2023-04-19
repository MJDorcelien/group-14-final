from flask import Flask, abort, redirect, render_template, request
from src.models import db, Person, Section, Post

class ProjectRepository:
    def get_all_user(self):
        return Person.query.all()
    
    def create_user(self,user_name,bio,email,password,university):
        new_user=Person(user_name,bio,email,password,university)

        db.session.add(new_user)
        db.session.commit()

        return new_user
    
project_repository_singleton = ProjectRepository()