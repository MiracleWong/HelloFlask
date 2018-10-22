from flask import Flask, flash, redirect, url_for, render_template, request
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from threading import Thread

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


# send email with HTML body
def send_subscribe_mail(subject, to, **kwargs):
    message = Message(subject, recipients=[to], sender='Flask Weekly <%s>' % os.getenv('MAIL_USERNAME'))
    message.body = render_template('emails/subscribe.txt', **kwargs)
    message.html = render_template('emails/subscribe.html', **kwargs)
    mail.send(message)


# send email asynchronously
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_async_mail(subject, to, body):
    # app = current_app._get_current_object()  # if use factory (i.e. create_app()), get app like this
    message = Message(subject, recipients=[to], body=body)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


class EmailForm(FlaskForm):
    to = StringField('To', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit_smtp = SubmitField('Send with SMTP')
    submit_api = SubmitField('Send with SendGrid API')
    submit_async = SubmitField('Send with SMTP asynchronously')


class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        to = form.to.data
        subject = form.subject.data
        body = form.body.data
        if form.submit_smtp.data:
            send_smtp_mail(subject, to, body)
            method = request.form.get('submit_smtp')
        elif form.submit_api.data:
            send_api_email(subject, to, body)
            method = request.form.get('submit_api')
        else:
            send_async_mail(subject, to, body)
            method = request.form.get('submit_async')

        flash('Email sent %s! Check your inbox.' % ' '.join(method.split()[1:]))
        return redirect(url_for('index'))
    form.subject.data = 'Hello, World!'
    form.body.data = 'Across the Great Wall we can reach every corner in the world.'
    return render_template('index.html', form=form)


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        send_subscribe_mail('Subscribe Success!', email, body=name)
        flash('Confirmation email have been sent! Check your inbox.')
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', form=form)


@app.route('/index')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
