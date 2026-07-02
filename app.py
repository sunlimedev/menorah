from flask import Flask
from flask import request
from flask import render_template
from flask import g
import sqlite3


# application object ###############################################################################


app = Flask(__name__)


# site routes ######################################################################################


@app.route(rule='/', methods=['GET'])
@app.route(rule='/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/presence-detection', methods=['GET', 'POST'])
def devices():
    return render_template('presence-detection.html')


@app.route('/presence-detection/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        db = get_db()

        name = request.form['name']
        mac = request.form['mac']

        db.execute('INSERT INTO devices (name, mac) VALUES (?, ?)', (name, mac))
        db.commit()

        close_db()

    return render_template('add-device.html')


@app.route('/presence-detection/edit', methods=['GET', 'POST'])
def edit_device():
    if request.method == 'POST':
        return 'placeholder'

    return render_template('edit-device.html')


# non-route functions ##############################################################################


def get_db():
    # check for existing connection
    if 'db' not in g:
        # connect to db
        g.db = sqlite3.connect('menorah.db')
        # return dictionary style row
        g.db.row_factory = sqlite3.Row

    # return database
    return g.db


def close_db():
    # remove db from global
    db = g.pop('db', None)

    # close the existing connection
    if db is not None:
        db.close()


# execution guard ##################################################################################


if __name__ == '__main__':
    app.run(debug=True)