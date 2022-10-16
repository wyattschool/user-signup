from operator import contains
from time import sleep
from flask import Flask, abort, redirect, render_template, request, url_for
import flask

app = Flask(__name__)

#Define global variables

username = ""
email_address = ""
password = ""
invalid_username = ""
invalid_email = ""
invalid_password = ""
empty_field = "You have left this field empty. Please enter the appropriate information."
invalid_entry = "You have entered an invalid value."
error_message = ""
access_granted = False

#Check if the username meets the requirements
def verify_username_is_valid(entered_username):
    #Requirement is that the username be at least 3 characters long, must be shorter than 20 characters long, and not contain a space.
    if contains(entered_username," ") != True and len(entered_username) > 3 and len(entered_username) < 20:
        global username 
        username = entered_username
        return True
    else:
        if username == "":
            global invalid_username
            invalid_username = empty_field
            global error_message
            error_message = invalid_username
        else:
            clear_password()
            invalid_username = "Invalid username."
            error_message = invalid_username

#Check if the email meets the requirements
def verify_email_is_valid(email_address):
    #The email doesn't have to be entered so check that first.
    if email_address == "":
        return None
    #Requirement is that the email be valid so it must contain an @, a period, and be at least 3 characters long, but not longer than 20.
    if contains(email_address,"@") and contains(email_address,".") and len(email_address) > 3 and len(email_address) < 20:
        return True
    else:
        clear_password()
        global invalid_email
        invalid_email = "Invalid email address."
        global error_message
        error_message = invalid_email

#Check if the password meets the requirements
def verify_password_is_valid(password):
    if password == "":
            global invalid_password
            global error_message
            invalid_password = empty_field
            error_message = invalid_password
            return
    #Requirement is that the password be at least 3 characters long, must be shorter than 20 characters long, and not contain a space.
    if len(password) > 3 and len(password) <20 and contains(password," ") != True:
        return True
    else:
        clear_password()
        invalid_password = "Invalid password."
        error_message = invalid_password

#Check that all entered values are meet requirements
def verify_credentials(username,email_address,password):
    valid1 = verify_username_is_valid(username)
    valid2 = verify_email_is_valid(email_address)
    valid3 = verify_password_is_valid(password)
    #Email can be empty so check that it equals true or none
    if valid1 == True and valid2 == True and valid3 == True or valid1 == True and valid2 == None and valid3 == True: 
        global access_granted
        access_granted = True
        return True
    else:
        return 

def clear_password():
    global password
    password = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/",methods=['POST'])
def sign_up():
    username = (request.form['userName'])
    email_address = (request.form['emailAddress'])
    password = (request.form['passWord'])
    if verify_credentials(username,email_address,password) == True:
        clear_password()
        return display_welcome_page()
    else:
        global error_message
        if error_message == empty_field:
            error_message = "You have left a least field empty please fill in the required fields."
        clear_password()
        return render_template("index.html",
        errorMessage = error_message,
        invalidUsername = invalid_username,userName=username,
        invalidEmail = invalid_email,emailAddress = email_address,
        invalidPassword = invalid_password,passWord = password)

@app.route("/welcome")
def welcome():
    if access_granted == True:
        global username
        return render_template("welcome.html",
        userName = username)
    else:
        return flask.redirect(url_for("index"))

def display_welcome_page():
    return flask.redirect(url_for("welcome"))

app.run()