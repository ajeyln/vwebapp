from flask import Flask, request, render_template
from flask import send_from_directory
import os, os.path
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user_data.db")

app = Flask(__name__, template_folder='template')

IMAGES_FOLDER=os.path.join('static', 'images')
FILES_FOLDER=os.path.join('files')

@app.errorhandler(404)
def page_notfound(self):
    return render_template('error.html')

@app.route('/')
@app.route('/home/')
def get_home():
    get_header()
    i1=os.path.join(IMAGES_FOLDER, "svt.jpg")
    i2=os.path.join(IMAGES_FOLDER, "svt1.jpg")
    return render_template('index.html', i1=i1, i2=i2)

@app.route('/contact')
def get_contactinfor():
    return render_template('contact.html')


@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    return send_from_directory(directory=FILES_FOLDER, filename="WL-2.pdf")
    
def get_header():
    conn = sqlite3.connect(db_path)
    print('Opened database successfully')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (SR_No integer primary key AUTOINCREMENT,\
                FIRST_NAME varchar(15), SECOND_NAME varchar(15), AGE integer,\
                GENDER varchar(15), CITY varchar(15))''')
    print("Table created successfully")

@app.route('/register', methods=['GET'])
def reg_user():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def get_user():
    srno = request.form['srno']
    first = request.form['first']
    second = request.form['second']
    age = request.form['age']
    gender = request.form['gender']
    city = request.form['city']

    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (FIRST_NAME,SECOND_NAME,AGE,GENDER,CITY)\
            VALUES (?,?,?,?,?)",(first,second,age,gender,city))
        con.commit()
        msg = "Record successfully added"
    return render_template('success.html', msg = msg)

@app.route('/delete', methods=['GET'])
def delete_user():
    return render_template('delete.html')

@app.route('/delete', methods = ["POST"])  
def deleterecord():  
    srno = request.form["srno"]  
    with sqlite3.connect(db_path) as con:  
        try:  
            cur = con.cursor()
            cur.execute("delete from users where SR_NO = ?",srno)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("deleterecord.html",msg = msg)

@app.route('/update', methods=['GET'])
def update():
    return render_template('update.html')

@app.route('/update', methods= ['POST'])
def update_user():
    srno = request.form['srno']
    first = request.form['first']
    second = request.form['second']
    age = request.form['age']
    gender = request.form['gender']
    city = request.form['city']
    with sqlite3.connect(db_path) as con:  
        try:  
            cur = con.cursor()
            cur.execute("UPDATE users SET FIRST_NAME = ?, SECOND_NAME = ?, AGE = ?, GENDER = ?,\
                         CITY = ? where SR_NO = ?", (first,second,age,gender,city,srno) ) 
            msg = "record successfully updated"  
        except:  
            msg = "can't be updated"  
        finally:  
            return render_template('updated.html', msg = msg)

@app.route('/list', methods= ['GET'])
def user_list():
    if os.path.exists("userlist.html"):
        os.remove("userlist.html")
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    return render_template('userlist.html', rows = rows)

if __name__ == '__main__':

    app.run(port= 5555, debug = True)