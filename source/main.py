from flask import Flask, request

app = Flask(__file__)

@app.route('/')
def get_home():
    return render_template('resource/index.html')

@app.route('/contact')
def get_contactinfor():
    return render_template('resource/contact.html')

@app.route('/userregister')
def reg_user():
    return render_template('resource/user_registration.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)