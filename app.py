from flask import Flask, abort, redirect,session, render_template, request, url_for
from dotenv import load_dotenv
import os

from src.models import Person, Section, Post
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from datetime import date

load_dotenv()

from src.project_repository import project_repository_singleton
from src.models import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret" 
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

db.init_app(app)

app.config['SQLALCHEMY_ECHO']=True

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/courses')
def view_all_courses():
    # hardcoding a person and a section
    user=Person("Britany","Baby Maisyn's mom","b@b.com","happybaby","UNCC")
    db.session.add(user)
    db.session.commit()
    section=Section("Comp Arch","hardest coure","UNCC","ITIS 3181")
    db.session.add(section)
    db.session.commit()
    today=date.today()
    post=Post(3,1,today,"hello")
    db.session.add(post)
    db.session.commit()
    
    users=Person.query.all()
    sections=Section.query.all()
    print(users)
    print(sections)

    # leave code below in
    # need to get all the section id's for the courses the user is in and add them to chats
    chats=[]
    posts=project_repository_singleton.get_all_posts()
    for post in posts:
        chat_id=post.post_id
        chat=project_repository_singleton.get_post_by_id(chat_id)
        chats.append(chat)
    # need to pass chats to html and ensure that its received for the route
    return render_template('get_all_courses.html',chats=chats)

@app.post('/courses')
def create_chat():
    users=project_repository_singleton.get_all_user()
    sections=Section.query.all()
    posts=Post.query.all()

    if not users:
        return render_template('get_all_courses.html', error="Please either signup or lognin", users=users,sections=sections,posts=posts)

    if not sections:
        return render_template('get_all_courses.html', error="Please add a course", users=users,sections=sections,posts=posts)

    return redirect("/courses/specific")

    # name=request.form.get("name")
    # code=request.form.get("code")
    # join=request.form.get("join",False)
    # create=request.form.get("create",False)

    # if not name:
    #     return render_template('get_all_courses.html', error="Please enter a name",code=code,name=name)
    
    # if join != False and not code:
    #     return render_template('get_all_courses.html', error="Please enter a room code",code=code,name=name)
    
    # room=code

    # # checks to see if they're creating a room
    # if create != False:
    #     room=generate_unique_code(4)
    #     rooms[room]={"members": 0, "messages": []}
    # # checks to see if they are attempting to join a room that does not exist
    # elif code not in rooms:
    #     return render_template('get_all_courses.html', error="Room does not exist.",code=code,name=name)
    
    # session["room"]=room
    # session["name"]=name   

    # return redirect("/courses/specific")

from string import ascii_uppercase

chats={}
# 56 minutes

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

###################### socketio methods

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    # this is where you would store the message on the server for the individual rooms
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room=session.get("room")
    name=session.get("name")

    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1

    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room=session.get("room")
    name=session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


############routes
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
    # for each chat in chats need to grab the information for that column
    return render_template('get_courses_chat.html')
    # room=session.get("room")
    # if room is None or session.get("name") is None or room not in rooms:
    #     return redirect("/courses")
    
    # return render_template('get_courses_chat.html',code=room,messages=rooms[room]["messages"])


# code from the video

# @app.post('/create-join')
# def home_post():
#     session.clear()
#     name=request.form.get("name")
#     code=request.form.get("code")
#     join=request.form.get("join",False)
#     create=request.form.get("create",False)

#     if not name:
#         return render_template('create_join_room.html', error="Please enter a name",code=code,name=name)
    
#     if join != False and not code:
#         return render_template('create_join_room.html', error="Please enter a room code",code=code,name=name)
    
#     room=code

#     # checks to see if they're creating a room
#     if create != False:
#         room=generate_unique_code(4)
#         rooms[room]={"members": 0, "messages": []}
#     # checks to see if they are attempting to join a room that does not exist
#     elif code not in rooms:
#         return render_template('create_join_room.html', error="Room does not exist.",code=code,name=name)
    
#     session["room"]=room
#     session["name"]=name   

#     return redirect(url_for("room"))

# @app.get('/create-join')
# def home_get():
#     session.clear()
#     return render_template("create_join_room.html")

# @app.get("/room")
# def room():
#     room=session.get("room")
#     if room is None or session.get("name") is None or room not in rooms:
#         return redirect("/create-join")
    
#     return render_template("in_room.html", code=room, messages=rooms[room]["messages"])