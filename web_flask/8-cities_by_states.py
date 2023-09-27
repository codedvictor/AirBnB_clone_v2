#!/usr/bin/python3
""" File to initiate a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_session(exception):
    """Teardown session"""
    storage.close()


@app.route("/cities_by_states")
def cities_by_states():
    """render cities_by_states list"""
    return render_template('8-cities_by_states.html', Table="States",
                           states=storage.all(State))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
