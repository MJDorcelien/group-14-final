from flask import Flask, abort, redirect, session, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src.models import db, Person, Section, person_section,Post,Section
from security import bcrypt
import os
from flask_socketio import SocketIO, leave_room,join_room,emit
import datetime
from src.project_repository import project_repository_singleton

load_dotenv()

from src.project_repository import project_repository_singleton
from src.models import db, Section

app = Flask(__name__)
socketio=SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')

app.secret_key = os.getenv('APP_SECRET')

db.init_app(app)
bcrypt.init_app(app)

app.config['SQLALCHEMY_ECHO']=True

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/join')
def view_join_courses():
    if 'user' not in session:
        return redirect('/login')

    id = session['user']['person_id']
    courses = project_repository_singleton.get_user_courses(id)  

    return render_template('join_courses.html', courses=courses)

@app.post('/join')
def add_courses():
    # Get info from form
    class2 = request.form.get('join-class')
    
    
    # Test to see if the class they created is already a class
    is_class = Section.query.filter_by(course=class2).first()
    
    # If it already exists, add the user to the class
    if is_class:
        id = session['user']['person_id']
        user = project_repository_singleton.get_user_by_id(id)
        section = Section.query.filter_by(course=class2).first()
        user.course.append(section)
        db.session.add(user)
        db.session.commit()
        flash('Join class successful', 'success')
        return redirect("/join")

    #If it doesnt already exist, create the class using some default values (which can be edited later), and add the user to it
    if not is_class:
        #class_to_join = request.form.get('join-class')
        made_class = Section (class2, "Default Description", "UNCC", class2 , True)
        db.session.add(made_class)
        db.session.commit()

        id = session['user']['person_id']
        user = project_repository_singleton.get_user_by_id(id)
        section = project_repository_singleton.get_sections_by_id(made_class.section_id)
        user.course.append(section)
        db.session.add(user)
        db.session.commit()
        flash('Create and join class successful', 'success')
        return redirect("/join")
    
    # If user cannot join class, produce error message!
    else:
        flash('Something went wrong. Please double check your course code and try again', 'danger')
        return redirect("/join")

@app.get('/friends')
def view_all_friends():
    if 'user' not in session:
        return "You must be logged in to view this page. Login or Signup to view"
    person=session['user']
    person_id=person['person_id']
    following=project_repository_singleton.get_user_following(person_id)
    followers=project_repository_singleton.get_user_followers(person_id)
    return render_template('get_all_friends.html', following=following, followers=followers)

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

rooms ={}
@app.post('/login')
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
    return redirect('/courses')

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

        session['user'] = {
        'username' : username,
        'person_id' : user.person_id
        }
        return redirect('/courses')
    except:
        return redirect('/signup')
    
# logs out the user
@app.post('/logout')
def logout():
    del session['user']
    return redirect('/')

@app.get('/courses')
def view_all_courses():
    person=session['user']
    person_id=person['person_id']
    sections=project_repository_singleton.get_user_courses(person_id)
    print(sections)
    return render_template('get_all_courses.html', courses=sections)

@app.get('/courses/<int:section_id>')
def view_specific_course(section_id):
    person=session['user']
    person_id=person['person_id']
    courses=project_repository_singleton.get_user_courses(person_id)
    
    posts=project_repository_singleton.get_all_posts()
    course=project_repository_singleton.get_sections_by_id(section_id)
    users=project_repository_singleton.get_all_user()
    user=project_repository_singleton.get_user_by_id(person_id)

    list_posts=project_repository_singleton.get_all_posts()
    for i in range(len(list_posts)):
        for j in range(i+1,len(list_posts)):
            if list_posts[i].post_id > list_posts[j].post_id:
                list_posts[i], list_posts[j] = list_posts[j], list_posts[i]

    person=user.user_name
    rooms["user"]=user
    rooms["course"]=course
    return render_template('get_courses_chat.html',list_posts=list_posts,courses=courses,section=section_id,posts=posts,exam=course,users=users,person_id=person_id,person=person)

@app.get('/courses/<int:post_id>/messages/edit')
def get_edit_specific_post(post_id):
    post=project_repository_singleton.get_post_by_id(post_id)
    content=post.content
    return render_template('edit_posts_form.html', post=post, content=content)

# this is for editing a post
@app.post('/courses')
def update_post():
    post_id=request.form.get('post-id')
    print(post_id)
    new_message=request.form.get('new-message')
    project_repository_singleton.update_post(post_id,new_message)
    post=project_repository_singleton.get_post_by_id(post_id)
    print(post)
    section=post.course

    return redirect(f'/courses/{section}')

@app.post('/courses/<int:post_id>/messages/delete')
def delete_specific_message(post_id):
    post=project_repository_singleton.get_post_by_id(post_id)
    print(post)
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

# takes in new message and adds to database
@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    user=rooms["user"]
    course=rooms["course"]
    date=datetime.datetime.now()

    project_repository_singleton.create_post(user.person_id,course.section_id,date,message)

    emit("chat",{"message": message,"username": user.user_name},broadcast=True)
