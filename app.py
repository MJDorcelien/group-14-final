from flask import Flask, redirect, render_template

app = Flask(__name__)


# Maggie was at the meeting on Wednesday Night
# Kya was also at the meeting!
@app.get('/')
def index():
    return render_template('index.html')
