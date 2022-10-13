from operator import contains
from time import sleep
from flask import Flask, render_template, request, url_for
import flask

app = Flask(__name__)
app.config['DEBUG'] = True

email_address= ""
correct_email = "test@local.local"
password = ""
correct_password = "Password123"
invalid_password = "<b>You have entered the an invalid password.</b>"
wrong_password = "<b>You have entered the wrong password for that email address.</b>"
invalid_email = "<b>You have entered an invalid email address.</b>"
emtpy_field = "<b>You have left the email or password field empty. Please enter your credentials.</b>"
error_message = ""


def verify_email_is_valid(email_address):
    if contains(email_address,"@") and contains(email_address,".") and len(email_address) > 3 and len(email_address) < 20:
        print("Email is valid.")
        return True
    else:
        error_message = invalid_password
        return error_message

def verify_password_is_valid(password):
    if len(password) > 3 and len(password) <20:
        print("Password is valid.")
        return True
    else:
        error_message = invalid_password
        return error_message

def verify_credentials(email_address,password):
    if correct_email == email_address and correct_password == password:
        print("The credentials are correct.")
    else:
        print("Ehh, not right.")
        error_message = wrong_password
        return error_message

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/",methods=['POST'])
def submit(emailAddress=None,passWord=None):
    email_address = (request.form['emailAddress'])
    password = (request.form['passWord'])
    print(password + " is the password " + email_address + " is the email address")
    verify_email_is_valid(email_address)
    verify_password_is_valid(password)
    display_welcome_page()
    if verify_credentials(email_address,password) == True:
        display_welcome_page()
        print("Go to welcome page")
    else:
        return render_template("index.html",
        errorMessage = error_message)

@app.route("/welcome")
def welcome():
    print("welcome")
    return render_template("welcome.html")

def display_welcome_page():
    flask.redirect(url_for("welcome"))

app.run()