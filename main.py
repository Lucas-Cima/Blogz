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

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():

    return redirect('/blog')


@app.route('/blog', methods=['POST', 'GET'])
def display_blog():

    blogs = Blog.query.all()
    return render_template("index.html", blogs=blogs)

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['blog']
        title_error = ''
        body_error = ''
        
        if len(blog_title) == 0:
            title_error = 'Please fill out a title'
        
        if len(blog_body) == 0:
            body_error = 'Please fill in a blog'
        
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id={0}".format(Blog.id))
        
        else:
            return render_template('new_post.html', title_error=title_error, body_error=body_error)



if __name__ == '__main__':
    app.run()