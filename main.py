from operator import contains
from time import sleep
from flask import Flask, abort, redirect, render_template, request, url_for
import flask

app = Flask(__name__)
app.config['DEBUG'] = True

class user():
    def __init__(self, username, email_address, password):
        self.username = username
        self.email_address = email_address
        self.password = password

username = ""
saved_username = ""
email_address = ""
saved_emailAddress = ""
password = ""
saved_password = ""
invalid_username = ""
invalid_email = ""
invalid_password = ""
wrong_combo = "You have entered the wrong password for that username/ username & email address."
emtpy_field = "You have this field empty. Please enter the appropriate information."
invalid_entry = "You have entered an invlaid value."
error_message = ""
access_granted = False

def verify_username_is_valid(entered_username):
    if contains(entered_username," ") != True and len(entered_username) > 3 and len(entered_username) < 20:
        global saved_username
        global username 
        username = entered_username
        if saved_username == "":
            saved_username = entered_username
        return True
    else:
        clear_password()
        global invalid_username
        invalid_username = "Invalid username."
        global error_message
        error_message = invalid_username
        #return render_template("index.html",
        #errorMessage = error_message,
        #invalidUsername = invalid_username)

def verify_email_is_valid(email_address):
    if contains(email_address,"@") and contains(email_address,".") and len(email_address) > 3 and len(email_address) < 20:
        global saved_emailAddress
        if saved_emailAddress == "":
            saved_emailAddress = email_address
        return True
    else:
        clear_password()
        global invalid_email
        invalid_email = "Invalid email address."
        global error_message
        error_message = invalid_email
        #return render_template("index.html",
        #errorMessage = error_message,
        #invalidEmail = invalid_email)

def verify_password_is_valid(password):
    if len(password) > 3 and len(password) <20 and contains(password," ") != True:
        global saved_password
        if saved_username == "":
            saved_password = password
        return True
    else:
        clear_password()
        global invalid_password
        invalid_password = "Invalid password."
        global error_message
        error_message = invalid_password
        #return render_template("index.html",
        #errorMessage = error_message,
        #invalidPassword = invalid_password)

def verify_credentials(username,email_address,password):
    valid1 = verify_username_is_valid(username)
    valid2 = verify_email_is_valid(email_address)
    valid3 = verify_password_is_valid(password)
    if valid1 == True and valid2 == True and valid3 == True:
        global access_granted
        access_granted = True
        return True
    else:
        global error_message
        error_message = invalid_entry
        return 

def check_credentials(username,email_address,password):
    global saved_username
    global saved_emailAddress
    global saved_password
    global error_message
    print(username + password + email_address)

    if saved_emailAddress != "":
        if username == saved_username and email_address == saved_emailAddress and password == saved_password:
            global access_granted
            access_granted = True
            clear_password()
            return True
        else:
            clear_password()
            error_message = wrong_combo
            return error_message

    if username == saved_username and password == saved_password:
        access_granted = True
        clear_password()
        return True
    else:
        clear_password()
        error_message = wrong_combo
        return error_message

def clear_password():
    global password
    password = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/",methods=['POST'])
def sign_up():
    username = (request.form['userName'])
    print(username)
    email_address = (request.form['emailAddress'])
    password = (request.form['passWord'])
    user1 = user(username,email_address,password)
    if verify_credentials(username,email_address,password) == True:
        clear_password()
        return display_welcome_page()
    else:
        global error_message
        print("Error: " + error_message)
        clear_password()
        return render_template("index.html",
        errorMessage = error_message,
        invalidUsername = invalid_username,userName=username,
        invalidEmail = invalid_email,emailAddress = email_address,
        invalidPassword = invalid_password,passWord = password)

@app.route("/welcome")
def welcome():
    print(f"Access granted? {access_granted}")
    if access_granted == True:
        global username
        return render_template("welcome.html",
        userName = username)
    else:
        #abort(403)
        #sleep(2)
        return flask.redirect(url_for("index"))

@app.route("/clear")
def clear():
    global saved_username
    global saved_emailAddress
    global saved_password

    saved_username = ""
    saved_emailAddress = ""
    saved_password = ""
    return flask.redirect(url_for("index"))

def display_welcome_page():
    return flask.redirect(url_for("welcome"))

app.run()