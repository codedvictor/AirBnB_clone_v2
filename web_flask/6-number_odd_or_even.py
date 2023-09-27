#!/usr/bin/python3
""" File to initiate a Flask web application """
from flask import Flask
from flask import render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def index():
    """render the route"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """Serve hbnb page"""
    return "HBNB"


@app.route("/c/<text>")
def c(text):
    """Serve C page with text argument"""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route("/python/<text>")
@app.route("/python")
def python(text="is cool"):
    """Serve python route"""
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route("/number/<int:n>")
def number(n):
    """Serve number"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>")
def number_template(n):
    """Render a html template"""
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>")
def number_odd_or_even(n):
    """Rnder even or odd"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
