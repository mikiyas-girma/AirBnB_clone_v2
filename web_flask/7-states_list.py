#!/usr/bin/python3
"""
script that starts flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_session(self):
    """
    close session
    """
    storage.close()


@app.route('/states_list')
def state_list():
    """ display a HTML page: (inside the tag BODY)"""
    states = list(storage.all(State).values())
    states.sort(key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
