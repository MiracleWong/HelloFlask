from flask import Flask, render_template
from forms import LoginForm
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/basic')
def basic():
    form = LoginForm()
    return render_template('basic.html', form=form)


@app.route('/bootstrap')
def bootstrap():
    form = LoginForm()
    return render_template('bootstrap.html', form=form)


if __name__ == '__main__':
    app.run()
