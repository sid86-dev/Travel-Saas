from os import read
from flask import Flask, render_template, request, url_for, redirect, flash,session
from flask_sqlalchemy import SQLAlchemy
import json
import random
from urllib.request import urlopen
import hashlib
import MySQLdb
from datetime import datetime
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
#Con = MySQLdb.Connect(host="184.168.96.123", port=3306, user="sid86", passwd="siddharth18", db="untouched_destination")
app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql://sid86:siddharth18@184.168.96.123/untouched_destination"
#app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel1.db'
#app.config ['SQLALCHEMY_DATABASE_URI'] = Con
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'TPmi4aLWRbyVq8zu9v82dWYW1'

db = SQLAlchemy(app)

class booking_details(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(150))
    last_name=db.Column(db.String(150))
    people_count=db.Column(db.Integer)
    email=db.Column(db.String(80))
    phone=db.Column(db.String(30))
    package_title=db.Column(db.String(150))
    period=db.Column(db.String(50))
    dep_date=db.Column(db.Date)
    arrival_date=db.Column(db.Date)
    price=db.Column(db.Integer)
    #id_proof=db.Column(db.String(150))
    def __repr___(self):
        return '<Task %r>' % self.id

class city(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    img=db.Column(db.String(100))
    def __repr___(self):
        return '<Task %r>' % self.id

class details(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    price = db.Column(db.Integer)
    location = db.Column(db.String(70))  
    img=db.Column(db.String(100))
    subheading=db.Column(db.String(100))
    body=db.Column(db.String(100))
    
    def __repr___(self):
        return '<Task %r>' % self.id        

@app.route('/')
def home():
    l=[]
    result=[]
    stms=city.query.all()
    for stm in stms:
        l.extend([stm.id,stm.name,stm.img])
        result.append(l)
        l=[]
    return render_template('/index.html',res=result)

@app.route('/package_details/<string:name>')
def package_details(name):
    l=[]
    stm=details.query.filter_by(title=name).first()
    l.extend([stm.id,stm.title,stm.price,stm.location,stm.img,stm.subheading,stm.body])
    return render_template("/details.html",res=l)

@app.route('/package_/<string:pid>')
def package_(pid):
    l=[]
    result=[]
    rows=details.query.filter_by(location=pid).all()
    for stm in rows:
        l.extend([stm.id,stm.title,stm.price,stm.location,stm.img])
        result.append(l)
        l=[]
    return render_template("/package.html",res=result)

@app.route('/booking/<int:pid>',methods=['POST','GET'])
def booking(pid):
    l=[]
    row=details.query.filter_by(id=pid).first()
    l.extend([row.id,row.title,row.subheading])
    if 'f_name' in request.form and 'l_name' in request.form and 'phone' in request.form and 'email' in request.form and 'dep_date' in request.form and 'arrive_date' in request.form and 'count' in request.form :
        f_name= request.form['f_name']
        l_name= request.form['l_name']
        phone= request.form['phone']
        email= request.form['email']
        arrive_date= request.form['arrive_date']
        dep_date= request.form['dep_date']
        count= request.form['count']
        #id= request.form['pack']
        if f_name=="" or l_name=="" or phone=="" or email=="" or dep_date=="" or arrive_date=="" or count=="" or id=="":
            flash("Fields shouldnt be left empty")
            return redirect(url_for('booking',pid=pid))
        

        s=row.subheading
        a=0
        for i, c in enumerate(s):
            if a<2 and c.isdigit():
                a+=1
            break
        c=int(c)
        date=dep_date
        #date = datetime.datetime(dep_date)
        """
        for i in range(c): 
            date += datetime.timedelta(days=1)
        print(date)
        #date_after_month = datetime.now()+ relativedelta(day=1)
        """
        price=count*row.price
        book=booking_details(first_name=f_name,last_name=l_name,people_count=count,email=email,phone=phone,package_title=row.title,period=row.subheading,dep_date=dep_date,arrival_date=arrive_date,price=price)
        db.session.add(book)
        db.session.commit()
        return redirect('/')
        """except:
            #print("error")
            flash("Something went wrong!!!")
        """
        return redirect("/booking/pid")
    else:
        return render_template("/booking.html",res=l)

@app.route('/admin_login',methods=['POST','GET'])
def admin_login():
    if 'email' in request.form and 'password' in request.form:
        us = request.form['email']
        password = request.form['password']
        if us == "" or password == "":
            flash("Fields shouldnt be left empty")
            return redirect('/admin_login')
        if us=="admin@gmail.com" and password=="admin@123":
            session['user']='admin'
            return render_template("/dashdetails.html",name=session['user'])
        else:
            flash("Incorrect email/password")
            return redirect('/admin_login')
    return render_template("/admin_login.html")

@app.route('/admin_dashboard')
def admin_dasboard():
    #if session['user']=='admin':
    if 'user' in session:
        pass
    else:
        return render_template("/admin_login.html")
    return render_template("/dashdetails.html",name=session['user'])

@app.route('/admin_citydetails')
def admin_citydetails():
    if 'user' in session:
        pass
    else:
        return render_template("/admin_login.html")
    return render_template("/admin.html",name=session['user'])

@app.route('/admin_logout')
def admin_logout():
    if 'user' in session:  
        session.pop('user',None) 
    return render_template("/admin_login.html")

    



if __name__ == "__main__":
    app.run(debug=True)

#{{url_for('package_details',pid=i[0])}}
