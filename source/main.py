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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(CURRENT_DIR, "user_data.db")

app = Flask(__name__, template_folder='template')

INDEX_IMAGES = os.path.join("static", "images")
IMAGES_FOLDER = os.path.join("static", "plotter_images")
PDF_FOLDER = os.path.join("static", "statistics")

@app.errorhandler(404)
def page_notfound(self):
    return render_template('error.html')

@app.route('/')
@app.route('/home/')
def get_home():
    get_header()
    image1= os.path.join(INDEX_IMAGES, "svt.jpg")
    image2= os.path.join(INDEX_IMAGES, "svt1.jpg")
    return render_template('index.html', image1=image1, image2=image2)

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
    if request.form['plot'] == 'Line Graph':
        MESSAGE1_T = "Statistical Image(Line Graph)"
        MESSAGE1 = "The line graph shows Employee count with respect to their Cities."
        IMAGE_FILE1 = create_line_graph(user_list, users_dataframe)
        return render_template('plot.html', msg1=MESSAGE1_T, msg2=MESSAGE1,image = IMAGE_FILE1)

    elif request.form['plot'] == 'Bar Graph':
        MESSAGE2_T = "Statistical Image(Bar Graph)"
        MESSAGE2 = "The bar graph shows Employee count with respect to their Second Names."
        IMAGE_FILE2 = create_bar_graph(user_list, users_dataframe)
        return render_template('plot.html', msg1=MESSAGE2_T, msg2=MESSAGE2,image = IMAGE_FILE2)

    elif request.form['plot'] == 'Histogram':
        MESSAGE3_T = "Statistical Image(Histogram)"
        MESSAGE3 = "In this section, we are plotting the graph based on User age with duration of 10 Years"
        IMAGE_FILE3 = create_histogram(users_dataframe)
        return render_template('plot.html', msg1=MESSAGE3_T, msg2=MESSAGE3,image = IMAGE_FILE3)

    elif request.form['plot'] == 'Scatter Plot':
        MESSAGE4_T = "Statistical Image(Scatter Plot)"
        MESSAGE4 = "The scatter graph shows the Age of Male and Female based on their Cities."
        IMAGE_FILE4 = create_scatter_plot(users_dataframe)
        return render_template('plot.html', msg1=MESSAGE4_T, msg2=MESSAGE4,image = IMAGE_FILE4)
    else:
        MESSAGE5_T = "Statistical Image(Pie Chart)"
        MESSAGE5 = "Percentagewise City of Users"
        IMAGE_FILE5 = create_pie_chart(users_dataframe)
        return render_template('plot.html', msg1=MESSAGE5_T, msg2=MESSAGE5,image = IMAGE_FILE5)

def create_line_graph(user_list, users_dataframe):
    style.use('ggplot')
    city_name = users_dataframe['CITY'].to_list()
    users_city = []
    [users_city.append(z) for z in city_name if z not in users_city]
    
    female_count = []
    for i in range(0, len(users_city)):
        count_female = 0
        for j in range(0, len(user_list)):
            if user_list[j][4] == "Female" and user_list[j][5] == users_city[i]:
                count_female += 1
        female_count.append(count_female)

    male_count = []
    for k in range(0, len(users_city)):
        count_male = 0
        for l in range(0, len(user_list)):
            if user_list[l][4] == "Male" and user_list[l][5] == users_city[k]:
                count_male += 1
        male_count.append(count_male)

    other_count = []
    for m in range(0, len(users_city)):
        count_other = 0
        for n in range(0, len(user_list)):
            if user_list[n][4] == "Other" and user_list[n][5] == users_city[m]:
                count_other += 1
        other_count.append(count_other)

    plt.plot(users_city,female_count,'b',label='Female', linewidth=5)
    plt.plot(users_city,male_count,'g',label='Male', linewidth=5)
    plt.plot(users_city,other_count,'r',label='Other',linewidth=5)
    plt.title('Residence of Cities')
    plt.ylabel('Count')
    plt.xlabel('City Name')
    plt.legend(loc ="upper right", prop={"size":10})
    IMAGE_FILE = os.path.join(IMAGES_FOLDER,"01_line_plot.png")
    plt.savefig(IMAGE_FILE)
    return IMAGE_FILE

