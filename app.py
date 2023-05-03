from flask import Flask, abort, redirect,session, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.models import db, Person
import bcrypt
import os
from flask_socketio import SocketIO

load_dotenv()

from src.project_repository import project_repository_singleton
from src.models import db

app = Flask(__name__)
socketio=SocketIO(app)

if __name__ == "__main__":
    socketio.run(app, debug=True)

db_user=os.getenv('DB_USER')
db_pass=os.getenv('DB_PASS')
db_host=os.getenv('DB_HOST')
db_port=os.getenv('DB_PORT')
db_name=os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI']\
    =f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

app.secret_key = os.getenv('APP_SECRET')

db.init_app(app)

app.config['SQLALCHEMY_ECHO']=True

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/courses')
def view_all_courses():
    sections=project_repository_singleton.get_user_courses(7) # need to change to the id of the auth
    return render_template('get_all_courses.html', courses=sections)

@app.get('/join')
def search_all_universities():
    return render_template('join_university.html')

@app.post('/join')
def add_uni():
    # Will be implemented 
    pass

@app.get('/friends')
def view_all_friends():
    if 'user' not in session:
        abort(401)
    return render_template('get_all_friends.html')

@app.get('/profile')
def view_user_profile():
    if 'user' not in session:
        abort(401)
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
    return render_template('get_user_settings.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    # Retrieve the user with the given username from the database
    user = Person.query.filter_by(username=username).first()

    if user is None:
        return 'Invalid username or password'

    # Use bcrypt to check if the provided password matches the stored hashed password
    if bcrypt.checkpw(password, user.password.encode('utf-8')):
        # Redirect to the page you want the user to go to after they login.
        # I don't know what page to send them to lol. You guys have my permission to change
        # this if you want. Right now it is to the index page.
       
        return redirect('/courses') 
    else:
        return 'Invalid username or password'

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Create a new user with the hashed password
    user = Person(username=username, password=hashed_password)

    # Try to add the new user to the database
    try:
        db.session.add(user)
        db.session.commit()
        return 'User created successfully'
    except:
        db.session.rollback()
        return 'User already exists'
    

@app.get('/courses/<int:section_id>')
def view_specific_course(section_id):
    person_id=7 # this needs to get the person_id from the user
    courses=project_repository_singleton.get_user_courses(person_id)
    posts=project_repository_singleton.get_all_posts()
    course=project_repository_singleton.get_sections_by_id(section_id)
    users=project_repository_singleton.get_all_user()
    return render_template('get_courses_chat.html',courses=courses,section=section_id,posts=posts,exam=course,users=users)
