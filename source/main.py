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
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    city = request.form.get('city')
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    # while creating the data base first time
    # c.execute('''create table users(NAME varchar(15) primary key, AGE integer,\
             # GENDER varchar(15), CITY varchar(15))''')
    c.execute(f"insert into users values(\"{name}\", {age}, \"{gender}\", \"{city}\")")
    if os.path.exists("template\success.html"):
        os.remove("template\success.html")
    with open("template\success.html", "w") as data:
        data.write(f'''<!DOCTYPE html>
                <html>
                <title>Sucess !!!!!</title>
                <body style="background-color: green;">
                <h1 align="center">Registration Completed</h1>
                <h2> You have registered with name {name} age {age} gender {gender} and city {city} </h2>
                </html>''')
    return render_template('success.html')

@app.route('/list')
def user_list():
    return render_template('userdata.csv')

if __name__ == '__main__':

    app.run(port= 5555, debug = True)