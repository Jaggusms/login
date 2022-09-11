from distutils.log import debug
from select import select
from flask import Flask,request,render_template 
import pyodbc
import numpy as np
import pandas as pd
connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
            "Server=JAGADEESH-MS\JAGADEESHM;"
            "Database=JAGGU;"
            "Trusted_Connection=yes;");# Creating Cursor    
    
cursor = connection.cursor()



app = Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/validation_login',methods=['POST','GET'])
def validation_login():
    aadhar=request.form['aadhar']
    pwd=request.form['password']
    if len(str(aadhar))==0 or len(str(pwd))==0:
        return render_template('login.html')
    try:
        aadhar=int(aadhar)
    except:
        pass
    data=pd.read_sql_query('select * from jaggu',connection)
    if aadhar not in list(data['aadhar']):
	    return render_template('login.html',info='Invalid User')
    else:
        if pwd not in list(data['password']):
            return render_template('login.html',info='Invalid Password')
        else:
            name=list(data['name'])[list(data['aadhar']).index(aadhar)]
            return render_template('home.html',name=name)
    

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/uplode_database",methods=['POST','GET'])
def uplode_database():
    name1=request.form['name']
    aadhar=request.form['aadhar']
    mail=request.form["email"]
    pwd=request.form['password']
    data=pd.read_sql_query('select * from jaggu',connection)
    try:
        aadhar=int(aadhar)
    except:
        pass
    if len(str(aadhar))==0 or len(str(name1))==0 or len(str(mail))==0 or len(str(pwd))==0 :
        return render_template('register.html')
    if len(str(aadhar))!=12 or isinstance(aadhar,str):
        return render_template('aadhar_validation.html',info='please enter correct format of aadhar which is only 12 digits of number')
    if mail in list(data['email']) or aadhar in list(data['aadhar']):
	    return render_template('login.html',info='Alreaday User please login')
    cursor.execute("INSERT INTO jaggu values ('{0}','{1}','{2}',{3})".format(name1,mail,pwd,aadhar))
    connection.commit()
    return render_template("home.html",name=name1)

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")
@app.route("/password",methods=['POST','GET'])
def password():
    data=pd.read_sql_query('select * from jaggu',connection)
    aadhar=request.form['aadhar']
    if len(aadhar)<12:
        return render_template("password.html", password="please enter correct aadhar")
    try:
        aadhar=int(aadhar)
    except:
        pass
    value=list(data[data['aadhar']==aadhar]['password'])
    password='please enter correct aadhar'
    if bool(value):
        password=value[0]
    return render_template("password.html", password=password)
if __name__ == '__main__':
    app.run(debug=True)
