from flask import Flask, abort, redirect,session, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.models import db, Person
import bcrypt
import os

from src.models import Person, Section, Post, person_section,user_following
from flask_socketio import join_room, leave_room, send, SocketIO
import random
import datetime 

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
    # software1=Section("Software Engineering","most useful courses","UNCC","ITSC 3155", True)
    # software2=Section("Software Engineering","most useful courses","UNCC","ITSC 3155", False)
    # mobile1=Section("Mobile Application Development","stupid andriod studio","UNCC","ITIS 5180",True)
    # mobile2=Section("Mobile Application Development","stupid andriod studio","UNCC","ITIS 5180",False)
    # db.session.add_all([software1,software2,mobile1,mobile2])
    # db.session.commit()

    # user=project_repository_singleton.get_user_by_id(7)
    # user.course.append(software1)
    # user.course.append(software2)
    # user.course.append(mobile1)
    # db.session.add(user)
    # db.session.commit()

    # date=datetime.datetime.now()
    # post1=Post(7,5,date,"hello this is for the main chat")
    # post2=Post(4,5,date,"this is in reponse to Britany")
    # post3=Post(4,6,date,"whomst is this")
    # post4=Post(4,7,date,"main chat for mobile peeps")
    # post5=Post(7,7,date,"main chat??")
    # db.session.add_all([post1,post2,post3,post4,post5])
    # db.session.commit()

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

@app.post('/login')
def login():
    #session['user'] = {
      #      'username' : username
      #  }
      pass

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
        return 'Login successful'
    else:
        return 'Invalid username or password'
    # Redirect to the page you want the user to go to after they login
    # 
    return redirect('/') 

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
