from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')