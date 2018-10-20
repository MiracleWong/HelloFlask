from flask import Flask, flash, redirect, url_for, render_template, request
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Email
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

app = Flask(__name__)

# app.config.update(
#     SECRET_KEY=os.getenv('SECRET_KEY', 'secret string'),
#     MAIL_SERVER=os.getenv('MAIL_SERVER'),
#     MAIL_PORT=25,
#     MAIL_USE_TLS=True,
#     MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
#     MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
#     MAIL_DEFAULT_SENDER=('Miracle Wong', os.getenv('MAIL_USERNAME'))
# )

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret string'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('SENDGRID_API_KEY'),
    MAIL_DEFAULT_SENDER=('Miracle Wong', os.getenv('MAIL_USERNAME'))
)


mail = Mail(app)


# send over SMTP
def send_smtp_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)


def send_api_email(subject, to, body):
    sg = SendGridAPIClient(apikey=os.getenv('SENDGRID_API_KEY'))
    from_email = Email('noreply@miraclewong.me')
    to_email = Email(to)
    content = Content('text/plain', body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        send_api_email('Subscribe Success!', email, body=name)
        flash('Confirmation email have been sent! Check your inbox.')
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', form=form)


@app.route('/index')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
