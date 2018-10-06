from flask import Flask, render_template, Markup

app = Flask(__name__)

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
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run()
