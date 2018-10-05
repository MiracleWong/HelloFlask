from flask import Flask
import click

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello/<name>')
def great(name):
    return 'Hello %s!' % name


@app.cli.command('say-hello')
def hello():
    click.echo('Hello Human!')


if __name__ == '__main__':
    app.run()
