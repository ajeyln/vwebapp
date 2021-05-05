from flask import Flask, request, render_template, send_from_directory
import os, os.path
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib import style
import pandas as pd
from fpdf import FPDF
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user_data.db")
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME1 = os.path.join(CURRENT_DIR, "static")
FILE_NAME = os.path.join(FILE_NAME1, "plotter_images")

app = Flask(__name__, template_folder='template')

@app.errorhandler(404)
def page_notfound(self):
    return render_template('error.html')

@app.route('/')
@app.route('/home/')
def get_home():
    get_header()
    return render_template('index.html')

@app.route('/contact')
def get_contactinfor():
    return render_template('contact.html')

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

@app.route('/statistic', methods= ['GET'])
def get_statistic():
    return render_template('statistic.html')

@app.route('/statistic', methods= ['POST'])
def put_statistic():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("select * from users ")
    rows = cur.fetchall()
    user_list = []
    [user_list.append(list(row)) for row in rows]
    users_dataframe = pd.DataFrame(rows, columns=['SR_No','FIRST_NAME','SECOND_NAME','AGE','GENDER','CITY'])
    if request.form['plot'] == 'Line Graph' or request.form['plot'] == 'Bar Graph':
        if request.form['plot'] == 'Line Graph':
            create_line_graph(user_list, users_dataframe)
        else:
            create_bar_graph(user_list, users_dataframe)
    elif request.form['plot'] == 'Histogram' or request.form['plot'] == 'Scatter Plot':
        if request.form['plot'] == 'Histogram':
            create_histogram(users_dataframe)
        else:
            create_scatter_plot(users_dataframe)
    else:
        if request.form['plot'] == 'Pie Chart':
            create_pie_chart(users_dataframe)

def create_line_graph(user_list, users_dataframe):
    style.use('ggplot')
    female_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Female"]
    city_name_female = female_dataframe['CITY'].to_list()
    city_users_female = []
    [city_users_female.append(x) for x in city_name_female if x not in city_users_female]
    print(city_users_female)

    male_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Male"]
    city_name_male = male_dataframe['CITY'].to_list()
    city_users_male = []
    [city_users_male.append(y) for y in city_name_male if y not in city_users_male]
    print(city_users_male)

    other_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Other"]
    city_name_other = other_dataframe['CITY'].to_list()
    city_users_other = []
    [city_users_other.append(z) for z in city_name_other if z not in city_users_other]
    print(city_users_other)
    
    for i in range(0, len(city_users_female)):
        count_female = 0
        female_count = []
        for j in range(0, len(user_list)):
            if user_list[j][4] == "Female" and user_list[j][5] == city_users_female[i]:
                count_female += 1
        female_count.append(count_female)
    print(female_count)

    for k in range(0, len(city_users_male)):
        male_count = []
        print(city_users_male[k])
        count_male = 0
        for l in range(0, len(user_list)):
            if user_list[l][4] == "Male" and user_list[l][5] == city_users_male[k]:
                count_male += 1
                print(count_male)
            male_count.append(count_male)
    print(male_count)

    for m in range(0, len(city_users_other)):
        count_other = 0
        other_count = []
        for n in range(0, len(user_list)):
            if user_list[n][4] == "Other" and user_list[n][5] == city_users_other[m]:
                count_other += 1
        other_count.append(count_other)
    print(other_count)

    plt.plot(city_users_female,female_count,'b',label='Female', linewidth=5)
    # plt.plot(city_users_male,male_count,'g',label='Male', linewidth=5)
    plt.plot(city_users_other,other_count,'r',label='Other',linewidth=5)
    plt.title('Residence of Cities')
    plt.ylabel('Count')
    plt.xlabel('City Name')
    plt.legend(loc ="upper right", prop={"size":10})
    filepath = os.path.join(FILE_NAME,"01_line_plot.png")
    plt.savefig(filepath)
    msg = "The line graph shows Employee count with respect to their Cities."
    image_path = os.path.join(FILE_NAME, "01_line_plot.png")
    return render_template('plot.html', msg = msg, image = image_path)

