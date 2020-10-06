from flask import Flask, render_template, request, Response
import query
from functools import wraps
import time
import os

app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == os.getenv('U') and password == os.getenv('P')

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/")
@requires_auth
def dashboard():
    subscriber_count = query.post_request()
    # if time.time() - query_time < 600:
    return render_template("index.html", count = subscriber_count)

@app.route("/subs")
def subs():
    subscriber_count = query.post_request()
    return str(subscriber_count)


if __name__ == '__main__':
    app.run()