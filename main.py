from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib
from werkzeug.security import generate_password_hash, check_password_hash

my_mail = 'shreekantpukale0@gmail.com'
my_pass = "oetcvxgceidcvgyf"  # this is not the correct password
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dengueusers.db'

app.secret_key = 'helloshree'
# app.config['SQLALCHEMY_DATABASE_MODIFICATION'] = False
db = SQLAlchemy(app)


class Dengue(db.Model):
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=False)
    phone = db.Column(db.String, unique=True, primary_key=True)
    password = db.Column(db.String, unique=False)
    address = db.Column(db.String, unique=False)
    sector = db.Column(db.String, unique=False)


db.create_all()


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        address = request.form.get('address')
        sector = request.form.get('sector')
        user = Dengue(email=email, username=username, phone=phone, password=generate_password_hash(password), address=address, sector=sector)
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered")
        return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/office', methods=['POST', 'GET'])
def office():
    if request.method == 'POST':
        # name = request.form.get('name')
        # address = request.form.get('address')
        sector = request.form.get('sector')
        user = Dengue.query.filter_by(sector=sector)
        clients = {u.email:u.username for u in user}
        with open('precautions.txt') as p:
            content = p.read()
        if len(clients) >= 1:
            for client in clients:
                connection = smtplib.SMTP('smtp.gmail.com')
                connection.starttls()
                connection.login(user=my_mail, password=my_pass)
                connection.sendmail(from_addr=my_mail, to_addrs=client, msg=content)
                connection.close()
        else:
            pass
    return render_template('office.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Dengue.query.filter_by(username=username).first()
        if user:
            if check_password_hash(pwhash=user.password, password=password):
                return redirect(url_for('complaint'))
            else:
                pass
        else:
            pass
    return render_template('login.html')


@app.route('/complaint')
def complaint():
    return render_template('complaint.html')


@app.route('/news')
def news():
    return render_template('news.html')


if __name__ == '__main__':
    app.run(debug=True)