def create_histogram(users_dataframe):
    age_users = users_dataframe['AGE'].to_list()
    bins = []
    [bins.append(x) for x in range(10,80,10)]
    plt.hist(age_users, bins, histtype='bar', rwidth=0.3)
    plt.title('Age Info')
    plt.ylabel('Count')
    plt.xlabel('Age')
    plt.legend(loc ="upper right", prop={"size":10})
    filepath = os.path.join(FILE_NAME, "03_histogram.png")
    plt.savefig(filepath)
    msg = "In this section, we are plotting the graph based on User age with duration of 10 Years"
    image_path = os.path.join(FILE_NAME, "03_histogram.png")
    return render_template('plot.html', msg = msg, image = image_path)

def create_bar_graph(user_list, users_dataframe):
    width = 0.2
    female_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Female"]
    sur_name_female = female_dataframe['SECOND_NAME'].to_list()
    sec_name_female = []
    [sec_name_female.append(x) for x in sur_name_female if x not in sec_name_female]
    print(sec_name_female)

    male_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Male"]
    sur_name_male = male_dataframe['SECOND_NAME'].to_list()
    sec_name_male = []
    [sec_name_male.append(y) for y in sur_name_male if y not in sec_name_male]
    print(sec_name_male)

    other_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Other"]
    sur_name_other = other_dataframe['SECOND_NAME'].to_list()
    sec_name_other = []
    [sec_name_other.append(z) for z in sur_name_other if z not in sec_name_other]
    print(sec_name_other)

    for i in range(0, len(sec_name_female)):
        count_female = 0
        female_count = []
        for j in range(0, len(user_list)):
            if user_list[j][2] == sec_name_female[i] and user_list[j][4] == "Female":
                count_female += 1
        female_count.append(count_female)
    print(female_count)

    for k in range(0, len(sec_name_male)):
        male_count = []
        print(sec_name_male[k])
        count_male = 0
        for l in range(0, len(user_list)):
            if user_list[l][2] == sec_name_male[k] and user_list[l][4] == "Male":
                count_male += 1
                print(count_male)
        male_count.append(count_male)
    print(male_count)

    for m in range(0, len(sec_name_other)):
        count_other = 0
        other_count = []
        for n in range(0, len(user_list)):
            if user_list[n][2] == sec_name_other[m] and user_list[n][4] == "Other":
                count_other += 1
        other_count.append(count_other)
    print(other_count)

    plt.bar(sec_name_female,female_count, label="Female",color='b', width=width)
    plt.bar(sec_name_male,male_count, label="Male",color='g', width=width)
    plt.bar(sec_name_other,other_count, label="Other", color='r', width=width)
    plt.title('User details with their Second Names')
    plt.ylabel('Count')
    plt.xlabel('Year')
    plt.legend(loc ="upper right", prop={"size":10})
    filepath = os.path.join(FILE_NAME,"02_bar_graph.png")
    plt.savefig(filepath)
    msg = "The line graph shows Employee count with respect to their Second Names."
    image_path = os.path.join(FILE_NAME, "02_bar_graph.png")
    return render_template('plot.html', msg = msg, image = image_path)

def create_scatter_plot(users_dataframe):
    female_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Female"]
    age_female = female_dataframe["AGE"].to_list()
    city_female = female_dataframe["CITY"].to_list()

    male_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Male"]
    age_male = male_dataframe["AGE"].to_list()
    city_male = male_dataframe["CITY"].to_list()

    other_dataframe = users_dataframe.loc[users_dataframe["GENDER"] == "Other"]
    age_other = other_dataframe["AGE"].to_list()
    city_other = other_dataframe["CITY"].to_list()
    plt.scatter(city_female, age_female, label='Female',color='b')
    plt.scatter(city_male, age_male,label='Male',color='g')
    plt.scatter(city_other, age_other,label='Other',color='r')
    plt.title('Age of Users(Male vs Female)')
    plt.ylabel('City')
    plt.xlabel('Age')
    plt.legend(loc ="upper right", prop={"size":10})
    filepath = os.path.join(FILE_NAME, "04_scatter_plot.png")
    plt.savefig(filepath)
    msg = "The scatter graph shows the Age of Male and Female based on their Cities."
    image_path = os.path.join(FILE_NAME, "04_scatter_plot.png")
    return render_template('plot.html', msg = msg, image = image_path)