def create_histogram(users_dataframe):
    age_users = users_dataframe['AGE'].to_list()
    bins = []
    [bins.append(x) for x in range(10,80,10)]
    plt.hist(age_users, bins, histtype='bar', rwidth=0.3)
    plt.title('Age Info')
    plt.ylabel('Count')
    plt.xlabel('Age')
    plt.legend(loc ="upper right", prop={"size":10})
    IMAGE_FILE = os.path.join(IMAGES_FOLDER, "03_histogram.png")
    plt.savefig(IMAGE_FILE)
    return IMAGE_FILE

def create_bar_graph(user_list, users_dataframe):
    width = 0.2
    sur_name = users_dataframe['SECOND_NAME'].to_list()
    sec_name = []
    [sec_name.append(x) for x in sur_name if x not in sec_name]

    female_count = []
    for i in range(0, len(sec_name)):
        count_female = 0
        for j in range(0, len(user_list)):
            if user_list[j][2] == sec_name[i] and user_list[j][4] == "Female":
                count_female += 1
        female_count.append(count_female)

    male_count = []
    for k in range(0, len(sec_name)):
        count_male = 0
        for l in range(0, len(user_list)):
            if user_list[l][2] == sec_name[k] and user_list[l][4] == "Male":
                count_male += 1
        male_count.append(count_male)

    other_count = []
    for m in range(0, len(sec_name)):
        count_other = 0
        for n in range(0, len(user_list)):
            if user_list[n][2] == sec_name[m] and user_list[n][4] == "Other":
                count_other += 1
        other_count.append(count_other)

    plt.bar(sec_name,female_count, label="Female",color='b', width=width)
    plt.bar(sec_name,male_count, label="Male",color='g', width=width)
    plt.bar(sec_name,other_count, label="Other", color='r', width=width)
    plt.title('User details with their Second Names')
    plt.ylabel('Count')
    plt.xlabel('Year')
    plt.legend(loc ="upper right", prop={"size":10})
    IMAGE_FILE = os.path.join(IMAGES_FOLDER,"02_bar_graph.png")
    plt.savefig(IMAGE_FILE)
    return IMAGE_FILE

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
    IMAGE_FILE = os.path.join(IMAGES_FOLDER, "04_scatter_plot.png")
    plt.savefig(IMAGE_FILE)
    return IMAGE_FILE

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
    IMAGE_FILE = os.path.join(IMAGES_FOLDER, '05_pie_chart.png')
    plt.savefig(IMAGE_FILE)
    return IMAGE_FILE

@app.route('/download')
def create_pdf():
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(225, 10, txt= "Statistical Report", ln = 1, align = "C")
    pdf.multi_cell(200, 10, txt= "The line graph shows Employee count with respect to their Cities.", align = "l")
    file_image1 = os.path.join(IMAGES_FOLDER, "01_line_plot.png")
    pdf.image(file_image1, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt=  "The bar graph shows Employee count with respect to their Second Names.", ln = 4, align = "l")
    file_image2 = os.path.join(IMAGES_FOLDER, "02_bar_graph.png")
    pdf.image(file_image2, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt= "In this section, we are plotting the graph based on User age with duration of 10 Years", ln = 6, align = "l")
    file_image3 = os.path.join(IMAGES_FOLDER, "03_histogram.png")
    pdf.image(file_image3, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt= "The scatter graph shows the Age of Male and Female based on their Cities.", ln = 8, align = "l")
    file_image4 = os.path.join(IMAGES_FOLDER, "04_scatter_plot.png")
    pdf.image(file_image4, x = None, y = None, w=700/5, h=450/5, type = '')
    pdf.cell(200, 10, txt= "Percentagewise City of Users ",ln = 10, align = "l")
    file_image5 = os.path.join(IMAGES_FOLDER, "05_pie_chart.png")
    pdf.image(file_image5, x = None, y = None, w=700/5, h=450/5, type = 'png', link = '')
    PDF_FILE = os.path.join(PDF_FOLDER, "Statistic.pdf")
    if os.path.exists(PDF_FILE):
        os.remove(PDF_FILE)
    pdf.output(PDF_FILE,'F')
    msg = f"The files sucessfully downloaded in this location : {PDF_FILE}"
    return render_template('download.html', msg = msg,)

if __name__ == '__main__':

    app.run(port= 5555, debug = True)