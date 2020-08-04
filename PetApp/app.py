from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import random
app=Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'petclinic'
mysql = MySQL(app)

app.secret_key = "mysecretkey"



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Pets ORDER BY id DESC LIMIT 15')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',pet=data)

@app.route('/addrecord',methods=['POST'])
def addrecord():
    if request.method=='POST':
        petname = request.form['petname']
        kind = request.form['kind']
        gender = request.form['gender']

        Age=int(request.form['Age'])
        
        Ownerfname=request.form['OwnerfName']
        Ownerlname=request.form['OwnerlName']
        City = request.form['City']
        State = request.form['State']
        Add=request.form['Address']
        OwnerID=random.randint(1000,9999)

        char=chr(random.randint(65,92))
        num=str(random.randint(0,10))
        num1=str(random.randint(1000,9999))
        l=[char,num,'-',num1]
        PetID=''.join(l)

        print(PetID)
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO owners(OwnerID,Name,Surname,StreetAddress,City,StateFull) VALUES (%s,%s,%s,%s,%s,%s)""",(OwnerID,Ownerfname,Ownerlname
        ,Add,City,State))
        mysql.connection.commit()
        cur.close()
        cur1=mysql.connection.cursor()
        cur1.execute("INSERT INTO Pets (PetID,Name,Kind,Gender,Age,OwnerID) VALUES (%s,%s,%s,%s,%s,%s)", (PetID,petname, kind, gender,Age,OwnerID))
        mysql.connection.commit()
        cur1.close()
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM messages ORDER BY id DESC LIMIT 1')
        d=cur.fetchall()
        if(d[0][1]=='1'):
            
            cur1=mysql.connection.cursor()
            cur1.execute("DELETE FROM pets where PetID='{id4}'".format(id4=PetID))
            mysql.connection.commit()
            cur1.close()
            cur=mysql.connection.cursor()
            
            flash("We don't treat wild animals here.Sorry!")
            return redirect(url_for('Index'))

        else:
            flash('Record added successfully')
            return redirect(url_for('Index'))

@app.route('/edit/<id1>', methods = ['POST', 'GET'])
def get_contact(id1):
    cur1 = mysql.connection.cursor()
    print(id1)
    cur1.execute('SELECT * FROM pets WHERE id = {id3}'.format(id3=id1))
    data = cur1.fetchall()
    
    cur1.close()
    print(data[0])
    return render_template('edit-contact.html', pet = data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        Name = request.form['Name']
        Kind = request.form['Kind']
        Gender = request.form['Gender']
        Age=request.form['Age']
        PID = request.form['petid']
        #OwnerID=request.form['OwnerID']
        
        cur = mysql.connection.cursor()
        #cur.execute("""UPDATE Owners SET OwnerID=%s  WHERE OwnerID={owd} """.format(OwnerID))
        #mysql.connection.commit()
        cur.execute("""UPDATE Pets SET Name = %s, Kind = %s,Gender = %s,Age=%s WHERE id = %s""", (Name, Kind, Gender,Age, id))

        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    print(id)
    cur.execute('DELETE FROM pets WHERE id = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/showmypets',methods=['POST'])
def showthepets():
    cur1 = mysql.connection.cursor()
    id1=request.form['petid']
    
    #cur1.execute('SELECT * FROM pets WHERE OwnerID = {id3}'.format(id3=id1))
    cur1.execute("""SELECT p.PetID,p.Name,pro.ProcedureType,pro.ProcedureSubCode,det.Price,p.OwnerID
                FROM petclinic.pets AS p LEFT JOIN petclinic.procedurehistory AS pro ON p.PetID=pro.PetID , 
                petclinic.proceduredetails as det 
                WHERE pro.ProcedureSubCode=det.ProcedureSubCode AND pro.ProcedureType=det.ProcedureType AND p.PetID= '{id3}' """.format(id3=id1))
    data = cur1.fetchall()
    
    cur1.close()
    print(data)
    return render_template('showpets.html', pets = data)

@app.route('/Addprocedurerecord',methods=['POST','GET'])
def addprocedurerecord():
    id1=request.form['petid1']
    ptype=request.form['proceduretype']
    psub=request.form['proceduresubcode']
    date=request.form['date']
    
    cur=mysql.connection.cursor()
    cur.execute('INSERT INTO procedurehistory(PetID,Date,ProcedureType,ProcedureSubCode) VALUES (%s,%s,%s,%s)',(id1,date,ptype,psub))
    mysql.connection.commit()
    cur.close()
    flash("Procedure details have been added")
    return redirect(url_for('Index'))
@app.route('/Check',methods=['POST'])
def printalldomains():
    proc=request.form['proceduretype1']
    cur=mysql.connection.cursor()
    cur.execute("""SELECT p1.PetID,p1.Name,p1.Kind,p1.OwnerID
                    FROM petclinic.pets as p1
                    WHERE p1.PetID in (SELECT p.PetID FROM petclinic.procedurehistory p,petclinic.pets as p2 WHERE p.ProcedureType='{id3}' ) 
""".format(id3=proc))
   
    data=cur.fetchall()
    return render_template('check.html',pets=data)

@app.route('/bill', methods = ['POST', 'GET'])
def makebill():
    
    return render_template('bill.html')
@app.route('/showbill',methods=['POST'])
def bill():
    id=request.form['petid']
    date=request.form['date']
    cur=mysql.connection.cursor()
    cur.execute("""SELECT p.PetID,p.Name,pro.ProcedureType,pro.ProcedureSubCode,det.Price,p.OwnerID,pro.Date
                FROM petclinic.pets AS p LEFT JOIN petclinic.procedurehistory AS pro ON p.PetID=pro.PetID , 
                petclinic.proceduredetails as det 
                WHERE pro.ProcedureSubCode=det.ProcedureSubCode AND pro.ProcedureType=det.ProcedureType AND p.PetID='{id3}' AND pro.Date='{dat}'
                """.format(dat=date,id3=id))
    
    data=cur.fetchall()
    cur=mysql.connection.cursor()
    cur.execute("""SELECT SUM(det.Price) AS Total
                FROM petclinic.pets AS p LEFT JOIN petclinic.procedurehistory AS pro ON p.PetID=pro.PetID , 
                petclinic.proceduredetails as det 
                WHERE pro.ProcedureSubCode=det.ProcedureSubCode AND pro.ProcedureType=det.ProcedureType AND p.PetID='{id3}' AND pro.Date='{dat}'
                """.format(dat=date,id3=id))
    da=cur.fetchall()
    cur.close()
    return render_template('showthebill.html',pets=data,data=da[0])
@app.route('/showold',methods=['POST','GET'])
def showold():
    cur=mysql.connection.cursor()
    cur.execute('SELECT PetID,Name,Age FROM pets ORDER BY Age DESC LIMIT 1')
    data=cur.fetchall()
    cur.close()
    return render_template('showold.html', pets=data)
@app.route('/showresult',methods=['POST','GET'])
def runthequery():
    query=request.form['results']
    print(query)
    cur=mysql.connection.cursor()
    cur.execute(query)
    data=cur.fetchall()
    l=len(data[0])
    l1=len(data)
    cur.close()
    return render_template('showresult.html',pets=data,l2=l1,length=l)
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
