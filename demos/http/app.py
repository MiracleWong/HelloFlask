from flask import Flask, redirect, url_for, abort, make_response, json, jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return redirect('http://miracleprogramming.wang')


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


if __name__ == '__main__':
    app.run()
