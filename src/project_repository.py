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
    
    # methods for the Post Table
    def get_post_by_id(self, post_id):
        return  Post.query.filter_by(post_id=post_id).first()
    
    def get_all_posts(self):
        posts= Post.query.all()
        return posts
    
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
        
    # def delete_movie(self, movie_id: int) -> Movie:
    #         """Delete a movie and return it"""
    #         # Make sure the movie exists
    #         old_movie = self._db.get(movie_id)
    #         # Complain if we did not find the movie
    #         if not old_movie:
    #             raise ValueError(f'movie with id {movie_id} not found')
    #         # Remove the movie from the dict
    #         del self._db[movie_id]
    #         return old_movie
    
#    def update_movie(self, movie_id: int, title: str, director: str, rating: int) -> Movie:
#             """Update a movie and return it"""
#             # Get a reference to the movie in the dict
#             movie = self._db.get(movie_id)
#             # Complain if we did not find the movie
#             if not movie:
#                 raise ValueError(f'movie with id {movie_id} not found')
#             # Update the movie, which is the same object that is in the dict, so the changes stick
#             movie.title = title
#             movie.director = director
#             movie.rating = rating
#             return movie
    
    # methods for the Section Table
    def get_all_courses(self):
        courses=Section.query.all()
        return courses
    
    def get_sections_by_id(self, section_id):
        return Section.query.filter_by(section_id=section_id).first()
    
project_repository_singleton = ProjectRepository()