#!/usr/bin/python3
"""
script that starts flask web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_session(exec):
    """
    close session
    """
    storage.close()


@app.route('/hbnb_filters')
def hbnb_filters():
    """
    display a HTML page: (inside the tag BODY)
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
