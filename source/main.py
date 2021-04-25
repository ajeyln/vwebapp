from flask import Flask, request, render_template
import os, time
import sqlite3

app = Flask(__name__, template_folder='template')

@app.errorhandler(404)
def page_notfound():
    return render_template('error.html')

@app.route('/')
@app.route('/home/')
def get_home():
    return render_template('index.html')

@app.route('/contact')
def get_contactinfor():
    return render_template('contact.html')

def get_header():
    conn = sqlite3.connect('database.db')
    print('Opened database successfully')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (SR_No integer primary key AUTOINCREMENT,\
                FIRST_NAME varchar(15), SECOND_NAME varchar(15), AGE integer,\
                GENDER varchar(15), CITY varchar(15))''')
    print("Table created successfully")
    conn.close()

@app.route('/register', methods=['GET'])
def reg_user():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def get_user():
    srno = request.form['Index Number']
    first = request.form['First Name']
    second = request.form['Second Name']
    age = request.form['age']
    gender = request.form['gender']
    city = request.form['city']
    get_header()
    with sqlite3.connect("user_data.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (SR_NO,FIRST_NAME,SECOND_NAME,AGE,GENDER,CITY)\
            VALUES (?,?,?,?,?,?)",(srno,first,second,age,gender,city))
        con.commit()
        msg = "Record successfully added"
        con.close()

@app.route('/list', methods= ['GET'])
def user_list():
    if os.path.exists("userlist.html"):
        os.remove("userlist.html")
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    return render_template('userlist.html', rows = rows)

if __name__ == '__main__':

    app.run(port= 5555, debug = True)