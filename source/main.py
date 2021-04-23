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
    print(f"insert into users values({srno}, \'{first}\', \'{second}\', {age}, \'{gender}\', \'{city}\')")
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
                <button  onclick="window.location.href='/register';">
                <h3 align = "center">OK</h3>
                </html>''')
    return render_template('success.html')

@app.route('/list', methods= ['GET'])
def user_list():
    if os.path.exists("userlist.html"):
        os.remove("userlist.html")
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('PRAGMA table_info(users)')
    dummy_list_header = [list(x) for x in c.fetchall()]
    list_header = [dummy_list_header[y][1] for y in range(0, len(dummy_list_header))]
    with open("userlist.html", "w") as head:
        head.write(f'''<!DOCTYPE html>
                <html>
                <title>Registered Details</title>)
                <head>
                <style>
                table 
                tr:nth-child(even)
                </style>
                </head>
                <body>
                <h2> USER DETAILS </h2>
                <table>
                    <tr>
                        <th>{list_header[0]}</th>
                        <th>{list_header[1]}</th>
                        <th>{list_header[2]}</th>
                        <th>{list_header[3]}</th>
                        <th>{list_header[4]}</th>
                        <th>{list_header[5]}</th>
                    </tr> ''')
    with open("userlist.html", "a") as column:
        list_column = create_list_column()
        for i in range(0, len(list_column)):
            column.write(f'''
                    <tr>
                        <th>{list_column[i][0]}</th>
                        <th>{list_column[i][1]}</th>
                        <th>{list_column[i][2]}</th>
                        <th>{list_column[i][3]}</th>
                        <th>{list_column[i][4]}</th>
                        <th>{list_column[i][5]}</th>
                    </tr>
                    ''')
            print(list_column[i][0])
            print(list_column[i][1])
            print(list_column[i][2])
            print(list_column[i][3])
            print(list_column[i][4])
            print(list_column[i][5])
            
    with open("userlist.html", "a") as conclusion:
        conclusion.write(f'''</table>
                        </body>
                        </html>''')
    return render_template('userlist.html')

def create_list_column():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("Select * from users")
    print(c.fetchall)
    list_values = [list(z) for z in c.fetchall()]
    return (list_values)

def user_details_html():
    return render_template('user_details.html')

if __name__ == '__main__':

    app.run(port= 5555, debug = True)