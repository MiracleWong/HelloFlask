from flask import Flask, request, redirect, url_for

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return redirect('http://miracleprogramming.wang')


@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to the %d </p>' % (2018 - year)


if __name__ == '__main__':
    app.run()
