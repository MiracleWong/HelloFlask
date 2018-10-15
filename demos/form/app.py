import os
from flask import Flask, render_template, flash, redirect, url_for, send_from_directory, session
from forms import LoginForm, FortyTwoForm, UploadForm
import uuid

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        username = form.username.data
        flash("Welcome Home, %s" % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)


@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash("Welcome Home, %s" % username)
        return redirect(url_for('index'))
    return render_template('bootstrap.html', form=form)


@app.route('/custom-validator', methods=['GET', 'POST'])
def custom_validator():
    form = FortyTwoForm()
    if form.validate_on_submit():
        flash('Bingo!')
        return redirect(url_for('index'))
    return render_template('custom_validator.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')


if __name__ == '__main__':
    app.run()
