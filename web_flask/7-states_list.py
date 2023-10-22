#!/usr/bin/python3
"""Start flask web application must be listening
on 0.0.0.0, port 5000
"""

from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def display_state():
    """return an HTML Page that displays all states"""
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(excep):
    """Call Storage.close method"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
