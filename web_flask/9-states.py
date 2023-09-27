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


@app.route("/states")
@app.route("/states/<id>")
def cities_list(id=None):
    """render the cities list for a given state"""
    state = None
    states = storage.all(State)

    if not id:
        return render_template('7-states_list.html', Table="States",
                               states=states)

    if "State.{}".format(id) in states:
        state = states["State.{}".format(id)]
    return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
