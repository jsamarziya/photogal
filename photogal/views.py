from flask import render_template

from photogal.app import app


@app.route('/')
def index():
    return "Index Page"


@app.route('/hello/', methods=['GET'])
@app.route('/hello/<name>', methods=['GET'])
def hello(name=None):
    return render_template("hello.html", name=name)


@app.route('/hello/', methods=['POST'])
def post_hello():
    return 'You rang?'
