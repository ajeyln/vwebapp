from flask import Flask, request, render_template
import os
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

@app.route('/register', methods=['GET'])
def reg_user():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def get_user():
    srno = request.form.get('Index Number')
    first = request.form.get('First Name')
    second = request.form.get('Second Name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    city = request.form.get('city')
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (SR_No integer primary key,\
                FIRST_NAME varchar(15), SECOND_NAME varchar(15), AGE integer,\
                GENDER varchar(15), CITY varchar(15))''')
    c.execute(f"insert into users values({srno}, \'{first}\', \'{second}\', {age}, \'{gender}\', \'{city}\')")
    c.execute('PRAGMA table_info(users)')
    dummy_list_header = [list(x) for x in c.fetchall()]
    list_header = [dummy_list_header[y][1] for y in range(0, len(dummy_list_header))]
    print(list_header)
    return create_html(srno, first, second, age, gender, city)

def create_html(srno, first, second, age, gender, city):
    if os.path.exists("template\success.html"):
        os.remove("template\success.html")
    with open("template\success.html", "w") as data:
        data.write(f'''<!DOCTYPE html>
                <html>
                <title>Sucess !!!!!</title>
                <body style="background-color: green;">
                <h1 align="center">Registration Completed</h1>
                <h2> You have registered with following details : <br />
                Index Number: {srno} <br />
                First Name: {first} <br />
                Second Name: {second} <br />
                Age: {age} <br />
                Gender: {gender} <br />
                City: {city} </h2>
                </html>''')
    return render_template('success.html')

@app.route('/list', methods= ['GET'])
def user_list():
    return render_template('user details.html')

if __name__ == '__main__':

    app.run(port= 5555, debug = True)