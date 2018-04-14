from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogging@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/')
def index():
    return redirect('/blog')


@app.route('/blog', methods=['POST', 'GET'])
def display_blog():
    return render_template("index.html")

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

        blogs = Blog.query.all()
    return render_template('new_post.html')


@app.route('/new_post', methods=['POST', 'GET'])
def validate_new_post():
    title = request.form['title']
    blog = request.form['blog']
    title_error = ''
    blog_error = ''

    if len(title) < 1:
        title_error = 'Please enter a title'
    if len(blog) < 1:
        blog_error = 'Please enter a blog'
    if not title_error or blog_error:
        return render_template('new_post.html', title=title, blog=blog)

if __name__ == '__main__':
    app.run()