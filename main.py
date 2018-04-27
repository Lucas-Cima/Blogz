from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:bloggin@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route('/')
def index():

    if request.args.get('id'):
        user_id = request.args.get('id')
        user = User.query.filter_by(id=user_id).first()
        return render_template('index.html', user=user)
    else:
        users = User.query.all()
        return render_template("index.html", users=users)

    


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash('Logged in')
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exit', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        email_error = ''
        password_error = ''
        verify_error = ''

        if len(email) == 0:
            email_error = 'Please enter a username'
        if len(password) == 0:
            password_error = 'Plese enter a password'
        if verify != password:
            verify_error = 'Passwords do not match'

        if not email_error and not password_error and not verify_error:

            existing_user = User.query.filter_by(email=email).first()
            if not existing_user:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect('/blog')
            else:
                flash('User already exists', 'error')
        else:
            return render_template('signup.html', email_error=email_error, 
            password_error=password_error, verify_error=verify_error)



@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.args.get('user'):
        user = request.args.get('user')
        owner = User.query.filter_by(email=user).first()
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('singleUser.html', blogs=blogs, owner=owner, user=user)


    if request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.filter_by(id=blog_id).first()
        email_id = request.args.get('email')
        user = User.query.filter_by(email=email_id).first()
        return render_template('blog.html', blog=blog, user=user)
    else:
        email_id = request.args.get('email')
        
        user = User.query.filter_by(email=email_id).first()
        
        blogs = Blog.query.all()
        return render_template("main.html", blogs=blogs, user=user)


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
            blog_owner = User.query.filter_by(email=session['email']).first()
            new_blog = Blog(blog_title, blog_body, blog_owner)
            db.session.add(new_blog)
            db.session.commit()
            new_blog_id = new_blog.id
            return redirect('/blog?id=' + str(new_blog_id))
        
        else:
            return render_template('new_post.html', title_error=title_error, body_error=body_error)

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

if __name__ == '__main__':
    app.run()