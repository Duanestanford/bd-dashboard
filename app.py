from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import datetime
import os

app = Flask(__name__)

#DB Setup

user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASS')
url = os.getenv('DATABASE_URL')
db_name = os.getenv('DATABASE_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{url}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Brands(db.Model):
    __tablename__ = 'brands'
    brand = db.Column(db.String(200), primary_key = True, unique = True)
    tm = db.Column(db.String(200), unique = True)
    co = db.Column(db.String(200), unique = True)
    cat = db.Column(db.String(200), unique = True)
    subcat = db.Column(db.String(200), unique = True)

    def __init__(self, brand, tm, co, cat, subcat):
        self.brand = brand
        self.tm = tm
        self.co = co
        self.cat = cat
        self.subcat = subcat

class Sub_Count(db.Model):
    __tablename__='sub_count'
    now = db.Column(db.String(300), primary_key = True, unique = True)
    sub_count = db.Column(db.Integer)

    def __init__(self, now, sub_count):
        self.now = now
        self.sub_count = sub_count


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    your_user = str(os.getenv('U'))
    your_pass = str(os.getenv('P'))
    return username == your_user and password == your_pass

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
    import query
    subscriber_count = query.post_request()
    # if time.time() - query_time < 600:
    now = datetime.datetime.now()
    data = Sub_Count(now, subscriber_count)
    db.session.add(data)
    db.session.commit()
    return render_template("index.html", count = subscriber_count)
    # return render_template("index.html", count = "399")


if __name__ == '__main__':
    app.run()