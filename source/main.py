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

@app.route('/register')
def reg_user():
    return render_template('registration.html')

if __name__ == '__main__':
    app.run(port= 5555, debug = True)