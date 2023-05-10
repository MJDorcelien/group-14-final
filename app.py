from flask import Flask, abort, redirect, session, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.models import db, Person
from security import bcrypt
import os
from flask_socketio import SocketIO

load_dotenv()

from src.project_repository import project_repository_singleton
from src.models import db

app = Flask(__name__)
socketio=SocketIO(app)

db_user=os.getenv('DB_USER')
db_pass=os.getenv('DB_PASS')
db_host=os.getenv('DB_HOST')
db_port=os.getenv('DB_PORT')
db_name=os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI']\
    =f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

app.secret_key = os.getenv('APP_SECRET')

db.init_app(app)
bcrypt.init_app(app)

app.config['SQLALCHEMY_ECHO']=True

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/courses')
def view_all_courses():
    person=session['user']
    person_id=person['person_id']
    sections=project_repository_singleton.get_user_courses(person_id)
    return render_template('get_all_courses.html', courses=sections)

@app.get('/join')
def view_join_courses():
    if 'user' not in session:
        return "You must be logged in to join a course. Login or Signup to join."
    return render_template('join_university.html')

@app.post('/join')
def add_courses():
    # Will be implemented 
    pass

@app.get('/friends')
def view_all_friends():
    if 'user' not in session:
        return "You must be logged in to view this page. Login or Signup to view"
    return render_template('get_all_friends.html')

@app.get('/profile')
def view_user_profile():
    if 'user' not in session:
        return "You must be logged in to view this page. Login or Signup to view"
    return render_template('get_user_profile.html')

@app.get('/login')
def login_user():
    return render_template('login_user.html')

@app.get('/signup')
def signup_user():
    return render_template('sign_up_user.html')

@app.get('/friends/profile')
def view_friend_profile():
    return render_template('get_friends_profile.html')

@app.get('/profile/settings')
def view_user_settings():
    if 'user' not in session:
        abort(401)
    return render_template('get_user_settings.html')

@app.route('/login', methods=['POST'])
def login():
    # If user already logged in, redirect them to the "all courses" homepage view
    if 'user' in session:
        redirect('/courses')

    username = request.form.get('username')
    password = request.form.get('password')
    # Retrieve the user with the given username from the database
    user = Person.query.filter_by(user_name=username).first()

    if not user:
        #return redirect('/login')
        return redirect('/login')

    # Use bcrypt to check if the provided password matches the stored hashed password
    if not bcrypt.check_password_hash(user.password,password):

        # return redirect('/login')
        return redirect('/login') 
    
    # Create user session that stores username
    user=project_repository_singleton.get_user_by_name(username)
    person_id=user.person_id
    session['user'] = {
        'username' : username,
        'person_id' : person_id
        }
    
    # Redirects user to "all courses" page after login 
    return redirect('/')

@app.post('/signup')
def signup():
    username = request.form.get('username')
    password = request.form.get('password').encode('utf-8')
    biography = request.form.get('bio')
    email_address = request.form.get('email')
    your_university = request.form.get('university')

    if not username or not password or not biography or not email_address or not your_university:
        abort(400)

    # Hash the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode()

    # Create a new user with the hashed password
    user = project_repository_singleton.create_user(user_name = username, bio = biography, email = email_address, password = hashed_password, university = your_university)

    # Try to add the new user to the database
    try:
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    except:
        db.session.rollback()
        return redirect('/signup')
    
# logs out the user
@app.post('/logout')
def logout():
    del session['user']
    return redirect('/')
    

@app.get('/courses/<int:section_id>')
def view_specific_course(section_id):
    person=session['user']
    person_id=person['person_id']
    courses=project_repository_singleton.get_user_courses(person_id)
    posts=project_repository_singleton.get_all_posts()
    course=project_repository_singleton.get_sections_by_id(section_id)
    users=project_repository_singleton.get_all_user()
    return render_template('get_courses_chat.html',courses=courses,section=section_id,posts=posts,exam=course,users=users)


