from flask import Flask, render_template, redirect,url_for, request,flash
import mysql.connector as connector

db = connector.connect(host="localhost", user="root", passwd="root", database="dennis")

app = Flask(__name__)
app.secret_key = "fsggrsgsrgrg"

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
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        country = request.form["country"]
        password = request.form["password"]

        print(name, email, country, password)
        cursor = db.cursor()
        sql = "INSERT INTO `users`(`name`, `email`, `country`, `password`) VALUES (%s,%s,%s,%s)"
        val = (name, email, country, password)
        cursor.execute(sql, val)
        db.commit()
        flash("saved in database")
        # redirect(url_for('show_register'))
    return render_template('contact.html')

@app.route('/form')
def form():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
