from flask import Flask, request, jsonify, render_template, make_response
from datetime import datetime, timedelta
from functools import wraps
import sys
import os
import time
import random


app = Flask(__name__, static_url_path='')

# https://github.com/miguelgrinberg/oreilly-flask-apis-video/issues/6
def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            resp = func(*args, **kwargs)
            resp.direct_passthrough = False
            resp.set_data('{}({})'.format(
                str(callback),
                resp.get_data(as_text=True)
            ))
            resp.mimetype = 'application/javascript'
            return resp
        else:
            return func(*args, **kwargs)
    return decorated_function


@app.route('/')
def homepage():
    return app.send_static_file('index.html')


@app.route('/data', methods = ["GET"])
@jsonp
def data():
    return app.send_static_file('data.json')


@app.route('/welcome')
def welcome():
    user = request.args.get('name', default = "user")
    #print(user)
    r = make_response( render_template("welcome.html", user = user) )
    r.headers.set("X-XSS-Protection", "0")
    return r

#Obsolete path used for testing client side code eval
@app.route('/calc', methods = ["POST"])
def calc():
    print(request.get_json()['str'])
    print(request.get_json()['value'])
    #print(request.form["value"])
    return jsonify( str = '{}+{}'.format(random.randint(0,1000), random.randint(0,1000)) )

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run()
