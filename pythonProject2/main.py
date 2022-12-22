from flask import Flask, render_template, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "booking appoiment"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3307/appoiment'
db = SQLAlchemy(app)


class contacts_us(db.Model):
    ''' sno, name phone_num, msg, date, email '''

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/contacts_us", methods=['GET', 'POST'])
def contacts():
    if request.method == 'GET':
        return render_template('fetch.html')

    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        dataread = contacts_us(name=name, phone_num=phone, email=email, date=datetime.now())
        db.session.add(dataread)
        db.session.commit()
        flash("Appoiment Submitted Successfully")

    return render_template('index.html')


@app.route("/book_appoiment")
def book_appoiment():
    return render_template('Contact-us.html')


# fetch data or retrive data

@app.route("/admin")
def admin():
    dataread = contacts_us.query.all()

    return render_template("fetch.html", dataread=dataread)


## updating data

@app.route('/edit', methods=['GET', 'POST'])
def edit():

    if request.method == 'POST':

        box_name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        data = contacts_us(name=box_name, phone_num=phone, email=email, date=datetime.now())
        db.session.add(data)
        db.session.commit()


    return render_template('edit.html')

## delete data


@app.route('/delete <int:sno>')
def erase(sno):
    # Deletes the data on the basis of unique id and
    # redirects to home page
    data = contacts_us.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return render_template('edit.html')

app.run(debug=True)
