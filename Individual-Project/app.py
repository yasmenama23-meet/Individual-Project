from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyAD4GfFEryVSOtmCwg8K31i9ARTCDnKPPQ",

  "authDomain": "yasmena1-d7852.firebaseapp.com",

  "projectId": "yasmena1-d7852",

  "storageBucket": "yasmena1-d7852.appspot.com",

  "messagingSenderId": "883793147528",

  "appId": "1:883793147528:web:8151bfd6c196e1badad13d",

  "measurementId": "G-NM1BS96RRV",
  "databaseURL": "https://yasmena1-d7852-default-rtdb.europe-west1.firebasedatabase.app/"} 

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db= firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#routes



@app.route('/home')
def home():
    user = db.child('Users').child(login_session['user']['localId']).get().val()
    return render_template("index.html", username= user['username'])

@app.route('/cart')
def cart():
    cart = db.child('cart').get().val()
    return render_template('cart.html', cart = cart)

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = 'Error'
            return error

    else: 
        return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        username= request.form['username']

        cart = {"chocolate":10, "almond":7, "cookie":5}
        login_session['cart']= cart
        db.child('cart').push(cart)
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email": email, "password": password, "username":username}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('home'))
        except:
            error = 'Error'
            return error
    else: 
        return render_template('signup.html')


















if __name__ == '__main__':
    app.run(debug=True)