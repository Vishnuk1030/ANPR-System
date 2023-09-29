from re import A
from cv2 import trace
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_cors import CORS

mydb = mysql.connector.connect(
    #put your sql username password host and database
    host="sqlserver",
    user="root",
    passwd="changepassword",
    database="mf"
)


app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('home.html')
    

@app.route('/result')
def result():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findV")
    myresult = mycursor.fetchall()
    return render_template('result.html', results=myresult,)

@app.route('/results/<string:vehno>')
def results(vehno):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Latitude,Longitude FROM findV WHERE Vehno = %s", (vehno,))
    myresult = mycursor.fetchall()
    return render_template('results.html', results=myresult) 

@app.route('/result/<string:vehno>')
def result_vehno(vehno):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findV where Vehno = %s", (vehno,))
    myresult = mycursor.fetchall()
    return render_template('result.html', results=myresult,)

@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'GET':
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM findV")
        myresult = mycursor.fetchall()
        return render_template('gmap.html', page_data=myresult,)
    if request.method == 'POST':
        vno = request.form.get('vno')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM findBlock where Vehno = %s", (vno,))
        myresult = mycursor.fetchall()
        return render_template('gmap.html',page_data=myresult,)
    else:
        return render_template('gmap.html')

@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        Vehno = request.form.get('Vehno')
        Location = request.form.get('Location')
        mycursor = mydb.cursor()  
        mycursor.execute('''INSERT INTO findV(Vehno,Location) VALUES(%s,%s)''',(Vehno,Location))
        mydb.commit()
        mydb.close()
        return render_template("index.html")
    else:
        return render_template("index.html")
@app.route('/other')
def other():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findBlock")
    myresult = mycursor.fetchall()
    return render_template('other.html', results=myresult,)
    #return render_template('other.html')

@app.route('/block', methods=['GET','POST'])
def block():
    #return render_template("block.html")
    if request.method == 'GET':
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM findBlock")
        myresult = mycursor.fetchall()
        mycursor.execute("select * from blockNO")
        myresult2 = mycursor.fetchall()
        for x in myresult2:
            for i in myresult:
                if i[0] == x[0]:
                    mycursor.execute("SELECT * FROM findBlock WHERE Vehno = %s", (x[0],))
                    resul = mycursor.fetchall()
                    print(resul)
                    return render_template("block.html",results=resul)
                else:
                    print('no found')
        return render_template("block.html")
    if request.method == 'POST':
        Vehno = request.form.get('block')
        mycursor = mydb.cursor()
        mycursor.execute("insert into blockNO(vno) values(%s)",(Vehno,))
        mydb.commit()
        mydb.close()
        return render_template("block.html")

@app.route('/test')
def test():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM findV")
    myresult = mycursor.fetchall()
    return render_template('test.html', page_data=myresult,)
if __name__ == '__main__':
    app.run(debug=True)