def create_pie_chart(users_dataframe):
    city_karkala = users_dataframe.loc[users_dataframe["CITY"] == "Karkala"]
    city_mangalore = users_dataframe.loc[users_dataframe["CITY"] == "Mangalore"]
    city_mumbai = users_dataframe.loc[users_dataframe["CITY"] == "Mumbai"]
    city_bangalore = users_dataframe.loc[users_dataframe["CITY"] == "Bangalore"]
    city_udupi = users_dataframe.loc[users_dataframe["CITY"] == "Udupi"]
    city_kundapura = users_dataframe.loc[users_dataframe["CITY"] == "Kundapura"]
    count_karkala_user = len(city_karkala.index)
    count_mangalore_user = len(city_mangalore.index)
    count_mumbai_user = len(city_mumbai.index)
    count_bangalore_user = len(city_bangalore.index)
    count_udupi_user = len(city_udupi.index)
    count_kundapura_user = len(city_kundapura.index)

    slices = [count_karkala_user, count_mangalore_user, count_mumbai_user, count_bangalore_user, count_udupi_user, count_kundapura_user]
    Age_of_Employees = ['Karkala','Mangalore','Mumbai','Bangalore','Udupi','Kundapura']
    cols = ['lightgray','coral','yellow','red','mediumpurple','lightblue']
    plt.pie(slices,
    labels= Age_of_Employees,
    colors=cols,
    startangle=90,
    shadow= True,
    autopct='%1.1f%%')
    plt.title('Residence of Users')
    plt.legend()
    filepath = os.path.join(FILE_NAME, '05_pie_chart.png')
    plt.savefig(filepath)
    msg = "Percentagewise City of Users "
    image_path = os.path.join(FILE_NAME, "05_pie_chart.png")
    return render_template('plot.html', msg = msg, image = image_path)

def create_pdf(cur):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(225, 10, txt= "Statistical Report", ln = 1, align = "C")
    pdf.multi_cell(200, 10, txt= "The line graph shows Employee count with respect to their joining year and there are two lines, one reprsents to Female and another to Male in a company.", align = "l")
    file_image1 = os.path.join(FILE_NAME, "01_line_plot.png")
    pdf.image(file_image1, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt= "In this task, The Bar graph shows the Average salary of the Female and Male based on their joing years.", ln = 4, align = "l")
    file_image2 = os.path.join(FILE_NAME, "02_bar_graph.png")
    pdf.image(file_image2, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt= "In this section, we are plotting the graph based on Employees age with duration of 5 Years.", ln = 6, align = "l")
    file_image3 = os.path.join(FILE_NAME, "03_histogram.png")
    pdf.image(file_image3, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt= "The scatter graph shows the salary of Male and Female based on their experience on company.", ln = 8, align = "l")
    file_image4 = os.path.join(FILE_NAME, "04_scatter_plot.png")
    pdf.image(file_image4, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt= "In the Piechart, we can find the agewise employee percentage of company.",ln = 10, align = "l")
    file_image5 = os.path.join(FILE_NAME, "05_pie_chart.png")
    pdf.image(file_image5, x = None, y = None, w=700/5, h=450/5, type = 'png', link = '')
    pdf_path = os.path.join(CURRENT_DIR, "statistics")
    pdf_file = os.path.join(pdf_path, "Statistic.pdf")
    pdf.output(pdf_file,'F')

@app.route('/download')
def downloadFile ():
    return send_from_directory(directory=files_folder, filename="Statistic.pdf")

if __name__ == '__main__':

    app.run(port= 5555, debug = True)