from flask import Flask, render_template, request, flash, redirect, url_for
from forms import LoginForm
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        username = form.username.data
        flash("Welcome Home, %s" % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)


@app.route('/bootstrap')
def bootstrap():
    form = LoginForm()
    return render_template('bootstrap.html', form=form)


if __name__ == '__main__':
    app.run()
