from flask import Flask, request, render_template


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

@app.route('/register', methods=['GET','POST'])
def reg_user():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        city = request.form.get('city')
        with open("userdata.csv", "a") as file_name:
            file_name.write("{};{};{};{}".format(name, age, gender, city))
    return render_template('registration.html')

@app.route('/list')
def user_list():
    return render_template('userdata.csv')

if __name__ == '__main__':
    app.run(port= 5555, debug = True)