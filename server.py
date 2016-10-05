from flask import Flask, session, render_template, redirect, flash, request
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = 'ShhhSneaky'
mysql = MySQLConnector(app, 'email')

email_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_email', methods=['POST'])
def process_email():
    d = request.form
    if not email_REGEX.match(d['email']):
        flash("Email is Not Valid", 'error')
        return redirect('/')
    else:
        query = "INSERT INTO users (email, created_at) VALUES (:email, NOW())"
        data = {
                'email': d['email']
        }
        mysql.query_db(query, data)
        returnQuery = "SELECT u.email, u.created_at FROM users u"
        allEmail = mysql.query_db(returnQuery)
        flash("Email has been successfully added to the Database!", 'success')
        return render_template('success.html', all_emails = allEmail)

@app.route('/process_delete', methods=['POST'])
def process_delete():
    d = request.form
    checkQuery = 'SELECT COUNT(1) FROM users WHERE email = :email'
    data = {
           'email': d['email']
    }

    print mysql.query_db(checkQuery,data)[0]['COUNT(1)']

    if  mysql.query_db(checkQuery,data)[0]['COUNT(1)'] == 0:
        query = 'DELETE FROM users WHERE email = :email'
        mysql.query_db(query,data)
        flash('Email Deleted from Database!', 'success')
        return redirect('/')

    else:
        flash('Email address was not found', 'error')
        return redirect('/')



app.run(debug=True)
