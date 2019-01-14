from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector as connector
from validation import *

db = connector.connect(host="localhost", user="root", passwd="root", database="dennis")

app = Flask(__name__)
app.secret_key = "fsggrsgsrgrg"


@app.route('/')
def house():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/projects')
def project():
    return render_template('projects.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            name = request.form["name"]
            email = request.form["email"]
            country = request.form["country"]
            phone = request.form["phone"]

            print(name, email, country, phone)
            cursor = db.cursor()
            sql = "INSERT INTO `users`(`name`, `email`, `country`, `phone`) VALUES (%s,%s,%s,%s)"
            val = (name, email, country, phone)
            cursor.execute(sql, val)
            db.commit()
            flash("saved in database")
    return render_template('contact.html', form=form)


@app.route('/notify', methods=['POST', 'GET'])
def notify():
    if request.method == 'POST':
        subscribe = request.form["subscribe"]

        print(subscribe)
        cursor = db.cursor()
        sql2 = "INSERT INTO `notification`(`subscribe`) VALUES (%s)"
        val = (subscribe,)
        cursor.execute(sql2, val)
        db.commit()
        flash("You're in, Thank you for Subscribing")
    return render_template('index.html')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        service = request.form["service"]
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        print(service, name, email, phone, message)
        cursor = db.cursor()
        sql2 = "INSERT INTO `feedback`(`service`, `name`, `email`, `phone`, `message`) VALUES (%s,%s,%s,%s,%s)"
        val = (service, name, email, phone, message)
        cursor.execute(sql2, val)
        db.commit()
        flash("Thank you for you Honest Feedback")
    return render_template('about.html')


@app.route('/form')
def form():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
