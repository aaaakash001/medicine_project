from flask import render_template
from backend import app

#index or main page
@app.route('/')
def index():
    return render_template('index.html')
