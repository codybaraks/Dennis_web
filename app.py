from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector as connector
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer, SignatureExpired

from validation import *

db = connector.connect(host="localhost", user="root", passwd="root", database="dennis")

# mycursor = db.cursor()

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'earvinbaraka@gmail.com'
app.config['MAIL_PASSWORD'] = 'Commandprompt.1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config.from_pyfile('config.cfg')


app.secret_key = "fsggrsgsrgrg"

s = URLSafeSerializer('secretthistime!')


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


@app.route('/form')
def form():
    return render_template('contact.html')


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
    form = ContactForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            subscribe = request.form["subscribe"]

            print(subscribe)
            cursor = db.cursor()
            sql2 = "INSERT INTO `notification`(`subscribe`) VALUES (%s)"
            val = (subscribe,)
            cursor.execute(sql2, val)
            db.commit()
            flash("You're in, Thank you for Subscribing")

    return render_template('index.html', form=form)


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


# Mail Section

@app.route('/mailing', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subscribe = request.form['subscribe']
        token = s.dumps(subscribe, salt='email-confirm')
        print(subscribe)

        cursor = db.cursor()
        sql = "INSERT INTO `notification`(`subscribe`)VALUES (%s)"
        val = (subscribe,)
        cursor.execute(sql, val)
        db.commit()
        flash('Thank you For subscribing')

        msg = Message(subject='Eximix Subscription', sender='earvinbaraka@gmail.com',recipients=[request.form['subscribe']])
        link = url_for('conf_email', token=token, _external=True)
        msg.body = render_template('newsletters.html', token=token, link=link)

        mail.send(msg)

    return render_template('index.html', token=token)


# '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)


@app.route('/conf_email/<token>')
def conf_email(token):
    try:
        subscribe = s.loads(token, salt='email-confirm')
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    # return '<h1>The token works!</h1>'
    return render_template('index.html')


# to Handle Exceptions

@app.errorhandler(404)
def error_page(e):
    return render_template('Error_page.html')


if __name__ == '__main__':
    app.run()
