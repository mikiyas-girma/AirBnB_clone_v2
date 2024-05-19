#!/usr/bin/python3
"""starts flask application with two routes"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """display hello hbnb"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """display hbnb"""
    return "HBNB"


@app.route('/c/<text>')
def c_route(text):
    """return c followed by value of text variable"""
    return "C {}".format(escape(text.replace('_', ' ')))


@app.route('/python/<text>')
@app.route('/python', defaults={'text': 'is cool'})
def python_route(text):
    """return c followed by value of text variable"""
    return "Python {}".format(escape(text.replace('_', ' ')))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
