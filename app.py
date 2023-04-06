from flask import Flask, redirect, render_template

app = Flask(__name__)


# Maggie was at the meeting on Wednesday Night
# Kya was also at the meeting!
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