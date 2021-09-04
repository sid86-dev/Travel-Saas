from os import read
from flask import Flask, render_template, request, url_for, redirect, flash,session
from flask_sqlalchemy import SQLAlchemy
import json
import random
from urllib.request import urlopen
import hashlib


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'TPmi4aLWRbyVq8zu9v82dWYW1'

db = SQLAlchemy(app)

def hash(text):
    has = hashlib.sha256(text.encode()).hexdigest()
    return has

class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    mail = db.Column(db.String(70))  
    pw = db.Column(db.String(256))
       
    def __repr___(self):
        return '<Task %r>' % self.id


@app.route('/signup', methods=['POST','GET'])
def signup():
    if 'email' in request.form and 'first name' in request.form and 'last name' in request.form and 'password' in request.form and 'cpassword' in request.form and 'checkbox' in request.form:
        email = request.form['email']
        first_name = request.form['first name']
        last_name= request.form['last name']
        new_password = request.form['password']
        confirm_password = request.form['cpassword']
        checkbox=request.form['checkbox']

        if email == "" or first_name == "" or last_name=="" or new_password == "" or confirm_password == "" :
            flash("No fields should be left empty")
            return redirect(url_for('signup'))
        if new_password != confirm_password:
            flash("Passwords did not match!!!")
            return redirect(url_for('signup'))
        if checkbox!="read":
            flash("Terms and conditions are mandatory")
            return redirect(url_for('signup'))

        password=str(hash(new_password))
        new_user=user(firstname=first_name,lastname=last_name,mail=email,pw=password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            flash("Something went wrong!!!")
            return redirect("/signup")
    else:
        return render_template("pages-sign-up.html")

@app.route('/login', methods=["POST",'GET'])
def login():
    
    if 'username' in request.form and 'password' in request.form:
        us = request.form['username']
        password = request.form['password']
        if us == "" or password == "":
            flash("Fields shouldnt be left empty")
            return redirect('/login')
        try:
            
            passw=str(hash(password))
            row=user.query.filter_by(mail=us,pw=passw).count()
            u=user.query.filter_by(mail=us,pw=passw).first()
            if row==1:
                sid=user.query.filter_by(mail=us,pw=passw).first().id
                session['user']=u.firstname+' '+u.lastname
                session['id']=sid
                session['mail']=u.mail
                return render_template("homepage2.html")
            else:
                flash("Invalid login credentials")
                return redirect('/login')
        except:
            flash("Something went wrong!!!")
            return redirect('/login')
    else:
        return render_template("pages-login.html")


@app.route('/package_details')
def package_details():
    return render_template("package_details.html")


if __name__ == "__main__":
    app.run(debug=True)


