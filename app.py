from flask import Flask, redirect, render_template

app = Flask(__name__)


# Maggie was at the meeting on Wednesday Night
# Kya was also at the meeting!
# .get should be .route so they work on Macs also
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def view_all_courses():
    return render_template('get_all_courses.html')

@app.route('/join')
def search_all_universities():
    return render_template('join_university.html')

@app.route('/friends')
def view_all_friends():
    return render_template('get_all_friends.html')

@app.route('/profile')
def view_user_profile():
    return render_template('get_user_profile.html')

@app.route('/login')
def login_user():
    return render_template('login_user.html')

@app.route('/friends/profile')
def view_friend_profile():
    return render_template('get_friends_profile.html')

@app.route('/profile/settings')
def view_user_settings():
    return render_template('get_user_settings.html')

# specific will later be changed to the courseId
@app.route('/courses/specific')
def view_specific_course():
    return render_template('get_courses_chat.html')