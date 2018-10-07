from flask import Flask, render_template, Markup, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

user = {
    'username': 'Miracle Wong',
    'bio': 'A boy who loves moives and music.'
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/')
def hello_world():
    name = 'baz'
    return render_template('index.html', name = name)


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


# 注册模板上下文处理函数
@app.context_processor
def inject_info():
    foo = 'I am foo.'
    # return {'foo': foo}
    return dict(foo=foo)  # equal to: return {'foo': foo}


# 注册全局模板函数
@app.template_global()
def bar():
    return 'I am bar. '


# 内置过滤器
@app.route('/hello')
def hello():
    text = Markup('<h1>Hello, Flask!</h1>')
    return render_template('index.html', text=text)


# 自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


# Flash
@app.route('/flash')
def just_flash():
    flash("I'm a Flash, who is looking for me ?")
    return redirect(url_for('hello'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run()
