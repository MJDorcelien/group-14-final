from flask import Flask, abort, redirect, session, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.models import db, Person,Post
import bcrypt
import os
from flask_socketio import SocketIO, leave_room,join_room,emit
import datetime
from src.project_repository import project_repository_singleton

load_dotenv()

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

@app.get('/join')
def view_join_courses():
    if 'user' not in session:
        return "You must be logged in to join a course. Login or Signup to join."
    return render_template('join_courses.html')

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
    if 'user' not in session:
        abort(401)
    return render_template('get_user_settings.html')

rooms ={}
@app.post('/login')
def login():
    # If user already logged in, redirect them to the "all courses" homepage view
    if 'user' in session:
        redirect('/courses')

    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    # Retrieve the user with the given username from the database
    user = Person.query.filter_by(username=username).first()

    if user is None:
        return 'Invalid username or password'

    # Use bcrypt to check if the provided password matches the stored hashed password
    if bcrypt.checkpw(password, user.password.encode('utf-8')):

        # Create user session that stores username
        session['user'] = {
            'username' : username
            }

        # Redirects user to "all courses" page after login 
        return redirect('/courses') 
    else:
        return 'Invalid username or password'
    
    return render_template('index.html')

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
    
@app.post('/logout')
def logout():
    del session['user']
    return redirect('/')
    
@app.get('/courses')
def view_all_courses():
    sections=project_repository_singleton.get_user_courses(7) # need to change to the id of the auth
    return render_template('get_all_courses.html', courses=sections)

@app.get('/courses/<int:section_id>')
def view_specific_course(section_id):
    person_id=7 # this needs to get the person_id from the user
    courses=project_repository_singleton.get_user_courses(person_id)
    posts=project_repository_singleton.get_all_posts()
    course=project_repository_singleton.get_sections_by_id(section_id)
    users=project_repository_singleton.get_all_user()
    user=project_repository_singleton.get_user_by_id(person_id)
    person=user.user_name
    rooms["user"]=user
    rooms["course"]=course
    return render_template('get_courses_chat.html',courses=courses,section=section_id,posts=posts,exam=course,users=users,person_id=person_id,person=person)

@app.post('/courses/<int:post_id>/messages/edit')
def edit_specific_message(post_id):
    post=project_repository_singleton.get_post_by_id(post_id)
    new_message=request.form.get('message')
    project_repository_singleton.update_post(post_id,new_message)

    return redirect(f'/courses/{post.course}')

@app.post('/courses/<int:post_id>/messages/delete')
def delete_specific_message(post_id):
    post=project_repository_singleton.get_post_by_id(post_id)
    section=post.course
    project_repository_singleton.delete_post(post_id)
    
    return redirect(f'/courses/{section}')

@socketio.on("connect")
def connect(auth):
    user=rooms["user"]
    course=rooms["course"]
    join_room(course.section_id)
    emit({"name": user.user_name,"message": "has entered the room"}, broadcast=True)
    print(f"{user.user_name} has joined {course.title} {course.section_id}")

@socketio.on("disconnect")
def disconnect():
    user=rooms["user"]
    course=rooms["course"]
    leave_room(course.section_id)

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    user=rooms["user"]
    course=rooms["course"]
    date=datetime.datetime.now()

    post=Post(user.person_id,course.section_id,date,message)
    db.session.add(post)
    db.session.commit()

    emit("chat",{"message": message,"username": user.user_name},broadcast=True)
