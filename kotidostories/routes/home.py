from flask import render_template

from kotidostories import app
@app.route('/')
def landing_page():
    return render_template("layout.html")
