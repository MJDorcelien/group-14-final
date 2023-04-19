from flask import Flask, abort, redirect, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()

from src.project_repository import project_repository_singleton
from src.models import db

app = Flask(__name__)

db_user=os.getenv('DB_USER')
db_pass=os.getenv('DB_PASS')
db_host=os.getenv('DB_HOST')
db_port=os.getenv('DB_PORT')
db_name=os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI']\
    =f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

db.init_app(app)

app.config['SQLALCHEMY_ECHO']=True

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/courses')
def view_all_courses():
    return render_template('get_all_courses.html')

@app.get('/join')
def search_all_universities():
    return render_template('join_university.html')

@app.get('/friends')
def view_all_friends():
    return render_template('get_all_friends.html')

@app.get('/profile')
def view_user_profile():
    return render_template('get_user_profile.html')

@app.get('/login')
def login_user():
    return render_template('login_user.html')

@app.get('/friends/profile')
def view_friend_profile():
    return render_template('get_friends_profile.html')

@app.get('/profile/settings')
def view_user_settings():
    return render_template('get_user_settings.html')

# specific will later be changed to the courseId
@app.get('/courses/specific')
def view_specific_course():
    return render_template('get_courses_chat.html')