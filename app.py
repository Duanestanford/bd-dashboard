from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import datetime
import os

app = Flask(__name__)

#DB Setup

heroku_db = os.getenv('DATABASE_URL')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
url = os.getenv('DB_URL')
db_name = os.getenv('DB_NAME')


# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{url}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db
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

class Delegate_Count(db.Model):
    __tablename__='delegate_count'
    now = db.Column(db.String(300), primary_key = True, unique = True)
    delegate_count = db.Column(db.Integer)

    def __init__(self, now, delegate_count):
        self.now = now
        self.delegate_count = delegate_count


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
    subscriber_count = query.request_sub_count()
    delegate_count = query.request_delegate_count()
    now = datetime.datetime.now()

    subscriber_data = Sub_Count(now, subscriber_count)
    db.session.add(subscriber_data)
    db.session.commit()
    db.session.close()

    
    delegates_data = Delegate_Count(now, delegate_count)
    db.session.add(delegates_data)
    db.session.commit()
    db.session.close()

    subscription_revenue_string = str(subscriber_count*995)
    conference_revenue_string = str(delegate_count*425)

    subscription_revenue= "${:,}".format(subscriber_count*995)
    conference_revenue= "${:,}".format(delegate_count*425)

    return render_template("index.html", subscriber_count = subscriber_count, delegate_count = delegate_count, subscription_revenue = subscription_revenue, conference_revenue = conference_revenue)


if __name__ == '__main__':
    app.run()