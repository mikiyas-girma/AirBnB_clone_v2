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
def close_session(exec):
    """
    close session
    """
    storage.close()


@app.route('/states')
@app.route('/states/<id>')
def states(id=None):
    """
    display a HTML page: (inside the tag BODY)
    """
    states = None
    state = None
    states_list = list(storage.all(State).values())
    case = 404

    if id is not None:
        match = list(filter(lambda x: x.id == id, states_list))
        if match:
            state = match[0]
            state.cities.sort(key=lambda x: x.name)
            case = 'cities'
    else:
        states = states_list
        for state in states:
            state.cities.sort(key=lambda x: x.name)
        states.sort(key=lambda x: x.name)
        case = 'states'
    vars = {'states': states, 'state': state, 'case': case}
    return render_template('9-states.html', **vars)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
