from flask import Flask, render_template, request, Response, flash, url_for, redirect
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
app.config['SECRET_KEY'] = '\x13\xacqR\xc8\xc6\xb4lz\xd9\xb4\xd7\xb9\x9b\x17$U\x04Y\x90\xbf4.N'


db = SQLAlchemy(app)

# class Brands(db.Model):
#     __tablename__ = 'brands'
#     brand = db.Column(db.String(200), primary_key = True, unique = True)
#     tm = db.Column(db.String(200), unique = True)
#     co = db.Column(db.String(200), unique = True)
#     cat = db.Column(db.String(200), unique = True)
#     subcat = db.Column(db.String(200), unique = True)

#     def __init__(self, brand, tm, co, cat, subcat):
#         self.brand = brand
#         self.tm = tm
#         self.co = co
#         self.cat = cat
#         self.subcat = subcat

class Subs(db.Model):
    __tablename__='subs'

    id = db.Column(db.Integer, primary_key=True)
    now = db.Column(db.String(300), unique = True)
    sub_count = db.Column(db.Integer)

    def __init__(self, now, sub_count):
        self.now = now
        self.sub_count = sub_count

class Free_Subs(db.Model):
    __tablename__="free_subs"
    id = db.Column(db.Integer, primary_key=True)
    now = db.Column(db.String(300), unique = True)
    free_subs = db.Column(db.Integer)

    def __init__(self, now, free_subs):
        self.now = now
        self.free_subs = free_subs


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
    now = datetime.datetime.now()

    free_subs = Free_Subs.query.order_by(Free_Subs.id.desc()).first().free_subs

    paid_subs = subscriber_count - free_subs

    
    # subs_record = Subs(now, paid_subs)
    # db.session.add(subs_record)
    # db.session.commit()
    # db.session.close()

    subscription_revenue= "${:,}".format(paid_subs*995)

    return render_template("index.html", paid_subs = paid_subs, free_subs = free_subs)


@app.route('/plus', methods=["POST"])
def plus():
    now = datetime.datetime.now()
    free_subs = Free_Subs.query.order_by(Free_Subs.id.desc()).first().free_subs
    higher_free_subs = free_subs+1
    new_subs = Free_Subs(now, higher_free_subs)
    db.session.add(new_subs)
    db.session.commit()
    return redirect(url_for('dashboard'))



@app.route('/minus', methods=["POST"])
def minus():
    now = datetime.datetime.now()
    free_subs = Free_Subs.query.order_by(Free_Subs.id.desc()).first().free_subs
    lower_free_subs = free_subs-1
    new_subs = Free_Subs(now, lower_free_subs)
    db.session.add(new_subs)
    db.session.commit()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port = 3000)