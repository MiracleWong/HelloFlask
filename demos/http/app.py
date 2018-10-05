import os
from flask import Flask, redirect, url_for, abort, make_response, json, jsonify, request, session
app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'asdfghjkl')


# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = '<h1>Hello, %s</h1>' % name

        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response


@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to the %d </p>' % (2018 - year)


@app.route('/404')
def not_found():
    abort(404)


@app.route('/foo')
def foo():
    # data = {
    #     'name': 'MiracleWong',
    #     'gender': 'man'
    # }
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response
    return jsonify(name='MiracleWong', gender='man')
    # return jsonify({name: 'MiracleWong', gender: 'man'})


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


## 模拟登录
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


## 模拟管理后台
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


## 模拟管理后台
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run()
