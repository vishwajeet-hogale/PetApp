from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app=Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysteriousman307'
app.config['MYSQL_DB'] = 'petclinic'
mysql = MySQL(app)

app.secret_key = "mysecretkey"
import pandas as pd
df=pd.read_csv('C:/Users/vishw/Desktop/New folder/section7/P9-Pets.csv')
cur = mysql.connection.cursor()
for i in df:
    
    cur.execute("INSERT INTO pets1 (PetID,Name,Kind,Gender,Age,OwnerID) VALUES (%s,%s,%s,%s,%s,%s)", (i[0],i[1],i[2],i[3],i[4],i[5]))
    mysql.connection.commit()
cur.close()