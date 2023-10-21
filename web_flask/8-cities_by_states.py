#!/usr/bin/python3
"""web app  must listening on 0.0.0.0"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def tear_down(self):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Cities by States"""
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
