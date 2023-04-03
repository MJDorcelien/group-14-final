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
